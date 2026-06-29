

import pytest

from pages.home_page import HomePage
from utils.config import Config


@pytest.mark.images
class TestProductImages:

    def _validate_images_on_page(self, home: HomePage, page_number: int):
        """Run all the image and checks for every image on the current page"""
        images = home.get_images()
        count = images.count()
        assert count > 0, f"No images found on page {page_number}"

        for i in range(count):
            img = images.nth(i)
            assert img.is_visible(), (
                f"Image {i} on page {page_number} is not visible"
            )
            src = img.get_attribute("src")
            assert src and src.strip() != "", (
                f"Image {i} on page {page_number} has empty src"
            )
            
            alt = img.get_attribute("alt")
            assert alt and alt.strip() != "", (
                f"Image {i} on page {page_number} has empty alt"
            )

            css_class = img.get_attribute("class") or ""
            assert "thumbnail" in css_class, (
                f"Image {i} on page {page_number} missing 'thumbnail' class"
            )

    def test_product_images_across_pages(self, page):
        home = HomePage(page)
        home.load()

        pages_visited = 0

        while pages_visited < Config.MAX_IMAGE_PAGES:
            pages_visited += 1
            self._validate_images_on_page(home, pages_visited)

            if not home.has_next_page():
                break

            home.go_to_next_page()

        assert pages_visited >= 1