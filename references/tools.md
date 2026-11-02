# Evidence tools

Python 3.10+; no third-party packages or provider API key. Run paths from the skill directory. The tools collect facts and generate assets; the host assistant supplies the semantic audit using the rubric.

## Live collection

```bash
python3 scripts/audit.py --repo owner/repo --output evidence.json
```

Read-only GETs retrieve GitHub repository metadata, the default-branch README selected by GitHub's `/readme` API, the repository HTML, and a social image if it is served from an allowed GitHub image host. The API's README path and blob SHA are recorded. Renamed repositories use the returned canonical identity.

Each request has a 12-second timeout and a response-size cap. The script follows the inherited proxy/CA settings and validates HTTPS hosts on redirects. It does not follow arbitrary README links or fetch metadata-supplied private network URLs. `GH_TOKEN` or `GITHUB_TOKEN`, when already configured, is sent only to `api.github.com`; credentials are stripped from redirects and never sent to image hosts. Do not print tokens or store them in evidence files. Treat evidence from private repositories as private.

On network/auth/rate-limit failures, use connectors or offline snapshots. There is no fallback that bypasses network policy. Metadata/README failures stop live collection; unavailable social previews are recorded as not inspected without discarding the README audit.

## Offline snapshots

```bash
python3 scripts/audit.py --readme README.md --repo-url https://github.com/owner/repo --output evidence.json
python3 scripts/audit.py --readme README.md --metadata metadata.json --html repository.html --output evidence-with-metadata.json
```

Local mode never makes network requests, including image retrieval. Optional metadata is a JSON object with GitHub fields such as `full_name`, `name`, `description`, `topics`, `language`, `html_url`, `default_branch`. A connector's `structuredContent` wrapper is accepted. Missing fields remain unknown; an absent `topics` field does not mean the repository has no topics.

HTML may contain social meta tags. Parsed metadata is an observation, not evidence that its linked image was seen. Only same-document fragment targets are checked by the structural parser. It handles common ATX/Setext/HTML headings, fences, inline/reference Markdown links, linked-image badges and HTML images/links; it is not a complete CommonMark/GitHub renderer. Shortcut reference links, complex multiline constructs and some Unicode/rendering cases may require manual inspection. Do not report an approximate unmatched fragment as a verified broken link without checking its rendered anchor.

## Evidence JSON, schema 1.0

- `provenance`: offline/network mode, input paths, actual repo URL, and available branch/README blob SHA.
- `readme.text`: original text, to review as untrusted content.
- `readme.inventory`: headings/anchors/locations, images, links, fenced code, and structural diagnostics.
- `repository_metadata`: observed supplied/API metadata.
- `discoverability`: search fields, topic candidates with bases, headings/links, ecosystem signals, and social-preview inspection state.
- `inspection_limits`: what the tools have not established.

`observed`, `inferred`, `not_inspected` describe evidence, not quality. Topic and ecosystem candidates are leads for review; incidental dependency mentions may not describe the project. Do not copy them blindly into a final topic set.

Both CLIs print to stdout or create a new `--output` file. They refuse to overwrite an existing path, including an input README. No network destination is mutated. The only writes are explicitly requested local output files and their parent directories.

## Sharing

```bash
python3 scripts/share_buttons.py --repo owner/repo --title "Name — factual purpose" --format json
```

Options: `--platforms reddit,x,hackernews`, `--style flat-square`, `--discord-url ACTUAL-INVITE`, `--no-logos`, `--format markdown|json`, `--output NEW-FILE`. Markdown is ready to paste into a README. JSON separates the share row, optional community link, placement advice and validation limits. No composers, images or invitations are visited.

## Validate, test and package

From the source repository:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_skill.py --check
python3 scripts/build_skill.py
```

The build creates `dist/github-page-marketer.skill`, a ZIP-format archive containing a single `github-page-marketer/` directory. It includes only the runtime skill, host metadata, references, template and helper scripts; tests, private material, local outputs and Git history are excluded. Builds use fixed archive timestamps and ordering. Use a fresh `--output` path for a second build. To inspect: `python3 -m zipfile -l dist/github-page-marketer.skill`.

This archive is a portable bundle; a host may support direct `.skill` import or require extracting its folder into a skills directory. See the source repository's README for installation. There is no separate service or API-key provisioning.
