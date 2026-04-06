from urllib.parse import urljoin

from bs4 import BeautifulSoup


SUMMARY_SELECTORS = [
    "div.NodeDetail-mainContent p",
    "div.article_body p",
    "article p",
    "section p",
]


def extract_feed_items(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    seen = set()

    for anchor in soup.select("a[href]"):
        href = urljoin(base_url, anchor.get("href", ""))
        title = anchor.get_text(" ", strip=True)
        if not href or not title or len(title) < 25:
            continue
        if "elespectador.com" not in href:
            continue
        if "/tags/" in href or href.endswith("/archivo/judicial/"):
            continue
        if href in seen:
            continue
        seen.add(href)
        items.append({"title": title, "link": href, "summary": ""})

    return items


def extract_summary(html):
    soup = BeautifulSoup(html, "html.parser")

    meta_description = soup.find("meta", attrs={"property": "og:description"})
    if meta_description and meta_description.get("content"):
        return meta_description["content"]

    twitter_description = soup.find("meta", attrs={"name": "twitter:description"})
    if twitter_description and twitter_description.get("content"):
        return twitter_description["content"]

    for selector in SUMMARY_SELECTORS:
        paragraphs = soup.select(selector)
        if paragraphs:
            texts = [paragraph.get_text(" ", strip=True) for paragraph in paragraphs[:2]]
            return " ".join(texts).strip()

    return ""
