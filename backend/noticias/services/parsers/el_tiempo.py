from bs4 import BeautifulSoup


SUMMARY_SELECTORS = [
    "div.article__body p",
    "div.paragraph p",
    "article p",
    "section p",
]


def extract_summary(html):
    soup = BeautifulSoup(html, "html.parser")

    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description.get("content"):
        return meta_description["content"]

    og_description = soup.find("meta", attrs={"property": "og:description"})
    if og_description and og_description.get("content"):
        return og_description["content"]

    for selector in SUMMARY_SELECTORS:
        paragraphs = soup.select(selector)
        if paragraphs:
            texts = [paragraph.get_text(" ", strip=True) for paragraph in paragraphs[:2]]
            return " ".join(texts).strip()

    return ""

