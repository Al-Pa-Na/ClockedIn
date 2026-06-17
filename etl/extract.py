"""Extraction layer: pulls raw postings from the JSearch API."""

from typing import Any

import requests

from config.settings import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)


class JSearchExtractor:
    def __init__(self):
        settings = get_settings()
        self.base_url = settings.jsearch_base_url
        self.headers = {
            "X-RapidAPI-Key": settings.jsearch_api_key,
            "X-RapidAPI-Host": settings.jsearch_api_host,
        }

    def fetch_jobs(self, query: str, num_pages: int = 1) -> list[dict[str, Any]]:
        """Fetch raw job postings for a search query across N pages."""
        raw_jobs: list[dict[str, Any]] = []

        for page in range(1, num_pages + 1):
            params = {"query": query, "page": page, "num_pages": "1"}
            try:
                response = requests.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=params,
                    timeout=30,
                )
                response.raise_for_status()
            except requests.RequestException as exc:
                logger.error("JSearch request failed (page %s): %s", page, exc)
                continue

            payload = response.json()
            jobs = payload.get("data", [])
            logger.info("Fetched %s raw jobs for query='%s' page=%s", len(jobs), query, page)
            raw_jobs.extend(jobs)

        return raw_jobs
