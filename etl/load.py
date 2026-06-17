"""Load layer: writes validated, transformed jobs into the database.

Incremental-ingestion guarantees live in db.repository.JobRepository
(UNIQUE external_id + ON CONFLICT DO NOTHING); this layer just adapts
CleanedJob objects into the dict shape the repository expects.
"""

from typing import Optional

from db.repository import JobRepository
from utils.logger import get_logger
from validation.schemas import CleanedJob

logger = get_logger(__name__)


class JobLoader:
    def __init__(self, repository: Optional[JobRepository] = None):
        self.repository = repository or JobRepository()

    def load(self, jobs: list[CleanedJob]) -> dict:
        if not jobs:
            logger.info("No jobs to load.")
            return {"inserted": 0, "skipped": 0}

        payload = [job.model_dump() for job in jobs]
        return self.repository.upsert_jobs(payload)
