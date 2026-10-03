"""Independent API checks based on the official YouGile REST API v2."""

from __future__ import annotations

import allure
import pytest

from api.client import YouGileApiClient
from config import Config


@pytest.mark.api
@allure.epic("YouGile")
@allure.feature("REST API v2")
class TestYouGileApi:
    """Five positive and two negative API scenarios."""

    @allure.title("Получение списка компаний по валидным учётным данным")
    @allure.story("Авторизация")
    def test_get_companies(
        self,
        credentials_client: YouGileApiClient,
        config: Config,
    ) -> None:
        with allure.step("Запросить список компаний"):
            response = credentials_client.post(
                "/api-v2/auth/companies",
                {"login": config.email, "password": config.password},
            )
        with allure.step("Проверить статус и контракт ответа"):
            assert response.status_code == 200, response.text
            body = response.json()
            assert isinstance(body.get("content"), list)
            assert isinstance(body.get("paging"), dict)

    @allure.title("Создание и удаление временного API-ключа")
    @allure.story("Авторизация")
    def test_create_api_key(
        self,
        credentials_client: YouGileApiClient,
        config: Config,
    ) -> None:
        with allure.step("Определить ID компании"):
            companies_response = credentials_client.post(
                "/api-v2/auth/companies",
                {"login": config.email, "password": config.password},
            )
            assert companies_response.status_code == 200, companies_response.text
            companies = companies_response.json().get("content", [])
            company_id = config.company_id or str(companies[0]["id"])

        created_key = ""
        try:
            with allure.step("Создать API-ключ"):
                response = credentials_client.post(
                    "/api-v2/auth/keys",
                    {
                        "login": config.email,
                        "password": config.password,
                        "companyId": company_id,
                    },
                )
            with allure.step("Проверить статус и наличие ключа"):
                assert response.status_code == 201, response.text
                created_key = str(response.json().get("key", ""))
                assert created_key
        finally:
            if created_key:
                credentials_client.delete(f"/api-v2/auth/keys/{created_key}")

    @allure.title("Получение текущего пользователя с валидным API-ключом")
    @allure.story("Пользователь")
    def test_get_current_user(self, api_client: YouGileApiClient) -> None:
        with allure.step("Запросить текущего пользователя"):
            response = api_client.get("/api-v2/users/me")
        with allure.step("Проверить успешный ответ и ID пользователя"):
            assert response.status_code == 200, response.text
            assert response.json().get("id")

    @allure.title("Получение списка проектов")
    @allure.story("Проекты")
    def test_get_projects(self, api_client: YouGileApiClient) -> None:
        with allure.step("Запросить проекты"):
            response = api_client.get("/api-v2/projects", {"limit": 50, "offset": 0})
        with allure.step("Проверить пагинированный ответ"):
            assert response.status_code == 200, response.text
            body = response.json()
            assert isinstance(body.get("content"), list)
            assert isinstance(body.get("paging"), dict)

    @allure.title("Получение списка задач")
    @allure.story("Задачи")
    def test_get_tasks(self, api_client: YouGileApiClient) -> None:
        with allure.step("Запросить задачи"):
            response = api_client.get("/api-v2/tasks", {"limit": 50, "offset": 0})
        with allure.step("Проверить пагинированный ответ"):
            assert response.status_code == 200, response.text
            body = response.json()
            assert isinstance(body.get("content"), list)
            assert isinstance(body.get("paging"), dict)

    @allure.title("Запрос текущего пользователя без API-ключа отклонён")
    @allure.story("Авторизация")
    def test_get_current_user_without_token(
        self,
        credentials_client: YouGileApiClient,
    ) -> None:
        with allure.step("Отправить запрос без Authorization"):
            response = credentials_client.get("/api-v2/users/me")
        with allure.step("Проверить отказ в авторизации"):
            assert response.status_code == 401, response.text
            assert response.json().get("error")

    @allure.title("Запрос проектов с невалидным API-ключом отклонён")
    @allure.story("Авторизация")
    def test_get_projects_with_invalid_token(self, config: Config) -> None:
        invalid_client = YouGileApiClient(config.api_base_url, "invalid-token")
        try:
            with allure.step("Отправить запрос с невалидным Bearer token"):
                response = invalid_client.get("/api-v2/projects")
            with allure.step("Проверить отказ в авторизации"):
                assert response.status_code == 401, response.text
                assert response.json().get("error")
        finally:
            invalid_client.close()
