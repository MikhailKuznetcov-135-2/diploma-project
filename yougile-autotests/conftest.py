"""Shared pytest fixtures for API and UI tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from api.client import YouGileApiClient
from config import Config, load_config
from ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def config() -> Config:
    """Load validated settings once per test session."""
    return load_config()


def _company_id(client: YouGileApiClient, config: Config) -> str:
    if config.company_id:
        return config.company_id
    response = client.post(
        "/api-v2/auth/companies",
        {"login": config.email, "password": config.password},
    )
    response.raise_for_status()
    companies = response.json().get("content", [])
    if not companies:
        raise RuntimeError("В ответе YouGile нет доступных компаний")
    return str(companies[0]["id"])


@pytest.fixture(scope="session")
def credentials_client(config: Config) -> Generator[YouGileApiClient, None, None]:
    """Provide an unauthenticated API client for auth endpoint tests."""
    client = YouGileApiClient(config.api_base_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def api_token(
    credentials_client: YouGileApiClient,
    config: Config,
) -> Generator[str, None, None]:
    """Use configured token or create a temporary key and delete it after the run."""
    if config.token:
        yield config.token
        return

    company_id = _company_id(credentials_client, config)
    response = credentials_client.post(
        "/api-v2/auth/keys",
        {
            "login": config.email,
            "password": config.password,
            "companyId": company_id,
        },
    )
    response.raise_for_status()
    token = str(response.json()["key"])
    try:
        yield token
    finally:
        credentials_client.delete(f"/api-v2/auth/keys/{token}")


@pytest.fixture(scope="session")
def api_client(config: Config, api_token: str) -> Generator[YouGileApiClient, None, None]:
    """Provide an authenticated API client."""
    client = YouGileApiClient(config.api_base_url, api_token)
    yield client
    client.close()


@pytest.fixture(scope="session")
def browser(config: Config) -> Generator[Browser, None, None]:
    """Launch the selected Playwright browser."""
    with sync_playwright() as playwright:
        selected: Playwright = playwright
        browser_type = getattr(selected, config.browser, None)
        if browser_type is None:
            raise ValueError("browser должен быть chromium, firefox или webkit")
        instance = browser_type.launch(headless=config.headless)
        yield instance
        instance.close()


@pytest.fixture()
def page(browser: Browser, config: Config) -> Generator[Page, None, None]:
    """Create an isolated browser context for every UI test."""
    context: BrowserContext = browser.new_context()
    current_page = context.new_page()
    current_page.set_default_timeout(config.ui_timeout_ms)
    yield current_page
    context.close()


@pytest.fixture()
def logged_in_page(page: Page, config: Config) -> Page:
    """Open a clean session and authenticate before each UI scenario."""
    login_page = LoginPage(page, config.web_base_url)
    login_page.open()
    login_page.login(config.email, config.password)
    login_page.expect_logged_in()
    return page
