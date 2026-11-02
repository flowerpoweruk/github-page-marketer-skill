"""Conservative Markdown inventory; no evaluation or execution of repository code."""

import html
from html.parser import HTMLParser
import re
import unicodedata
from urllib.parse import unquote, urlsplit


def clean_inline(text):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(re.sub(r"[*`~]", "", text)).strip()


def heading_slug(text):
    """Approximate GitHub's documented section-anchor rules, preserving Unicode."""
    text = clean_inline(text).lower()
    return "".join(
        char for char in text
        if char in " -_" or unicodedata.category(char)[0] in "LNM"
    ).replace(" ", "-")


def _without_comments(text):
    return re.sub(r"<!--[\s\S]*?(?:-->|$)", lambda m: "\n" * m[0].count("\n"), text)


def _visible_lines(text):
    lines = _without_comments(text).splitlines()
    visible, blocks = [], []
    fence = None
    for index, line in enumerate(lines, 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                blocks[-1]["end_line"] = index
                blocks[-1]["closed"] = True
                fence = None
            else:
                blocks[-1]["content"] += line + "\n"
            visible.append("")
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            blocks.append({"line": index, "language": marker[2].strip(), "content": "", "closed": False})
            visible.append("")
        else:
            visible.append(line)
    return visible, blocks


def _target(text):
    text = text.strip()
    if text.startswith("<") and ">" in text:
        return text[1:text.index(">")]
    # Optional Markdown link titles follow whitespace; spaces in URLs should be encoded.
    return re.split(r"\s+[\"']", text, maxsplit=1)[0].strip()


def _inline_links(line):
    """Extract link/image targets, including balanced parentheses in URLs."""
    line = re.sub(r"(`+).*?\1", "", line)
    for match in re.finditer(r"(!?)\[([^\[\]\n]*)\]\(", line):
        depth, cursor = 1, match.end()
        start = cursor
        while cursor < len(line):
            if line[cursor] == "\\":
                cursor += 2
                continue
            if line[cursor] == "(":
                depth += 1
            elif line[cursor] == ")":
                depth -= 1
                if depth == 0:
                    yield {"kind": "image" if match[1] else "link", "label": match[2], "url": _target(line[start:cursor])}
                    if match[1] and match.start() > 0 and line[match.start() - 1] == "[" and line[cursor + 1:cursor + 3] == "](":
                        # Common linked-badge syntax: [![alt](image)](destination).
                        rest = line[cursor + 3:]
                        target_depth, end = 1, 0
                        while end < len(rest):
                            if rest[end] == "\\":
                                end += 2
                                continue
                            if rest[end] == "(":
                                target_depth += 1
                            elif rest[end] == ")":
                                target_depth -= 1
                                if target_depth == 0:
                                    yield {"kind": "link", "label": match[2], "url": _target(rest[:end])}
                                    break
                            end += 1
                    break
            cursor += 1


class _HTMLInventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.images = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and attrs.get("src"):
            self.images.append({"kind": "image", "label": attrs.get("alt", ""), "url": attrs["src"], "line": self.getpos()[0]})
        if tag == "a" and attrs.get("href"):
            self.links.append({"kind": "link", "label": attrs.get("aria-label", attrs.get("title", "")), "url": attrs["href"], "line": self.getpos()[0]})


def inventory(text):
    visible, blocks = _visible_lines(text)
    headings, links, images = [], [], []
    used, anchors = set(), set()
    definitions = {}
    for line in visible:
        match = re.match(r"^ {0,3}\[([^\]]+)\]:\s*(.+)$", line)
        if match:
            definitions[match[1].casefold().strip()] = _target(match[2])

    def add_heading(level, title, line_number):
        base = heading_slug(title)
        slug, suffix = base, 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        anchors.add(slug)
        headings.append({"level": level, "text": clean_inline(title), "anchor": slug, "line": line_number})

    for index, line in enumerate(visible, 1):
        match = re.match(r"^ {0,3}(#{1,6})(?:\s+|$)(.*)$", line)
        if match:
            add_heading(len(match[1]), re.sub(r"\s+#+\s*$", "", match[2]), index)
        elif index < len(visible) and line.strip() and not line.startswith(("    ", "\t")):
            underline = re.fullmatch(r" {0,3}(=+|-+)\s*", visible[index])
            if underline and not re.match(r"^\s*[-*>]", line):
                add_heading(1 if underline[1][0] == "=" else 2, line, index)
        for match in re.finditer(r"<h([1-6])\b[^>]*>(.*?)</h\1>", line, re.I):
            add_heading(int(match[1]), match[2], index)
        for match in re.finditer(r"\b(?:id|name)=[\"']([^\"']+)[\"']", line):
            anchors.add(html.unescape(match[1]))
        if line.startswith(("    ", "\t")) or re.match(r"^ {0,3}\[[^\]]+\]:", line):
            continue
        found = list(_inline_links(line))
        # Resolve explicit and collapsed reference links/images.
        masked = re.sub(r"(`+).*?\1", "", line)
        for match in re.finditer(r"(!?)\[([^\]]+)\]\[([^\]]*)\]", masked):
            key = (match[3] or match[2]).strip().casefold()
            if key in definitions:
                found.append({"kind": "image" if match[1] else "link", "label": match[2], "url": definitions[key]})
        for entry in found:
            entry["line"] = index
            (images if entry["kind"] == "image" else links).append(entry)
    html_inventory = _HTMLInventory()
    html_inventory.feed("\n".join("" if line.startswith(("    ", "\t")) else re.sub(r"(`+).*?\1", "", line) for line in visible))
    links.extend(html_inventory.links)
    images.extend(html_inventory.images)
    diagnostics = []
    for entry in links:
        if entry["url"].startswith("#") and unquote(entry["url"][1:]) not in anchors:
            diagnostics.append({"code": "unresolved_section_link", "line": entry["line"], "url": entry["url"], "message": "Fragment did not match a detected anchor; confirm against GitHub's rendered page."})
        scheme = urlsplit(entry["url"]).scheme.lower()
        if scheme and scheme not in {"https", "http", "mailto"}:
            diagnostics.append({"code": "unusual_link_scheme", "line": entry["line"], "url": entry["url"], "message": "Link uses a nonstandard scheme; it was not opened."})
    for entry in images:
        if not entry["label"].strip():
            diagnostics.append({"code": "empty_image_alt", "line": entry["line"], "message": "Image has no Markdown alt text; judge whether it is informative or decorative."})
    for block in blocks:
        if not block["closed"]:
            diagnostics.append({"code": "unclosed_code_fence", "line": block["line"], "message": "Code fence has no detected closing marker."})
    return {
        "line_count": len(text.splitlines()),
        "word_count": len(re.findall(r"\b\w+\b", "\n".join(visible))),
        "headings": headings, "links": links, "images": images,
        "code_blocks": blocks, "diagnostics": diagnostics,
        "anchor_check": "Approximation of GitHub rendering; only same-document fragments checked. No linked URL or command was executed.",
    }
