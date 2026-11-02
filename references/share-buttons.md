# Share Button Generator

An optional output within Discoverability, invoked on request. Use Shields.io SVG images wrapped in Markdown links. GitHub supports linked images without JavaScript; Shields' `link` option alone does not make an embedded Markdown image clickable.

## Generate

```bash
python3 scripts/share_buttons.py --repo OWNER/REPO --title "Project name — factual purpose"
python3 scripts/share_buttons.py --repo OWNER/REPO --title "Project name — factual purpose" --platforms reddit,x,hackernews --format json
python3 scripts/share_buttons.py --repo OWNER/REPO --title "Project name — factual purpose" --discord-url https://discord.gg/ACTUAL-CODE
```

Resolve the actual repository identity from the audit; never return placeholders as finished assets. Derive a factual title from supported page content. The examples above are invocation templates, not real project destinations. Do not claim logo or sharing-form availability unless checked. The script intentionally performs no network requests.

Default: Reddit and X, `flat-square`, compact Markdown row, descriptive alt text. Hacker News is available explicitly; its submit page is text-based and its community submission expectations still apply. Return the generated code block and suggest a “Share this project” row after the useful introduction or near the end. Keep the getting-started path prominent.

**Discord is a community invitation**, not a general share composer. Add it only when a real project invite is supplied or documented. The tool validates URL shape but cannot establish that an invite is active. Keep it under a separate Community label.

## Encoding and compatibility

- Escape each platform query value separately, exactly once, using URL encoding. Keep the canonical repository URL distinct from human-readable share text.
- Shields label/message escaping: `_` represents a space; `__` preserves an underscore; `--` preserves a hyphen. Escape literal underscores and hyphens before URL encoding.
- Use plain hex colours in the badge path, e.g. `000000`, `ff4500`, `5865F2`.
- Use the external Markdown link as the click target: `[![Descriptive alt](BADGE_URL)](SHARE_URL)`.
- Validate current logo availability through the actual image when host tools allow. `--no-logos` generates text-only badges if a logo is unavailable. Simple Icons support can change.
- Plain Markdown is the default. Do not generate script widgets, `onclick`, embedded iframes, or copy-to-clipboard JavaScript. Same-line badges can wrap naturally on narrow screens.
- Sharing forms may require login and the reader's final submission. Do not open/post to test. An HTTP success or login redirect does not prove the prefilled form works.

Missing share buttons are an optional opportunity, not a failure. Do not claim buttons improve GitHub search ranking, create backlinks automatically, or guarantee reach. They give an interested visitor a way to share.

Sources: [Shields badge syntax](https://shields.io/badges), [Shields logos](https://shields.io/docs/logos), [GitHub Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
