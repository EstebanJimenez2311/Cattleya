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


def _parse_sitemap_entries(xml_text):
    root = ET.fromstring(xml_text)
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
        lastmod = node.find("sm:lastmod", ns)

        if loc is None:
            continue

        items.append(
            SimpleNamespace(
                title=" ".join("".join(title.itertext()).split()) if title is not None else "",
                link=" ".join("".join(loc.itertext()).split()),
                summary=" ".join("".join(keywords.itertext()).split()) if keywords is not None else "",
                published=" ".join("".join(publication_date.itertext()).split())
                if publication_date is not None
                else " ".join("".join(lastmod.itertext()).split()) if lastmod is not None else "",
            )
        )

    return items


def _parse_sitemap_index(xml_text):
    root = ET.fromstring(xml_text)
    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    }
    items = []

    for node in root.findall("sm:sitemap", ns):
        loc = node.find("sm:loc", ns)
        if loc is None:
            continue
        items.append(" ".join("".join(loc.itertext()).split()))

    return items


def read_sitemap_url(url, timeout=20):
    response = _fetch(url, timeout)
    return _parse_sitemap_entries(response.text)


def read_sitemap_index_url(url, timeout=20):
    response = _fetch(url, timeout)
    return _parse_sitemap_index(response.text)


def _read_sitemap(source_config, timeout):
    return read_sitemap_url(source_config.feed_url, timeout)


def read_feed(source_config, timeout=20):
    if source_config.feed_mode == "sitemap":
        return _read_sitemap(source_config, timeout)
    if source_config.feed_mode == "html":
        return _read_html_listing(source_config, timeout)
    return _read_rss(source_config, timeout)
