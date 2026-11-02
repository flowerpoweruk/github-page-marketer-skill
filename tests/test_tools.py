import base64
from contextlib import redirect_stdout, redirect_stderr
import hashlib
from io import StringIO
import json
from pathlib import Path
import struct
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from page_marketer.cli import audit_main, share_main
from page_marketer.discoverability import social_metadata, topic_candidates
from page_marketer.github import CollectionError, IMAGE_HOSTS, _SafeRedirect, collect, image_dimensions, inspect_preview_image, parse_repository, validate_url
from page_marketer.markdown import inventory
from page_marketer.share import badge_text, generate
from build_skill import package, validate


class MarkdownTests(unittest.TestCase):
    def test_fences_comments_and_inline_code_are_not_findings(self):
        text = '# Real\n<!-- ![](hidden.png) -->\n```md\n# False\n[x](#absent)\n```\n`[x](#absent)`\n'
        result = inventory(text)
        self.assertEqual([h["text"] for h in result["headings"]], ["Real"])
        self.assertFalse(result["diagnostics"])

    def test_unicode_duplicate_headings_and_custom_anchors(self):
        text = '# Café & Tools!\n## Usage\n## Usage\n<a id="custom"></a>\n[one](#café--tools) [two](#usage-1) [three](#custom)\n'
        result = inventory(text)
        self.assertEqual([h["anchor"] for h in result["headings"]], ["café--tools", "usage", "usage-1"])
        self.assertFalse(result["diagnostics"])

    def test_broken_fragment_is_not_a_claim_about_external_links(self):
        result = inventory('# Tool\n[bad](#usage) [external](https://example.org/#usage)\n')
        self.assertEqual([item["code"] for item in result["diagnostics"]], ["unresolved_section_link"])

    def test_setext_and_html_headings(self):
        result = inventory('Title\n=====\n\n<h2>Usage</h2>\n[x](#usage)\n')
        self.assertEqual([h["level"] for h in result["headings"]], [1, 2])
        self.assertFalse(result["diagnostics"])

    def test_linked_badges_and_balanced_url_parentheses(self):
        text = '[![Share on X](https://img.shields.io/badge/X-black)](https://twitter.com/intent/tweet?url=repo)\n[Doc](https://example.org/a_(b))'
        result = inventory(text)
        self.assertEqual(result["images"][0]["label"], "Share on X")
        self.assertEqual(result["links"][0]["url"], "https://twitter.com/intent/tweet?url=repo")
        self.assertEqual(result["links"][1]["url"], "https://example.org/a_(b)")

    def test_reference_links_and_html_images(self):
        result = inventory('![Result][image]\n[Docs][]\n[image]: result.png\n[docs]: docs.md\n<img src="other.png" alt="Result">\n')
        self.assertEqual(len(result["images"]), 2)
        self.assertEqual(result["links"][0]["url"], "docs.md")
        self.assertFalse(result["diagnostics"])

    def test_empty_alt_and_unclosed_fence(self):
        result = inventory('![](result.png)\n```sh\nrun something\n')
        self.assertEqual({item["code"] for item in result["diagnostics"]}, {"empty_image_alt", "unclosed_code_fence"})


class DiscoverabilityTests(unittest.TestCase):
    def test_social_tags_are_case_insensitive_and_decode_entities(self):
        social = social_metadata('<meta property="og:title" content="Tool &amp; Docs"><meta name="twitter:image" content="https://example.org/img.png">')
        self.assertEqual(social["metadata"]["og:title"], "Tool & Docs")
        self.assertEqual(social["image_url"], "https://example.org/img.png")
        self.assertIn("not been visually inspected", social["note"])

    def test_absent_and_empty_topics_remain_distinct(self):
        self.assertEqual(topic_candidates("", {})["status"], "not_inspected")
        self.assertIsNone(topic_candidates("", {})["current"])
        self.assertEqual(topic_candidates("", {"topics": []})["status"], "observed")

    def test_inspected_html_without_preview_tags_is_not_unknown(self):
        result = social_metadata("<html><h1>Tool</h1></html>")
        self.assertEqual(result["status"], "observed")
        self.assertFalse(result["preview_tags_found"])

    def test_topic_candidates_have_evidence_are_bounded_and_not_padded(self):
        result = topic_candidates("A Python CLI for SEO checks.", {"topics": ["seo"], "language": "Python"})
        self.assertEqual(result["draft_set_for_review"], ["seo", "python", "command-line"])
        self.assertTrue(all(item["basis"] for item in result["candidates_for_review"]))
        self.assertEqual(len(topic_candidates("Python CLI", {"topics": [f"topic-{i}" for i in range(20)]})["draft_set_for_review"]), 20)

    def test_malformed_topics_are_not_silently_accepted(self):
        with self.assertRaises(ValueError):
            topic_candidates("", {"topics": "seo"})
        self.assertEqual(topic_candidates("", {"topics": ["bad_tag"]})["invalid_format"], ["bad_tag"])


