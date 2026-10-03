"""Base Page Object helpers."""

from __future__ import annotations

import allure
from playwright.sync_api import (
    Locator,
    Page,
    expect,
)
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)


class BasePage:
    """Common browser actions with Playwright auto-waits."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open_path(self, path: str) -> None:
        """Open an application path and wait for the DOM."""
        self.page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded")

    def first_visible(self, *locators: Locator) -> Locator:
        """Wait for and return the first visible locator from documented fallbacks."""
        for locator in locators:
            try:
                locator.first.wait_for(state="visible", timeout=5_000)
                return locator.first
            except PlaywrightTimeoutError:
                continue
        raise AssertionError("Подходящий видимый элемент интерфейса не найден")

    def attach_screenshot(self, name: str) -> None:
        """Attach a full-page screenshot to Allure."""
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    def expect_visible(self, locator: Locator) -> None:
        """Assert that an element is visible."""
        expect(locator).to_be_visible()
