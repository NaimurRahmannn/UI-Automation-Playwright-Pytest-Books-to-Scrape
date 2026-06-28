
import random

import pytest

from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage
from utils.config import Config


@pytest.mark.navigation
class TestBookNavigation:

    def test_random_books_open_correct_details_page(self, page):
        home = HomePage(page)
        home.load()

        total_books = home.get_book_count()
        assert total_books > 0, "No books found on homepage"

        # Randomly pick N unique book indexes from the page
        sample_size = min(Config.RANDOM_BOOK_SAMPLE_SIZE, total_books)
        selected_indexes = random.sample(range(total_books), sample_size)

        for index in selected_indexes:
            expected_title = home.get_book_full_title(index)
            assert expected_title != "", f"Book {index} has no title attribute"

            home.open_book(index)

            details = BookDetailsPage(page)
            actual_title = details.get_title_text()

            assert actual_title == expected_title, (
                f"Title mismatch: expected '{expected_title}', "
                f"got '{actual_title}'"
            )
            assert details.is_info_visible(), "Product info not visible"
            page.go_back(wait_until="domcontentloaded")