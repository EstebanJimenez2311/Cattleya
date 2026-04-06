from types import SimpleNamespace

from django.test import SimpleTestCase

from noticias.management.commands.backfill_noticias import month_range
from noticias.services.rss_reader import _parse_sitemap_entries


class SitemapReaderTests(SimpleTestCase):
    def test_parse_sitemap_entries_supports_plain_lastmod_entries(self):
        xml_text = """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url>
            <loc>https://example.com/articulo</loc>
            <lastmod>2020-01-15T12:00:00-05:00</lastmod>
          </url>
        </urlset>
        """

        entries = _parse_sitemap_entries(xml_text)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].link, "https://example.com/articulo")
        self.assertEqual(entries[0].title, "")
        self.assertEqual(entries[0].published, "2020-01-15T12:00:00-05:00")


class BackfillCommandHelperTests(SimpleTestCase):
    def test_month_range_starts_from_requested_year_and_reaches_current_month(self):
        months = list(month_range(2020))

        self.assertEqual(months[0], (2020, 1))
        self.assertGreaterEqual(len(months), 12)
