from types import SimpleNamespace
from xml.etree import ElementTree as ET

import feedparser
import requests


REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


def _fetch(url, timeout):
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.encoding or "utf-8"
    return response


def _read_rss(source_config, timeout):
    response = _fetch(source_config.feed_url, timeout)
    feed = feedparser.parse(response.content)
    return list(getattr(feed, "entries", []))


def _read_html_listing(source_config, timeout):
    response = _fetch(source_config.feed_url, timeout)
    items = source_config.parser.extract_feed_items(response.text, source_config.base_url)
    return [SimpleNamespace(**item) for item in items]


def _read_sitemap(source_config, timeout):
    response = _fetch(source_config.feed_url, timeout)
    root = ET.fromstring(response.text)
    items = []
    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "news": "http://www.google.com/schemas/sitemap-news/0.9",
    }

    for node in root.findall("sm:url", ns):
        loc = node.find("sm:loc", ns)
        title = node.find("news:news/news:title", ns)
        publication_date = node.find("news:news/news:publication_date", ns)
        keywords = node.find("news:news/news:keywords", ns)

        if loc is None or title is None:
            continue

        items.append(
            SimpleNamespace(
                title=" ".join("".join(title.itertext()).split()),
                link=" ".join("".join(loc.itertext()).split()),
                summary=" ".join("".join(keywords.itertext()).split()) if keywords is not None else "",
                published=" ".join("".join(publication_date.itertext()).split())
                if publication_date is not None
                else "",
            )
        )

    return items


def read_feed(source_config, timeout=20):
    if source_config.feed_mode == "sitemap":
        return _read_sitemap(source_config, timeout)
    if source_config.feed_mode == "html":
        return _read_html_listing(source_config, timeout)
    return _read_rss(source_config, timeout)
