"""Project board page object."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage


class BoardPage(BasePage):
    """Actions with tasks on a board."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    def create_task(self, title: str) -> None:
        """Create a task in the first available column."""
        self.page.get_by_role("button", name="Добавить задачу", exact=True).click()
        title_input = self.page.locator('[data-testid="board-task-input-name"]')
        title_input.fill(title)
        self.page.keyboard.press("Enter")
        expect(
            self.page.locator('[data-testid="board-task-title"]').filter(has_text=title)
        ).to_be_visible()

    def rename_task(self, old_title: str, new_title: str) -> None:
        """Open a task card and change its title."""
        task_card = self.page.locator('[data-testid="board-task-card"]').filter(has_text=old_title)
        task_id = task_card.get_attribute("data-task-id")
        if not task_id:
            raise AssertionError("У карточки задачи отсутствует data-task-id")
        stable_task_card = self.page.locator(
            f'[data-testid="board-task-card"][data-task-id="{task_id}"]'
        )
        task_card.hover()
        task_card.locator('[data-testid="board-task-pancel"]').click()
        title_input = stable_task_card.locator('[data-testid="board-task-title"] textarea')
        title_input.fill(new_title)
        self.page.keyboard.press("Enter")
        expect(
            stable_task_card.locator('[data-testid="board-task-title"]').filter(has_text=new_title)
        ).to_be_visible()

    def move_task_to_next_column(self, title: str) -> None:
        """Drag a task to the second board column."""
        task = self.page.get_by_text(title, exact=True)
        columns = self.page.locator('[data-testid="board-column"], .column')
        if columns.count() < 2:
            raise AssertionError("Для перемещения нужны минимум две колонки")
        task.drag_to(columns.nth(1))

    def expect_task_visible(self, title: str) -> None:
        """Verify that a task title is shown on the board."""
        expect(
            self.page.locator('[data-testid="board-task-title"]').filter(has_text=title)
        ).to_be_visible()
