# Four Cs and page inspection

Evaluate appropriateness for the intended reader, not compliance with a universal README template. A missing optional element is not a finding unless it leaves a material question unanswered. Do not award scores for section counts.

| C | Examine | Avoid |
| --- | --- | --- |
| Clarity | Audience, concrete purpose, assumed knowledge, supported use cases, examples, requirements, next step | Removing necessary jargon, replacing technical precision with slogans, claiming observed user confusion without user evidence |
| Conciseness | Useful emphasis, redundancy, economical language, scannability, navigable depth | Arbitrary length limits, deleting essential setup or limitations, calling every long README bloated |
| Compelling | Relevance, benefits, reason to choose, representative demonstration, return on adoption effort | Hype, generic praise, unsupported superiority, forced pain points, treating stars as a business objective |
| Credibility | Claim-specific support, realistic promises, maturity, boundaries, appropriate accountability | Decorative proof, invented statistics, treating a badge as a security guarantee, penalising honest experimental status |

## Checklist from the author's notes

Inspect presence **and effectiveness**, applying only relevant items:

| Element | Assessment |
| --- | --- |
| Title and concise tagline | Establish purpose promptly, with accurate category/task language; do not force a literal tagline when the opening already works |
| Banner or logo | Recognition, readability, visual weight and loading burden; optional, not a universal requirement |
| Build/version/licence badges | Relevant, understandable information without crowding; distinguish each badge's actual meaning from general project health |
| Demo GIF, screenshot or video | Show a representative task/result; code and sample output can be better for libraries and CLIs |
| Table of contents | Useful navigation for long pages; account for GitHub's automatic heading outline before demanding a manual TOC |
| Why / problem or desire | Audience-relevant circumstance and reason to care, not merely the creator's build story |
| Key features | Prioritised, scannable capabilities tied to benefits; no compulsory feature list |
| Prerequisites/system requirements | Dependencies, OS/runtime versions, accounts, permissions and required services before starting |
| Installation | Ordered instructions, copyable commands, explicit placeholders, relevant configuration; presentation review is not execution testing |
| Quickstart/usage | A supported path to a useful result and enough context to recognise success |
| API/configuration reference | Relevant flags, arguments, environment variables and options; clearly labelled links to fuller documentation are sufficient |
| Contributions | A route to contribution instructions and PR expectations when contributions are welcome; not every repository seeks contributors |
| Licence | Stated licence and accessible terms; never infer a licence from public visibility, prescribe a licence, or offer legal assurance |
| Acknowledgments/credits | Relevant contributors, dependencies and inspirations; missing a generic credits section is not automatically an omission |

## Priority and evidence

Use **High**, **Medium**, or **Optional** only to express practical priority, not a calculated score. High means a material obstacle such as an unclear purpose, misleading central promise or missing step in the only starting route. Medium means a useful improvement to evaluation or adoption. Optional means context-dependent polish.

For every main recommendation record: specific location or excerpt; what is observed; likely consequence for the intended reader; supported change; facts requiring substantiation. Quote sparingly. Preserve strengths with equal specificity. Do not turn an automated diagnostic into a finding without judging its importance.

## Calibration examples

- A niche compiler library may rightly lead with its intermediate representation and compatibility constraints. Do not simplify it for non-programmers unless that is the intended audience.
- A 25-line CLI README with purpose, input/output and install command may be excellent. No logo, manual TOC or testimonial is needed.
- A beautiful screenshot of an empty dashboard does not demonstrate the useful outcome.
- “Production-ready” beside an experimental-status note warrants a specific expectation check; the audit cannot establish actual reliability.
- A missing instruction to create the configuration file is friction. Several required services may be necessary product complexity, not bad documentation.
