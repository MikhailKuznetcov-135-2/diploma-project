"""Independent UI tests for three key YouGile functions."""

from __future__ import annotations

from uuid import uuid4

import allure
import pytest
from playwright.sync_api import Page

from config import Config
from ui.pages.board_page import BoardPage
from ui.pages.login_page import LoginPage
from ui.pages.projects_page import ProjectsPage


def _unique(prefix: str) -> str:
    return f"{prefix} {uuid4().hex[:8]}"


def _create_project(page: Page, config: Config) -> tuple[ProjectsPage, str]:
    projects = ProjectsPage(page, config.web_base_url)
    projects.open()
    title = _unique("Диплом UI")
    projects.create_project(title)
    projects.expect_project_visible(title)
    projects.open_project(title)
    return projects, title


@pytest.mark.ui
@allure.epic("YouGile")
@allure.feature("Web UI")
class TestYouGileUi:
    """Five isolated positive UI scenarios."""

    @allure.title("Вход по валидным логину и паролю")
    @allure.story("Авторизация")
    def test_login(self, page: Page, config: Config) -> None:
        login = LoginPage(page, config.web_base_url)
        with allure.step("Открыть страницу входа и авторизоваться"):
            login.open()
            login.login(config.email, config.password)
        with allure.step("Проверить, что форма входа скрылась"):
            login.expect_logged_in()
            login.attach_screenshot("Авторизованный пользователь")

    @allure.title("Открытие раздела проектов")
    @allure.story("Проекты")
    def test_open_projects(self, logged_in_page: Page, config: Config) -> None:
        projects = ProjectsPage(logged_in_page, config.web_base_url)
        with allure.step("Открыть веб-клиент"):
            projects.open()
        with allure.step("Проверить область проектов"):
            projects.expect_projects_area()
            projects.attach_screenshot("Раздел проектов")

    @allure.title("Создание проекта")
    @allure.story("Проекты")
    def test_create_project(self, logged_in_page: Page, config: Config) -> None:
        projects = ProjectsPage(logged_in_page, config.web_base_url)
        title = _unique("Диплом проект")
        with allure.step("Создать проект с уникальным названием"):
            projects.open()
            projects.create_project(title)
        with allure.step("Проверить новый проект в интерфейсе"):
            projects.expect_project_visible(title)
            projects.attach_screenshot("Созданный проект")

    @allure.title("Создание задачи на доске")
    @allure.story("Задачи")
    def test_create_task(self, logged_in_page: Page, config: Config) -> None:
        with allure.step("Создать и открыть отдельный тестовый проект"):
            _create_project(logged_in_page, config)
        board = BoardPage(logged_in_page, config.web_base_url)
        task_title = _unique("Диплом задача")
        with allure.step("Создать задачу"):
            board.create_task(task_title)
        with allure.step("Проверить задачу на доске"):
            board.expect_task_visible(task_title)
            board.attach_screenshot("Созданная задача")

    @allure.title("Редактирование названия задачи")
    @allure.story("Задачи")
    def test_rename_task(self, logged_in_page: Page, config: Config) -> None:
        with allure.step("Создать и открыть отдельный тестовый проект"):
            _create_project(logged_in_page, config)
        board = BoardPage(logged_in_page, config.web_base_url)
        old_title = _unique("До изменения")
        new_title = _unique("После изменения")
        with allure.step("Создать задачу и изменить её название"):
            board.create_task(old_title)
            board.rename_task(old_title, new_title)
        with allure.step("Проверить новое название"):
            board.expect_task_visible(new_title)
            board.attach_screenshot("Переименованная задача")
