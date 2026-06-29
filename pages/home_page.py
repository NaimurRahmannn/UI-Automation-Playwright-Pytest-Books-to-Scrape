from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    BOOK_ITEM = "article.product_pod"
    HEADINGS = "h1, h2, h3, h4, h5, h6"
    BOOKS_CONTAINER = "section"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> None:
        self.navigate(Config.BASE_URL)

    def get_book_count(self) -> int:
        return self.page.locator(self.BOOK_ITEM).count()

    def is_books_section_visible(self) -> bool:
        return self.page.locator(self.BOOKS_CONTAINER).first.is_visible()

    def get_all_headings(self):
        return self.page.locator(self.HEADINGS)

    # --- Book-link helpers  ---
    BOOK_LINK = "article.product_pod h3 a"

    def get_book_links(self):
        return self.page.locator(self.BOOK_LINK)

    def get_book_full_title(self, index: int) -> str:
        link = self.get_book_links().nth(index)
        return (link.get_attribute("title") or "").strip()

    def open_book(self, index: int) -> None:
        self.get_book_links().nth(index).click()

    BOOK_PRICE = "article.product_pod p.price_color"

    def get_book_price(self, index: int) -> str:
        """return  book price text from the homepage"""
        return self.page.locator(self.BOOK_PRICE).nth(index).inner_text().strip()

    ALL_LINKS = "a"

    def get_all_link_hrefs(self) -> list[str]:
        """return all absolute, de-duplicated href URLs on the page"""
        from urllib.parse import urljoin

        anchors = self.page.locator(self.ALL_LINKS)
        count = anchors.count()

        urls = set()
        for i in range(count):
            href = anchors.nth(i).get_attribute("href")
            if not href:
                continue
            href = href.strip()
            if href.startswith("#") or href.lower().startswith("javascript:"):
                continue
            absolute = urljoin(self.get_url(), href)
            urls.add(absolute)

        return sorted(urls)
