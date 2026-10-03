"""Login page object for the YouGile web application."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Actions available on the public login screen."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def open(self) -> None:
        """Open the web client login page."""
        self.open_path("/team/")

    def login(self, email: str, password: str) -> None:
        """Submit email and password."""
        email_input = self.first_visible(
            self.page.locator('input[type="email"]'),
            self.page.locator("input").nth(0),
        )
        password_input = self.first_visible(
            self.page.locator('input[type="password"]'),
            self.page.locator("input").nth(1),
        )
        email_input.fill(email)
        password_input.fill(password)
        self.page.get_by_role("button", name="Войти", exact=True).click()

    def expect_logged_in(self) -> None:
        """Verify that the authenticated application shell is visible."""
        expect(self.page.locator('[data-testid="left-sidebar"]')).to_be_visible(timeout=30_000)
        expect(self.page.get_by_role("button", name="Войти", exact=True)).not_to_be_visible()
