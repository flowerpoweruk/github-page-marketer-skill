"""Evidence-based discoverability helpers. Candidates require semantic review."""

import re
from html.parser import HTMLParser


class _MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return
        attrs = dict(attrs)
        key = (attrs.get("property") or attrs.get("name") or "").lower()
        if key.startswith(("og:", "twitter:")) or key in {"description", "robots"}:
            self.meta[key] = attrs.get("content", "")


def social_metadata(html_text):
    parser = _MetadataParser()
    parser.feed(html_text)
    meta = parser.meta
    return {
        "status": "observed",
        "preview_tags_found": any(key.startswith(("og:", "twitter:")) for key in meta),
        "metadata": meta,
        "image_url": meta.get("og:image") or meta.get("twitter:image") or meta.get("twitter:image:src"),
        "note": "Metadata only. Image appearance and platform rendering have not been visually inspected.",
    }


def topic_candidates(readme, metadata):
    current = metadata.get("topics", [])
    if not isinstance(current, list) or any(not isinstance(item, str) for item in current):
        raise ValueError("metadata.topics must be an array of strings")
    valid = [item for item in current if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", item)]
    invalid = [item for item in current if item not in valid]
    candidates = []
    language = metadata.get("language")
    if isinstance(language, str):
        slug = {"C++": "cpp", "C#": "csharp", "F#": "fsharp"}.get(language, language.lower())
        if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", slug) and slug not in current:
            candidates.append({"topic": slug, "basis": "Repository language metadata", "status": "inferred"})
    terms = {
        "seo": r"\bseo\b|search engine optimi[sz]ation",
        "command-line": r"\bcli\b|command[- ]line",
        "accessibility": r"\baccessibility\b",
        "markdown": r"\bmarkdown\b",
        "github-actions": r"\bgithub actions\b",
        "static-analysis": r"\bstatic analysis\b",
        "data-visualization": r"\bdata visuali[sz]ation\b",
        "developer-tools": r"\bdeveloper tools?\b",
        "nextjs": r"\bnext\.?js\b",
        "react": r"\breact\b",
        "python": r"\bpython\b",
        "typescript": r"\btypescript\b",
        "rust": r"\brust\b",
    }
    seen = set(current) | {item["topic"] for item in candidates}
    for topic, pattern in terms.items():
        match = re.search(pattern, readme, re.I)
        if match and topic not in seen:
            candidates.append({"topic": topic, "basis": f"README mentions {match[0]!r}; confirm it describes the project rather than an incidental reference", "status": "inferred"})
            seen.add(topic)
    proposed = list(dict.fromkeys(valid))
    proposed.extend(item["topic"] for item in candidates if item["topic"] not in proposed)
    return {
        "status": "observed" if "topics" in metadata else "not_inspected",
        "current": current if "topics" in metadata else None,
        "invalid_format": invalid,
        "candidates_for_review": candidates,
        "draft_set_for_review": proposed[:20],
        "current_exceeds_limit": len(current) > 20,
        "limit": 20,
        "note": "No ranking or search-volume claim. Draft candidates are not final positioning recommendations; select only relevant topics, do not fill unused slots.",
    }


def ecosystem_evidence(readme, links):
    signals = {
        "npm": (r"\b(?:npm (?:install|i|add)|pnpm add|yarn add|bun add)\b|npmjs\.com", "npm website search documents title, description, README and keywords; published package content may differ from GitHub."),
        "PyPI": (r"\b(?:pip3? install|uv (?:add|pip install)|poetry add)\b|pypi\.org", "PyPI uses separately supplied summary, description and metadata; authors commonly publish the README as long description."),
        "crates.io": (r"\bcargo (?:add|install)\b|crates\.io", "Cargo supplies description, keywords, categories and README separately; do not assume README-body search."),
        "NuGet": (r"\bdotnet add.*?package\b|\bInstall-Package\b|nuget\.org", "NuGet documents package IDs, descriptions and tags as search inputs; displaying a README is a separate feature."),
    }
    results = []
    for name, (pattern, note) in signals.items():
        matches = list(re.finditer(pattern, readme, re.I))
        if matches:
            results.append({"ecosystem": name, "status": "inferred", "signals": [m[0] for m in matches[:5]], "mechanism": note, "published_metadata": "not_inspected"})
    return {"candidates": results, "linked_package_urls": [link["url"] for link in links if re.search(r"https://(?:www\.)?(?:npmjs\.com|pypi\.org|crates\.io|nuget\.org)/", link["url"])], "note": "Signals identify possible relevance, including incidental setup dependencies. Confirm the project's own published package before making ecosystem recommendations."}


def build_evidence(readme, metadata, structure, social=None):
    return {
        "search_alignment": {
            "repository_name": metadata.get("name"),
            "description": metadata.get("description"),
            "h1": [heading["text"] for heading in structure["headings"] if heading["level"] == 1],
            "default_github_search_fields": ["name", "description", "topics"],
            "readme_search_qualifier": "in:readme",
            "assessment": "Semantic keyword fit requires the host assistant's review; no special H1 weighting is asserted.",
        },
        "topics": topic_candidates(readme, metadata),
        "headings_and_links": {"headings": structure["headings"], "diagnostics": structure["diagnostics"], "sitelinks": "Google selects sitelinks automatically; anchors do not guarantee them."},
        "ecosystems": ecosystem_evidence(readme, structure["links"]),
        "social_preview": social or {"status": "not_inspected", "reason": "Repository HTML was not available; README images do not identify its social preview."},
    }
