"""Bounded, read-only GitHub collection. Credentials never go to image hosts."""

import base64
import json
import os
import re
import struct
import urllib.error
import urllib.request
from urllib.parse import quote, urlsplit

from .discoverability import social_metadata


API_HOSTS = {"api.github.com", "github.com", "raw.githubusercontent.com"}
IMAGE_HOSTS = {"opengraph.githubassets.com", "repository-images.githubusercontent.com", "user-images.githubusercontent.com", "private-user-images.githubusercontent.com", "avatars.githubusercontent.com", "camo.githubusercontent.com"}


class CollectionError(Exception):
    pass


def parse_repository(value):
    value = value.strip()
    if "://" in value:
        parts = urlsplit(value)
        if parts.scheme != "https" or parts.hostname != "github.com" or parts.username or parts.password or parts.port not in (None, 443):
            raise ValueError("Use an HTTPS github.com repository URL or OWNER/REPO")
        value = parts.path.strip("/")
    else:
        value = value.strip("/")
    if value.endswith(".git"):
        value = value[:-4]
    segments = value.split("/")
    if len(segments) != 2 or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", part) or part in {".", ".."} for part in segments):
        raise ValueError("Expected OWNER/REPO or the repository's root URL")
    return "/".join(segments)


def validate_url(url, allowed_hosts):
    try:
        parts = urlsplit(url)
        valid = parts.scheme == "https" and parts.hostname in allowed_hosts and not parts.username and not parts.password and parts.port in (None, 443)
    except ValueError:
        valid = False
    if not valid:
        raise CollectionError("URL is outside the allowed HTTPS GitHub hosts")


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_hosts):
        self.allowed_hosts = allowed_hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl, self.allowed_hosts)
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected:
            redirected.remove_header("Authorization")
        return redirected


def request(url, *, token=None, allowed_hosts=None, limit=2_000_000, timeout=12):
    allowed_hosts = allowed_hosts or API_HOSTS
    validate_url(url, allowed_hosts)
    headers = {"User-Agent": "github-page-marketer/1.0", "Accept-Encoding": "identity"}
    if urlsplit(url).hostname == "api.github.com":
        headers["Accept"] = "application/vnd.github+json"
        if token:
            headers["Authorization"] = f"Bearer {token}"
    opener = urllib.request.build_opener(_SafeRedirect(allowed_hosts))
    try:
        with opener.open(urllib.request.Request(url, headers=headers), timeout=timeout) as response:
            data = response.read(limit + 1)
            if len(data) > limit:
                raise CollectionError("Response exceeds collection size limit")
            return data, response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        raise CollectionError(f"HTTP {error.code}; check access, rate limits or availability") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise CollectionError("Network request failed or timed out; use a connector or offline snapshots") from None


def _json_request(url, token):
    data, _ = request(url, token=token)
    try:
        result = json.loads(data)
    except (ValueError, UnicodeError):
        raise CollectionError("GitHub returned invalid JSON") from None
    if not isinstance(result, dict):
        raise CollectionError("GitHub response was not an object")
    return result


def image_dimensions(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"\xff\xd8"):
        position = 2
        while position + 4 <= len(data):
            if data[position] != 0xFF:
                position += 1
                continue
            while position < len(data) and data[position] == 0xFF:
                position += 1
            if position >= len(data):
                break
            marker = data[position]
            position += 1
            if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if position + 2 > len(data):
                break
            length = int.from_bytes(data[position:position + 2], "big")
            if length < 2 or position + length > len(data):
                break
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF} and length >= 7:
                height, width = struct.unpack(">HH", data[position + 3:position + 7])
                return width, height
            position += length
    return None


def inspect_preview_image(url):
    # Never fetch arbitrary URLs advertised in untrusted HTML, or forward GH_TOKEN.
    try:
        data, content_type = request(url, allowed_hosts=IMAGE_HOSTS, limit=5_000_000)
        if not content_type.lower().startswith("image/"):
            raise CollectionError("Preview endpoint did not return an image content type")
    except CollectionError as error:
        return {"status": "not_inspected", "reason": str(error)}
    dimensions = image_dimensions(data)
    return {
        "status": "observed", "bytes": len(data), "content_type": content_type,
        "width": dimensions[0] if dimensions else None,
        "height": dimensions[1] if dimensions else None,
        "source_kind": "github_generated" if urlsplit(url).hostname == "opengraph.githubassets.com" else "hosted_image_custom_status_unconfirmed",
        "visual_review": "not_inspected",
        "note": "Technical retrieval only. Generated previews need not match custom-upload dimensions. Appearance and actual social-platform rendering require separate inspection.",
    }


def collect(repository):
    repo = parse_repository(repository)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    api = "https://api.github.com/repos/" + repo
    metadata = _json_request(api, token)
    branch = metadata.get("default_branch", "main")
    readme = _json_request(api + "/readme?ref=" + quote(branch, safe=""), token)
    if readme.get("encoding") != "base64" or not isinstance(readme.get("content"), str):
        raise CollectionError("README content is unavailable through the contents API; use a connector or local file")
    try:
        text = base64.b64decode(readme["content"], validate=False).decode("utf-8-sig")
    except (ValueError, UnicodeError):
        raise CollectionError("README was not valid UTF-8 content") from None
    if len(text.encode("utf-8")) > 1_000_000:
        raise CollectionError("README exceeds the 1 MB text limit")
    # Resolve metadata by the actual API identity, accommodating repository renames.
    actual_repo = parse_repository(metadata.get("full_name", repo))
    canonical = "https://github.com/" + actual_repo
    selected = {key: metadata.get(key) for key in ("name", "description", "topics", "language", "default_branch", "archived", "visibility", "homepage")}
    if selected["topics"] is None:
        selected.pop("topics")
    selected["full_name"] = actual_repo
    selected["html_url"] = canonical
    try:
        page, _ = request(canonical, limit=4_000_000)
        social = social_metadata(page.decode("utf-8", errors="replace"))
        if social.get("image_url"):
            social["image_inspection"] = inspect_preview_image(social["image_url"])
    except CollectionError as error:
        social = {"status": "not_inspected", "reason": str(error)}
    return text, selected, social, {"repository_url": canonical, "branch": branch, "readme_path": readme.get("path"), "readme_blob_sha": readme.get("sha"), "mode": "network"}