class ShareTests(unittest.TestCase):
    def test_title_and_url_round_trip_without_query_injection(self):
        title = 'Tool & examples #1 — café? x=y / "quotes"'
        result = generate("https://github.com/example/a-b", title, ["reddit", "x", "hackernews"])
        links = inventory(result["share_markdown"])["links"]
        self.assertEqual(len(links), 3)
        for link in links:
            query = parse_qs(urlsplit(link["url"]).query)
            title_key = "text" if "twitter.com" in link["url"] else "t" if "ycombinator" in link["url"] else "title"
            url_key = "u" if "ycombinator" in link["url"] else "url"
            self.assertEqual(query[title_key], [title])
            self.assertEqual(query[url_key], ["https://github.com/example/a-b"])
            self.assertNotIn("x", query)

    def test_shields_literal_hyphens_and_underscores(self):
        self.assertEqual(badge_text("a-b_c d"), "a--b__c%20d")

    def test_discord_is_separate_and_no_network_is_used(self):
        with patch("urllib.request.OpenerDirector.open", side_effect=AssertionError("Unexpected network")):
            result = generate("example/tool", "Tool", discord_url="https://discord.gg/real-code")
        self.assertNotIn("Discord", result["share_markdown"])
        self.assertIn("Join Discord", result["community_markdown"])
        self.assertIn("5865F2", result["community_markdown"])

    def test_rejects_unsafe_or_invalid_destinations(self):
        for repo in ["https://evil.example/a/b", "https://github.com@evil.example/a/b", "a/../b", "a/b/extra", "a/b?injected=yes"]:
            with self.subTest(repo=repo), self.assertRaises(ValueError):
                generate(repo, "Tool")
        for invite in ["javascript:alert(1)", "https://discord.gg.evil.example/code", "https://discord.gg/", "https://user@discord.gg/code"]:
            with self.subTest(invite=invite), self.assertRaises(ValueError):
                generate("example/tool", "Tool", discord_url=invite)

    def test_invalid_title_platform_and_optional_logos(self):
        with self.assertRaises(ValueError):
            generate("a/b", "line\nbreak")
        with self.assertRaises(ValueError):
            generate("a/b", "Tool", ["unknown"])
        self.assertNotIn("logo=", generate("a/b", "Tool", use_logo=False)["share_markdown"])


class CollectionTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual(parse_repository("https://github.com/example/tool.git/"), "example/tool")
        for value in ["http://github.com/a/b", "https://github.com/a/b/tree/main", "https://github.com:444/a/b", "a/.."]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_repository(value)

    def test_image_hosts_and_redirects_do_not_leak_authorization(self):
        for url in ["http://opengraph.githubassets.com/a", "https://127.0.0.1/a", "https://opengraph.githubassets.com.evil.example/a"]:
            with self.subTest(url=url), self.assertRaises(CollectionError):
                validate_url(url, IMAGE_HOSTS)
        req = Request("https://api.github.com/repos/a/b", headers={"Authorization": "Bearer secret"})
        redirected = _SafeRedirect({"api.github.com"}).redirect_request(req, None, 302, "", {}, "https://api.github.com/repos/a/c")
        self.assertIsNone(redirected.get_header("Authorization"))
        with self.assertRaises(CollectionError):
            _SafeRedirect({"api.github.com"}).redirect_request(req, None, 302, "", {}, "https://evil.example/a")

    def test_image_dimensions_and_technical_only_inspection(self):
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + struct.pack(">II", 1280, 640)
        self.assertEqual(image_dimensions(png), (1280, 640))
        self.assertEqual(image_dimensions(b"GIF89a" + struct.pack("<HH", 640, 320)), (640, 320))
        with patch("page_marketer.github.request", return_value=(png, "image/png")) as mocked:
            result = inspect_preview_image("https://opengraph.githubassets.com/a/b")
        self.assertEqual(result["visual_review"], "not_inspected")
        self.assertNotIn("token", mocked.call_args.kwargs)

    def test_live_collection_uses_selected_readme_path_and_branch(self):
        metadata = {"full_name": "example/tool", "name": "tool", "default_branch": "docs/main", "topics": []}
        readme = {"path": ".github/README.md", "sha": "blob123", "encoding": "base64", "content": base64.b64encode(b"# Tool\n").decode()}
        with patch("page_marketer.github._json_request", side_effect=[metadata, readme]) as api, patch("page_marketer.github.request", side_effect=CollectionError("HTML unavailable")):
            text, _, social, provenance = collect("example/tool")
        self.assertEqual(text, "# Tool\n")
        self.assertIn("ref=docs%2Fmain", api.call_args_list[1].args[0])
        self.assertEqual(provenance["readme_path"], ".github/README.md")
        self.assertEqual(social["status"], "not_inspected")


