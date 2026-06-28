"""Base page object — parent class"""

from playwright.sync_api import Page

from utils.config import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Return current page's title text."""
        return self.page.title()

    def get_url(self) -> str:
        """Return current page URL."""
        return self.page.url