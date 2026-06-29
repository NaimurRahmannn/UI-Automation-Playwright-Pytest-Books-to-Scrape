import pytest

from pages.home_page import HomePage


@pytest.mark.links
class TestBrokenLinks:

    def test_no_broken_links(self, page):
        home = HomePage(page)
        home.load()

        urls = home.get_all_link_hrefs()
        urls = sorted(set(urls))

        assert len(urls) > 0, "No links found on homepage"

        broken = []

        for url in urls:
            try:
                response = page.context.request.get(
                    url,
                    timeout=15000,
                    ignore_https_errors=True
                )

                if response.status != 200:
                    broken.append((url, response.status))

            except Exception as exc:
                broken.append((url, f"error: {exc}"))

        assert not broken, f"Broken links found: {broken}"