class CLITests(unittest.TestCase):
    def test_offline_collection_with_snapshots_never_networks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme, meta, html, output = [root / name for name in ("README.md", "metadata.json", "page.html", "evidence.json")]
            readme.write_text("# Sample CLI\n\nA Python CLI.\n", encoding="utf-8")
            meta.write_text(json.dumps({"full_name": "example/sample", "topics": []}), encoding="utf-8")
            html.write_text('<meta property="og:title" content="Sample">', encoding="utf-8")
            with patch("urllib.request.OpenerDirector.open", side_effect=AssertionError("Unexpected network")):
                self.assertEqual(audit_main(["--readme", str(readme), "--metadata", str(meta), "--html", str(html), "--output", str(output)]), 0)
            evidence = json.loads(output.read_text())
            self.assertEqual(evidence["provenance"]["mode"], "offline")
            self.assertEqual(evidence["discoverability"]["social_preview"]["metadata"]["og:title"], "Sample")

    def test_output_cannot_overwrite_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            original = "# Keep this\n"
            path.write_text(original)
            with redirect_stderr(StringIO()):
                status = audit_main(["--readme", str(path), "--output", str(path)])
            self.assertEqual(status, 1)
            self.assertEqual(path.read_text(), original)

    def test_share_cli_and_invalid_input(self):
        out = StringIO()
        with redirect_stdout(out):
            self.assertEqual(share_main(["--repo", "a/b", "--title", "Tool", "--format", "json"]), 0)
        self.assertIn("share_markdown", json.loads(out.getvalue()))
        with redirect_stderr(StringIO()):
            self.assertEqual(share_main(["--repo", "a/b", "--title", "Tool", "--platforms", "invalid"]), 1)


class PackageTests(unittest.TestCase):
    def test_skill_is_complete_and_archive_reproducible(self):
        self.assertEqual(validate(), [])
        with tempfile.TemporaryDirectory() as directory:
            first, second = [package(Path(directory) / name) for name in ("first.skill", "second.skill")]
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(), hashlib.sha256(second.read_bytes()).digest())
            with zipfile.ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                names = archive.namelist()
                self.assertIn("github-page-marketer/SKILL.md", names)
                self.assertIn("github-page-marketer/scripts/audit.py", names)
                self.assertFalse(any("__pycache__" in name or ".git/" in name or "tests/" in name for name in names))

    def test_extracted_bundle_runs_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = package(root / "bundle.skill")
            with zipfile.ZipFile(archive) as zipped:
                zipped.extractall(root / "installed")
            scripts = root / "installed" / "github-page-marketer" / "scripts"
            readme = root / "README.md"
            readme.write_text("# Tool\n\nA local utility.\n")
            audit = subprocess.run([sys.executable, str(scripts / "audit.py"), "--readme", str(readme)], cwd=root, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(audit.stdout)["provenance"]["mode"], "offline")
            share = subprocess.run([sys.executable, str(scripts / "share_buttons.py"), "--repo", "example/tool", "--title", "Tool", "--format", "json"], cwd=root, capture_output=True, text=True, check=True)
            self.assertIn("share_markdown", json.loads(share.stdout))


if __name__ == "__main__":
    unittest.main()
