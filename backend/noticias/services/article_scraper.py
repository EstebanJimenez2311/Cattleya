import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


class ArticleScraper:
    def __init__(self, delay_seconds=1, timeout=15):
        self.delay_seconds = delay_seconds
        self.timeout = timeout
        self.session = requests.Session()

        retries = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch_html(self, url):
        response = self.session.get(url, headers=REQUEST_HEADERS, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.encoding or "utf-8"
        time.sleep(self.delay_seconds)
        return response.text, response.url
