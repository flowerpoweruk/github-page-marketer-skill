# GitHub Page Marketer Skill

**Find what stops visitors from understanding, trusting, and trying your GitHub project.**

A feedback-only marketing audit for an existing GitHub page. It reviews **Clarity, Conciseness, Compelling benefits, and Credibility**, with a separate **Discoverability** section covering search language, topics, navigation, package context, and social previews.

Give it your repository URL. The default audit works from the published page without an intake questionnaire. It identifies what works and prioritises the changes most likely to help the intended reader.

## Use it

Load the skill into a compatible assistant, then ask:

```text
Use GitHub Page Marketer to audit https://github.com/OWNER/REPO.
```

You can also supply a local or pasted README. The audit proceeds with available evidence and marks unavailable metadata or visuals as not inspected.

The skill does not edit the audited repository, open PRs, change settings, or post to social platforms. Suggested wording, topics and sharing badges are copyable outputs for you to review.

## What the report contains

- **What your page communicates:** a brief reading of the apparent audience, purpose, benefits and starting route.
- **What already works:** specific strengths to preserve.
- **Four Cs:** how effectively the page explains and presents the project.
- **Discoverability:** a distinct inspection of repository metadata and relevant page structure.
- **Priority improvements:** usually three to five, fewer when appropriate, each tied to evidence and a concrete recommendation.

See a [worked sample audit](examples/sample-audit.md). It uses a fictional project and makes no claims about real user outcomes.

## Audit and Advanced modes

**Audit** is the default: no positioning questionnaire. The skill infers what it can, qualifies uncertain judgments and treats ambiguity as a finding.

**Advanced** adds five optional questions about your intended audience, purpose and benefits. Ask for Advanced mode to compare your intent against what the page actually communicates.

1. **Who is the project primarily intended for?**
   The people the page should speak to most directly.
2. **What knowledge or experience do you expect those people to have?**
   This helps the audit judge whether explanations are appropriately technical or assume too much.
3. **What is the main thing the project enables them to do?**
   Its core purpose, before getting into supporting features.
4. **What do they gain from using it?**
   The practical benefits: less work, better results, more control, creative possibilities, or something else.
5. **Which of those benefits should be the strongest reason to try it?**
   This establishes what deserves emphasis, rather than treating every benefit as equally important.

Short answers, skipped questions and “not sure” are fine. The page-only reading comes first, so your answers do not conceal communication gaps.

## Discoverability

| Area | What gets reviewed |
| --- | --- |
| Search-language alignment | Repository name, About description, README heading and opening |
| Topic Tagging Engine | Current topics and a supported proposed set of up to 20 |
| Structure and navigation | Headings, section anchors, documentation links and alt text |
| Ecosystem context | Actual package identity and relevant registry metadata, where available |
| Social preview | Actual Open Graph tags and preview image, where accessible |

The audit respects documented platform behaviour: GitHub's default repository search uses name, description and topics; README search uses `in:readme`. Google sitelinks, social-card rendering and registry search differ by platform. The skill does not promise rankings, search traffic or CTR gains. [Mechanisms and sources](references/discoverability.md)

## Share Button Generator

Ask for GitHub-compatible share buttons and receive a compact Markdown row for Reddit and X. Hacker News is also supported. Known Discord invitations can be included separately as community links. The generator encodes actual project URLs and factual titles; it never submits a post.

```bash
python3 scripts/share_buttons.py \
  --repo flowerpoweruk/github-page-marketer-skill \
  --title "GitHub Page Marketer Skill — audit project pages and discoverability"
```

Use `--no-logos` for text-only badges, `--platforms reddit,x,hackernews` to select platforms, or `--format json` for structured output. [Generator details](references/share-buttons.md)

## Install

The skill runs in your existing assistant; no separate AI service, OpenAI API key, or paid backend is required. Helper tools use **Python 3.10+** and the standard library only. The skill itself can also work through the host's GitHub and browsing tools without running Python.

[Download the v1.0.0 skill bundle](https://github.com/flowerpoweruk/github-page-marketer-skill/raw/refs/heads/main/downloads/github-page-marketer-1.0.0.skill), or clone this repository and build it yourself:

```bash
git clone https://github.com/flowerpoweruk/github-page-marketer-skill.git
cd github-page-marketer-skill
python3 scripts/build_skill.py
```

This creates `dist/github-page-marketer.skill`, a ZIP-format bundle containing the skill, references, report template and runtime tools. A compatible host may import it directly; otherwise extract its `github-page-marketer` folder into the host's skills directory.

For Codex, install the extracted folder under `$CODEX_HOME/skills` (default `~/.codex/skills`):

```bash
python3 -m zipfile -e dist/github-page-marketer.skill "${CODEX_HOME:-$HOME/.codex}/skills"
```

If that skill folder already exists, compare or back it up before replacing it. Reload your assistant's skill discovery if needed. The host decides how skills are loaded; this project does not register a background service. [Core skill instructions](SKILL.md)

## Evidence collector

Optional tools help the assistant gather a consistent, read-only inventory:

```bash
# Public GitHub repository; optional existing GH_TOKEN for API access.
python3 scripts/audit.py --repo OWNER/REPO --output evidence.json

# Offline: no network requests.
python3 scripts/audit.py --readme /path/to/README.md --output evidence-offline.json
```

Offline snapshots can include `--metadata metadata.json`, `--html repository.html`, and `--repo-url https://github.com/OWNER/REPO`. Output files are never overwritten. The JSON contains observations and candidates, not an automated marketing score. The assistant uses the rubric to interpret them. [Tool options and limits](references/tools.md)

## The thinking behind it

The author's eight vetoes guide diagnosis: **demand, visibility, clarity, preference, confidence, value, friction, and experience**. For GitHub, value centres on “Is it worth my time?” rather than assuming a purchase. The vetoes support judgment; they are not eight compulsory criticisms. [Adapted framework](references/eight-vetoes.md)

The audit also checks the effectiveness of page elements such as the opening, examples, prerequisites, installation, configuration references, licence information and contribution guidance. It does not require every project to use the same template or penalise a useful short README for lacking decorative elements. [Audit rubric](references/audit-rubric.md)

## Development and validation

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_skill.py --check
python3 scripts/build_skill.py
```

GitHub Actions runs the checks on Python 3.10, 3.12 and 3.13 and uploads an installable archive as a workflow artifact. [Behavioural evaluation scenarios](evals/README.md) cover specialist tools, strong small pages, unclear claims, Advanced mode, one-off utilities, missing metadata, and untrusted README instructions. Unit tests verify tool behaviour; semantic judgment should also be evaluated in the host assistant.

The skill does not establish market demand, verify runtime reliability, audit security controls, execute project installation commands, or inspect material its tools cannot access. It reports those boundaries where they affect the findings.
