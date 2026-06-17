"""Transform layer: cleans, normalizes, and validates raw postings, and
extracts a skill list from free-text job descriptions."""

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import ValidationError

from utils.logger import get_logger
from validation.schemas import CleanedJob

logger = get_logger(__name__)

KNOWN_SKILLS = [
    "Python", "SQL", "Git", "Docker", "AWS", "PySpark", "JavaScript",
    "React", "Excel", "ML", "LLM", "Linux", "Kubernetes", "Java",
    "Spark", "Airflow", "GCP", "Azure", "Terraform", "Pandas",
]


class JobTransformer:
    def transform(self, raw_job: dict[str, Any]) -> Optional[CleanedJob]:
        try:
            cleaned = CleanedJob(
                external_id=str(raw_job.get("job_id", "")),
                title=raw_job.get("job_title", ""),
                company_name=raw_job.get("employer_name", ""),
                location=self._build_location(raw_job),
                employment_type=raw_job.get("job_employment_type"),
                description=raw_job.get("job_description"),
                posted_at=self._parse_posted_at(raw_job),
                skills=self._extract_skills(raw_job.get("job_description", "")),
            )
        except ValidationError as exc:
            logger.warning("Validation failed for raw job %s: %s", raw_job.get("job_id"), exc)
            return None
        return cleaned

    def transform_many(self, raw_jobs: list[dict[str, Any]]) -> list[CleanedJob]:
        cleaned_jobs = []
        for raw_job in raw_jobs:
            cleaned = self.transform(raw_job)
            if cleaned is not None:
                cleaned_jobs.append(cleaned)
        logger.info("Transformed %s/%s raw jobs successfully", len(cleaned_jobs), len(raw_jobs))
        return cleaned_jobs

    @staticmethod
    def _build_location(raw_job: dict[str, Any]) -> Optional[str]:
        if raw_job.get("job_is_remote"):
            return "Remote"
        city = raw_job.get("job_city")
        country = raw_job.get("job_country")
        parts = [part for part in (city, country) if part]
        return ", ".join(parts) if parts else None

    @staticmethod
    def _parse_posted_at(raw_job: dict[str, Any]) -> Optional[datetime]:
        timestamp = raw_job.get("job_posted_at_timestamp")
        if timestamp is None:
            return None
        try:
            return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _extract_skills(description: Optional[str]) -> list[str]:
        if not description:
            return []
        text_lower = description.lower()
        return [skill for skill in KNOWN_SKILLS if skill.lower() in text_lower]
