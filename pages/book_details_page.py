
from playwright.sync_api import Page

from pages.base_page import BasePage


class BookDetailsPage(BasePage):
   
    TITLE_H1 = "h1"
   
    PRICE = "p.price_color"
    PRODUCT_INFO_TABLE = "table.table"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_title_text(self) -> str:
        return self.page.locator(self.TITLE_H1).inner_text().strip()

    def get_price_text(self) -> str:
        return self.page.locator(self.PRICE).first.inner_text().strip()

    def is_info_visible(self) -> bool:
        return self.page.locator(self.PRODUCT_INFO_TABLE).is_visible()