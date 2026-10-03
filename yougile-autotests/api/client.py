"""Small typed client for the YouGile REST API v2."""

from __future__ import annotations

from typing import Any

import requests


class YouGileApiClient:
    """HTTP client that keeps the base URL and common headers in one place."""

    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def post(self, path: str, payload: dict[str, Any]) -> requests.Response:
        """Send POST request with a JSON body."""
        return self.session.post(
            f"{self.base_url}{path}",
            json=payload,
            timeout=20,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> requests.Response:
        """Send GET request."""
        return self.session.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=20,
        )

    def delete(self, path: str) -> requests.Response:
        """Send DELETE request."""
        return self.session.delete(f"{self.base_url}{path}", timeout=20)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()
