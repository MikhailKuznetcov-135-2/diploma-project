"""Projects page object."""

from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage


class ProjectsPage(BasePage):
    """High-level project actions."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def open(self) -> None:
        """Open the authenticated web client and select the company projects area."""
        self.open_path("/team/")
        expect(self.page.locator('[data-testid="left-sidebar"]')).to_be_visible(timeout=30_000)
        self.page.locator('[data-testid="my-company-item"]').click()
        expect(self.page.locator('[data-testid="panel-company-projects"]')).to_be_visible(
            timeout=20_000
        )

    def expect_projects_area(self) -> None:
        """Verify that project navigation is available."""
        candidate = self.page.locator('[data-testid="panel-company-projects"]')
        expect(candidate).to_be_visible(timeout=20_000)

    def create_project(self, title: str) -> None:
        """Create a project using visible controls."""
        create_button = self.first_visible(
            self.page.locator('[data-testid="add-project-button"]'),
            self.page.get_by_role("button", name=re.compile("Добавить проект", re.I)),
            self.page.get_by_role("button", name=re.compile("Создать проект", re.I)),
            self.page.locator('[data-testid="create-project"]'),
            self.page.get_by_text("Добавить проект", exact=True),
        )
        create_button.click()
        self.page.get_by_text("Проект с задачами", exact=True).click()
        title_input = self.first_visible(
            self.page.get_by_placeholder(re.compile("назван.*проект", re.I)),
            self.page.locator('input[name="title"]'),
            self.page.get_by_placeholder("Введите название проекта…"),
        )
        title_input.fill(title)
        self.first_visible(
            self.page.get_by_role("button", name="Добавить проект с задачами", exact=True),
            self.page.get_by_role("button", name="Создать", exact=True),
        ).click()

    def open_project(self, title: str) -> None:
        """Open a project by exact visible title."""
        self.page.locator('[data-testid="project-item"]').filter(has_text=title).click()

    def expect_project_visible(self, title: str) -> None:
        """Verify that a project title is shown."""
        expect(
            self.page.locator('[data-testid="project-item"]').filter(has_text=title)
        ).to_be_visible(timeout=20_000)
