

import pytest

from pages.home_page import HomePage
from utils.config import Config


@pytest.mark.homepage
class TestHomepage:

    def test_url_is_correct(self, page):
        home = HomePage(page)
        home.load()
        assert home.get_url() == Config.BASE_URL

    def test_title_matches_expected(self, page):
        home = HomePage(page)
        home.load()
        assert home.get_title() == Config.EXPECTED_TITLE

    def test_all_headings_visible_and_non_empty(self, page):
        home = HomePage(page)
        home.load()

        headings = home.get_all_headings()
        count = headings.count()
        assert count > 0, "No headings found on the page"

        for i in range(count):
            heading = headings.nth(i)
            assert heading.is_visible(), f"Heading {i} is not visible"
            text = heading.inner_text().strip()
            assert text != "", f"Heading {i} has empty text"

    def test_books_section_visible(self, page):
        home = HomePage(page)
        home.load()
        assert home.is_books_section_visible()

    def test_book_list_not_empty(self, page):
        home = HomePage(page)
        home.load()
        assert home.get_book_count() > 0