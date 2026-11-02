# Discoverability audit

Keep this separate from the four Cs in the report. Inspect the README plus relevant GitHub metadata. This is a repository-page audit, not an external promotion plan. Distinguish matching/indexing mechanisms from ranking promises.

## 1. Search-language alignment

Identify a small number of accurate category and task phrases from the page. In Advanced mode consider the author's intended positioning but substantiate capability claims. Compare repository name, About description, README H1 and opening for meaningful consistency, not exact repeated strings.

GitHub documents default repository search across **name, description and topics**. The `in:readme` qualifier searches README contents. Therefore changing an H1 alone does not establish default search visibility, and GitHub documents no special H1 keyword boost. Recommend natural language rather than keyword density or a list of synonyms.

Example: a heading “Purple Panda Digital Tool” could become “Purple Panda — SEO Discoverability Tool” if the project actually serves that purpose. Separately suggest a concrete repository description and relevant topics. Distinguish changing the README heading from renaming the repository slug. Do not rename anything or insist a recognised project brand must change.

Use candidate phrases, not invented search volumes or claims that a query is popular. Query matching does not guarantee position, traffic or adoption.

## 2. Topic Tagging Engine

GitHub supports topic search (`topic:seo`, `seo in:topics`) and includes topics in default repository search. Limits: **20 topics**, each no more than **50 characters**, using lowercase letters, numbers and hyphens.

Read actual current topics through a connector, repository API or rendered page. Build a set representing supported purpose, main use cases, language and genuinely relevant ecosystem. Preserve useful topics; explain additions and removals. A popular topic that misrepresents the project should not be added. Do not pad to 20, or use an incidental dependency as the project's defining topic.

Return a copyable proposed set and brief reasons. Script-generated candidates are **inferred**, based on explicit mentions and metadata; semantic relevance still needs review. If current topics are inaccessible, label them not inspected and distinguish proposed candidates from observed configuration.

## 3. Headings, anchors, links and alt text

GitHub creates section anchors and an automatic heading outline. Check useful descriptive headings, hierarchy, and same-page links; duplicate headings receive suffixes. Heading changes can break existing fragment links. Prefer the actual rendered anchors when available; the tool's Markdown parser is an approximation, not a full GitHub renderer.

Google can show headings/anchors as sitelinks, selected automatically. Clear structure supports navigation; it does not force sitelinks or independently index every URL fragment.

Check descriptive internal documentation links and image alt text. Relative links are useful for repository navigation, but do not assert a special crawler preference or ranking benefit. Markdown and HTML images both need inspection. Informative images need useful descriptions; decorative images may appropriately use empty alt text. Do not stuff keywords into alt text.

## 4. Package-manager and ecosystem discoverability

First establish whether this project publishes a package. Installation dependencies alone are not proof. Look for actual package identity, correct registry links, and supported installation commands. If relevant and accessible, compare the linked published package metadata with the page; otherwise label it not inspected.

Registry behaviour is not uniform:

- **npm website search** documents package title, description, README and keywords as inputs. This is not a claim about every npm client or registry implementation.
- **PyPI** has separate short-description, long-description, keyword and classifier metadata. The README is commonly submitted as long description. Do not assume search weighting or automatic scraping of the live GitHub page.
- **crates.io** uses Cargo metadata including description, keywords, categories and a published README. Cargo documents keywords as helping search; do not assert README-body search without evidence.
- **NuGet** documents package ID/title/description/tags search fields and separately supports embedded README display. README display is not proof of full-body indexing.

Updating a GitHub README does not necessarily update the published package. Mention actual ecosystem and language names where they help readers understand the project; do not add irrelevant registry names for search exposure. Do not recommend publishing to every ecosystem.

## 5. Social-share preview

Inspect the **repository root's actual HTML metadata**, including `og:title`, `og:description`, `og:image`, available image dimensions, `twitter:card` and image overrides. A Markdown banner is separate from GitHub's configured Social preview. Do not recommend putting `<meta>` tags in the README to control GitHub's document head.

GitHub provides generated repository previews and allows a separately uploaded custom image. Do not assume preview text is extracted from the README. The script reads actual tags and technically fetches an image only from a bounded allowlist of GitHub image hosts, without credentials. It reports observed type/size/dimensions separately from visual assessment.

Where the host can view the actual image, assess: identifiable project; concise useful purpose; readable text at small sizes; representative imagery; adequate contrast; cropping margins; consistency with the page; outdated or unsupported claims. Mark visuals not inspected if they cannot be viewed. A default generated image may be adequate; recommend a custom image only for a clear improvement.

GitHub's **custom-upload** guidance: PNG, JPG or GIF under 1 MB; at least 640×320 pixels, with 1280×640 recommended for best display. Do not automatically fail a GitHub-generated card for differing from custom-upload guidance.

If a custom image would help, give a small brief: actual project name, factual purpose, relevant visual, suggested dimensions, and “Repository Settings → Social preview.” Do not create/upload the image unless separately requested.

Social clients differ and cache previews. Inspecting metadata is not testing an actual platform card or measuring CTR. Hacker News' standard listing is text-based. Never post a link to test it. If fetching is blocked, report not inspected and continue the audit.

## Sources

Mechanisms checked on 2026-11-02. Recheck official sources if relying on changed behaviour or uncertain details; do not turn a routine audit into repeating all this research.

- [GitHub repository search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
- [GitHub topics and limits](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
- [GitHub section links](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links)
- [Google sitelinks](https://developers.google.com/search/docs/appearance/sitelinks)
- [Google search visual elements](https://developers.google.com/search/docs/appearance/visual-elements-gallery)
- [Google image guidance](https://developers.google.com/search/docs/appearance/google-images)
- [npm website search](https://docs.npmjs.com/searching-for-and-choosing-packages-to-download/)
- [PyPI descriptions](https://docs.pypi.org/project-management/project-descriptions/)
- [Cargo metadata](https://doc.rust-lang.org/cargo/reference/manifest.html)
- [NuGet search](https://learn.microsoft.com/en-us/nuget/api/search-query-service-resource)
- [GitHub social preview settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [GitHub generated Open Graph system](https://github.blog/open-source/git/framework-building-open-graph-images/)
