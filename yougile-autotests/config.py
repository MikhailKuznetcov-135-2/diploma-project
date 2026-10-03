"""Configuration loader for the YouGile test project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class Config:
    """Runtime settings loaded from YAML and optional environment overrides."""

    web_base_url: str
    api_base_url: str
    email: str = field(repr=False)
    password: str = field(repr=False)
    company_id: str
    token: str = field(repr=False)
    browser: str
    headless: bool
    ui_timeout_ms: int


def _required_text(data: dict[str, Any], key: str) -> str:
    value = str(data.get(key, "")).strip()
    if not value:
        raise ValueError(f"Заполните обязательный параметр '{key}' в config.yaml")
    return value.rstrip("/")


def load_config(config_path: str | Path = "config.yaml") -> Config:
    """Load settings without logging or exposing secrets."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Файл {path} не найден. Скопируйте config.example.yaml в config.yaml."
        )

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("Корень config.yaml должен быть объектом YAML")

    data: dict[str, Any] = {
        **raw,
        "email": os.getenv("YOUGILE_EMAIL", raw.get("email", "")),
        "password": os.getenv("YOUGILE_PASSWORD", raw.get("password", "")),
        "company_id": os.getenv("YOUGILE_COMPANY_ID", raw.get("company_id", "")),
        "token": os.getenv("YOUGILE_TOKEN", raw.get("token", "")),
        "browser": os.getenv("YOUGILE_BROWSER", raw.get("browser", "chromium")),
    }

    return Config(
        web_base_url=_required_text(data, "web_base_url"),
        api_base_url=_required_text(data, "api_base_url"),
        email=_required_text(data, "email"),
        password=_required_text(data, "password"),
        company_id=str(data.get("company_id", "")).strip(),
        token=str(data.get("token", "")).strip(),
        browser=str(data.get("browser", "chromium")).strip().lower(),
        headless=bool(data.get("headless", True)),
        ui_timeout_ms=int(data.get("ui_timeout_ms", 15_000)),
    )
