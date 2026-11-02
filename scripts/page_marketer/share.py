"""Generate linked badges; never visit sharing destinations or submit posts."""

from urllib.parse import quote, urlencode, urlsplit

from .github import parse_repository


PLATFORMS = {
    "reddit": {"name": "Reddit", "color": "ff4500", "logo": "reddit"},
    "x": {"name": "X", "color": "000000", "logo": "x"},
    "hackernews": {"name": "Hacker News", "color": "ff6600", "logo": "ycombinator"},
}
STYLES = {"flat", "flat-square", "plastic", "for-the-badge", "social"}


def badge_text(text):
    # Apply Shields escaping before percent encoding (hyphens are URL-unreserved).
    return quote(text.replace("_", "__").replace("-", "--"), safe="")


def badge(label, message, color, logo, style="flat-square", use_logo=True):
    if style not in STYLES:
        raise ValueError("Unsupported Shields badge style")
    options = {"style": style}
    if use_logo:
        options.update(logo=logo, logoColor="white")
    return f"https://img.shields.io/badge/{badge_text(label)}-{badge_text(message)}-{color}?" + urlencode(options)


def _markdown_image(alt, image_url, destination):
    alt = alt.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    return f"[![{alt}]({image_url})]({destination})"


def generate(repository, title, platforms=("reddit", "x"), *, style="flat-square", discord_url=None, use_logo=True):
    repo = parse_repository(repository)
    canonical = "https://github.com/" + repo
    title = title.strip()
    if not title or len(title) > 240 or any(ord(char) < 32 for char in title):
        raise ValueError("Use a factual single-line title between 1 and 240 characters")
    platforms = list(dict.fromkeys(platforms))
    if not platforms or any(platform not in PLATFORMS for platform in platforms):
        raise ValueError("Choose at least one of: reddit, x, hackernews")
    buttons = []
    for platform in platforms:
        details = PLATFORMS[platform]
        if platform == "reddit":
            target = "https://www.reddit.com/submit?" + urlencode({"url": canonical, "title": title}, quote_via=quote)
        elif platform == "x":
            target = "https://twitter.com/intent/tweet?" + urlencode({"text": title, "url": canonical}, quote_via=quote)
        else:
            target = "https://news.ycombinator.com/submitlink?" + urlencode({"u": canonical, "t": title}, quote_via=quote)
        buttons.append(_markdown_image("Share on " + details["name"], badge("Share on", details["name"], details["color"], details["logo"], style, use_logo), target))
    result = {"repository_url": canonical, "title": title, "share_markdown": " ".join(buttons), "community_markdown": None, "placement": "A compact Share this project row after the useful introduction or near the end; keep the primary getting-started route prominent.", "validation": "URLs constructed and encoded; destinations, logos and platform login flows have not been contacted or verified."}
    if discord_url:
        parts = urlsplit(discord_url)
        valid = parts.scheme == "https" and not parts.username and not parts.password and parts.port in (None, 443) and not parts.query and not parts.fragment
        valid = valid and ((parts.hostname == "discord.gg" and bool(parts.path.strip("/"))) or (parts.hostname == "discord.com" and parts.path.startswith("/invite/") and bool(parts.path[len("/invite/"):].strip("/"))))
        if not valid:
            raise ValueError("Provide an actual HTTPS discord.gg invite or discord.com/invite URL")
        # A supplied invitation is a destination, not an assertion that it is active.
        invite = "https://" + parts.hostname + quote(parts.path, safe="/-_~")
        result["community_markdown"] = _markdown_image("Join Discord", badge("Join us", "Discord", "5865F2", "discord", style, use_logo), invite)
    return result
