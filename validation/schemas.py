"""Pydantic models used to validate jobs at the transform boundary.

Nothing reaches the load step (and therefore the database) without first
passing through CleanedJob's validation rules.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class CleanedJob(BaseModel):
    external_id: str
    title: str
    company_name: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    posted_at: Optional[datetime] = None
    skills: list[str] = []

    @field_validator("external_id", "title", "company_name")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("must not be blank")
        return value.strip()

    @field_validator("location", "employment_type")
    @classmethod
    def empty_string_to_none(cls, value):
        if value is None:
            return None
        value = value.strip()
        return value or None
