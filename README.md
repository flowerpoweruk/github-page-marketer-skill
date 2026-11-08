# GitHub Page Marketer Skill

**Find out what to improve on your GitHub project page.**

Built a GitHub project you want more people to try? Give GitHub Page Marketer your repository link and get a short, prioritised list of changes to help visitors understand what it does, see why it’s worth trying, and get started. No marketing experience needed.

[Install in Codex](#install) · [See a sample audit](examples/sample-audit.md)

<img src="assets/logo-readme.png" alt="GitHub Page Marketer Skill — white and green wordmark on a dark background" width="480">

## Use it

[Install the skill in Codex](#install), then select `github-page-marketer` in the skill picker. Replace `OWNER/REPO` with your repository and send this prompt.

```text
Use GitHub Page Marketer to audit https://github.com/OWNER/REPO.
```

The audit starts from your published page and explains what already works, what to change first, and why. You can also supply a local or pasted README. The report identifies any repository details it couldn’t inspect. You decide which edits to make.

### What a recommendation looks like

In the fictional Nimbus audit, the tool’s main use case was buried under *Architecture*. The audit suggested putting this sentence in the opening.

> Nimbus analyses failed GitHub Actions logs and suggests patches for you to review, apply and test.

[Read the worked sample audit](examples/sample-audit.md).

## Install

These instructions assume you have Codex CLI set up. Choose [macOS or Linux (Bash)](#macos-or-linux-bash) or [Windows 11 (PowerShell)](#windows-11-powershell). Both install the skill in Codex’s [user-level skills directory](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### macOS or Linux (Bash)

Choose a download or source build, then run **Install and verify** in the same shell. You need `python3` (Python 3.10 or later) for either route. The download uses `curl` and the source build uses Git.

#### Option 1. Download the v1.0.1 bundle

```bash
download_dir="$(mktemp -d)" &&
  bundle="$download_dir/github-page-marketer-1.0.1.skill" &&
  curl --fail --location --output "$bundle" \
    'https://github.com/flowerpoweruk/github-page-marketer-skill/raw/refs/heads/main/downloads/github-page-marketer-1.0.1.skill'
```

You can also [download the bundle in your browser](https://github.com/flowerpoweruk/github-page-marketer-skill/raw/refs/heads/main/downloads/github-page-marketer-1.0.1.skill) and set `bundle` to the full path of the downloaded file.

#### Option 2. Clone and build from source

```bash
git clone https://github.com/flowerpoweruk/github-page-marketer-skill.git &&
  cd github-page-marketer-skill &&
  python3 scripts/build_skill.py &&
  bundle="$PWD/dist/github-page-marketer.skill"
```

The builder creates `dist/github-page-marketer.skill` and refuses to overwrite an existing archive.

#### Install and verify

Once you have the bundle, extract it to `$HOME/.agents/skills`. The archive creates the `github-page-marketer` folder for you. Move any existing copy to a backup location outside your skills directories before replacing it.

```bash
(
  set -eu

  skills_dir="$HOME/.agents/skills"
  skill_dir="$skills_dir/github-page-marketer"

  if [ -e "$skill_dir" ] || [ -L "$skill_dir" ]; then
    printf 'A copy already exists at %s. Back it up before installing.\n' "$skill_dir" >&2
    exit 1
  fi

  mkdir -p "$skills_dir"
  python3 -m zipfile -e "${bundle:?Download or build the bundle first.}" "$skills_dir"
  test -f "$skill_dir/SKILL.md"
  printf 'Verified skill file in %s\n' "$skill_dir"
)
```

### Windows 11 (PowerShell)

Use these steps with Codex CLI running natively on Windows 11. Choose one way to get the bundle, then run the install commands in the same PowerShell window.

#### Option 1. Download the v1.0.1 bundle

```powershell
$bundle = Join-Path $env:TEMP 'github-page-marketer-1.0.1.zip'
$url = 'https://github.com/flowerpoweruk/github-page-marketer-skill/raw/refs/heads/main/downloads/github-page-marketer-1.0.1.skill'
Invoke-WebRequest -Uri $url -OutFile $bundle -UseBasicParsing -ErrorAction Stop
```

The `.skill` bundle is already a ZIP archive. Saving it with a `.zip` extension lets PowerShell extract it with `Expand-Archive`.

#### Option 2. Clone and build from source

Install Git for Windows and Python 3.10 or later. The commands use the Windows Python launcher (`py`). If your Python installation uses `python`, run `python --version` to confirm the version, then replace `py -3` with `python`.

```powershell
git clone https://github.com/flowerpoweruk/github-page-marketer-skill.git
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }
Set-Location -LiteralPath '.\github-page-marketer-skill' -ErrorAction Stop

$bundle = Join-Path (Get-Location).Path 'dist\github-page-marketer.zip'
py -3 scripts/build_skill.py --output "$bundle"
if ($LASTEXITCODE -ne 0) { throw 'Skill build failed.' }
```

#### Install and verify

Extract the archive into Codex's [user-level skills directory](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), `$HOME\.agents\skills`. The archive creates the `github-page-marketer` folder for you. If you're replacing an existing copy, move it to a backup location outside your skills directories first.

```powershell
$skillsDir = Join-Path $HOME '.agents\skills'
$skillDir = Join-Path $skillsDir 'github-page-marketer'

if (Test-Path -LiteralPath $skillDir) {
    throw "A copy already exists at $skillDir. Back it up before installing."
}

Expand-Archive -LiteralPath $bundle -DestinationPath $skillsDir -ErrorAction Stop

foreach ($file in 'SKILL.md', 'agents\openai.yaml', 'assets\icon.png',
                  'references\audit-rubric.md', 'templates\report.md', 'scripts\audit.py') {
    $path = Join-Path $skillDir $file
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing installed file $path"
    }
}

Write-Output "Verified skill files in $skillDir"
```

### Run your first audit

In Codex CLI, type `$` in the prompt and look for `github-page-marketer` (GitHub Page Marketer Skill). If it doesn’t appear, exit Codex, start it again with `codex`, and check the picker again. Select the skill and [send the audit prompt](#use-it).

## What the report contains

- **What your page communicates.** Who it seems to be for, what the project does, and how a visitor would get started.
- **What already works.** The parts of the page worth keeping.
- **Four Cs.** How clearly and concisely the page explains the project, how compelling its benefits are, and what makes its claims credible.
- **Discoverability.** How the page and repository metadata help people find and navigate the project.
- **Priority improvements.** Usually three to five changes, each tied to evidence and a concrete recommendation.

## Audit and Advanced modes

**Audit** starts with the project page and needs no questionnaire.

**Advanced** compares what the page communicates with what you want it to communicate. Ask for Advanced mode and answer as many of the [five questions about audience, purpose and benefits](references/advanced-mode.md) as you like.

## Discoverability

| Area | What gets reviewed |
| --- | --- |
| Search-language alignment | Repository name, About description, README heading and opening |
| Topic Tagging Engine | Current topics and a supported proposed set of up to 20 |
| Structure and navigation | Headings, section anchors, documentation links and alt text |
| Ecosystem context | Actual package identity and relevant registry metadata, where available |
| Social preview | Actual Open Graph tags and preview image, where accessible |

See how the audit handles [GitHub search, repository topics and social previews](references/discoverability.md).

## Share Button Generator

Ask for GitHub-compatible Markdown share buttons for Reddit and X. Hacker News is also available. If you have a Discord community invite, the skill can format it as a separate link. You choose where to use the output. [Generator commands and options](references/share-buttons.md)

## Evidence collector

The optional Python tools collect a read-only inventory from a public repository or local snapshots. They use Python 3.10 or later and the standard library. The skill can also work with the evidence available to Codex. [Live and offline commands](references/tools.md)

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
