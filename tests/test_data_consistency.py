
import random

import pytest

from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage
from utils.config import Config
from utils.helpers import normalize_price

@pytest.mark.consistency
class TestDataConsistency:

    def test_homepage_matches_details_page(self, page):
        home = HomePage(page)
        home.load()

        total_books = home.get_book_count()
        assert total_books > 0, "No books found on homepage"

        sample_size = min(Config.RANDOM_BOOK_SAMPLE_SIZE, total_books)
        selected_indexes = random.sample(range(total_books), sample_size)

        for index in selected_indexes:
            home_title = home.get_book_full_title(index)
            home_price = home.get_book_price(index)

            assert home_title != "", f"Book {index} has no title"
            assert home_price != "", f"Book {index} has no price"

            home.open_book(index)

            details = BookDetailsPage(page)
            details_title = details.get_title_text()
            details_price = details.get_price_text()

            # Title match
            assert details_title == home_title, (
                f"Title mismatch: homepage '{home_title}' "
                f"vs details '{details_title}'"
            )

            # Price match
            assert normalize_price(home_price) == normalize_price(details_price), (
                f"Price mismatch: homepage '{home_price}' "
                f"vs details '{details_price}'"
            )

            page.go_back(wait_until="domcontentloaded")