# GitHub Page Marketer Skill

Audit your GitHub project page for clarity, conciseness, compelling benefits, credibility, and discoverability.

**Status: planning.** This repository is the development home for the skill. An installable skill has not been implemented yet.

## What it will do

Help developers with existing GitHub project pages understand what their page communicates, what already works, and which improvements would most help prospective users understand, trust, and try the project.

The skill will provide analysis and actionable feedback. It will not edit the audited repository or publish changes.

## Audit modes

### Audit

The default mode takes a repository URL and audits the published page without an intake questionnaire. It infers audience and purpose from the available information, identifies ambiguity, and distinguishes observations from assumptions.

### Advanced

The same audit, informed by five optional questions and their explanations:

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

The audit first assesses the page on its own, then compares what it communicates with the author's intended audience, purpose, and benefits.

## Communications review

The report uses four Cs:

| Criterion | Main question |
| --- | --- |
| Clarity | Can the intended reader understand the project and how to begin? |
| Conciseness | Does the page communicate efficiently, with appropriate emphasis? |
| Compelling | Does it give the right reader a meaningful reason to try the project? |
| Credibility | Are its promises supported and appropriately qualified? |

The author's eight vetoes inform the diagnosis: demand, visibility, clarity, preference, confidence, value, friction, and experience. Value emphasises whether adoption is worth the user's time and effort. The vetoes are diagnostic lenses, not compulsory report sections.

## Discoverability

A separate report section will examine:

- Search-language alignment across the README heading, repository name, and description.
- Repository topics, with a proposed relevant set within GitHub's 20-topic limit.
- Markdown headings, section anchors, useful documentation links, and image alt text.
- Ecosystem and package discoverability, using registry-specific evidence where applicable.
- Actual social-preview metadata and images, where accessible.

GitHub's default repository search examines names, descriptions, and topics; README-content search requires `in:readme`. The audit must not promise rankings, Google sitelinks, or click-through improvements.

## Optional share-button generator

Generate GitHub-compatible, ready-to-paste Markdown for Shields.io sharing badges using the project's actual URL and a factual description. Community links such as Discord require a supplied or documented destination and are labelled separately. This feature will not post to social platforms or edit the repository.

## Report principles

- Describe what the page currently communicates and identify strengths worth preserving.
- Prioritise roughly three to five consequential improvements without forcing a minimum.
- Ground each finding in evidence, explain its effect on the reader, and recommend a concrete improvement.
- Review relevant page elements for effectiveness rather than requiring every project to follow a template.
- Identify facts that need substantiation; never invent adoption figures, benchmarks, endorsements, or setup times.
- Distinguish communication gaps from unverified product behaviour.
- Mark inaccessible material as not inspected; do not imply commands were tested or links checked when they were not.
- Keep external campaigns, outreach, product redesign, and security audits outside the review.

## Development

Next steps are to implement `SKILL.md`, supporting audit references, a report template, share-button generation, and representative evaluation examples.
