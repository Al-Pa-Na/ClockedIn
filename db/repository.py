"""Reusable data-access layer for the real_jobs domain.

Both the ETL load step and the Streamlit dashboard go through this class,
so there is exactly one place that knows the real_jobs / real_job_skills
schema and SQL.
"""

import pandas as pd
from sqlalchemy import text

from db.engine import get_engine
from utils.logger import get_logger

logger = get_logger(__name__)


class JobRepository:
    """Encapsulates all SQL access to real_jobs / real_job_skills."""

    def __init__(self, engine=None):
        self.engine = engine or get_engine()

    # ------------------------------------------------------------------
    # Write path (used by the ETL load step)
    # ------------------------------------------------------------------

    def get_existing_external_ids(self) -> set[str]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT external_id FROM real_jobs")).fetchall()
        return {row[0] for row in rows}

    def upsert_jobs(self, jobs: list[dict]) -> dict:
        """Insert new jobs, skip ones that already exist by external_id.

        Incremental ingestion relies entirely on the UNIQUE constraint on
        real_jobs.external_id plus ON CONFLICT DO NOTHING -- no job is ever
        inserted twice, regardless of how many times a pipeline run overlaps
        with previous ones.
        """
        inserted, skipped = 0, 0
        with self.engine.begin() as conn:
            for job in jobs:
                result = conn.execute(
                    text(
                        """
                        INSERT INTO real_jobs (
                            external_id, title, company_name, location,
                            employment_type, description, posted_at, ingested_at
                        )
                        VALUES (
                            :external_id, :title, :company_name, :location,
                            :employment_type, :description, :posted_at, NOW()
                        )
                        ON CONFLICT (external_id) DO NOTHING
                        RETURNING real_job_id
                        """
                    ),
                    job,
                )
                row = result.fetchone()
                if row is None:
                    skipped += 1
                    continue

                inserted += 1
                real_job_id = row[0]
                for skill in job.get("skills", []):
                    conn.execute(
                        text(
                            """
                            INSERT INTO real_job_skills (real_job_id, skill_name)
                            VALUES (:real_job_id, :skill_name)
                            ON CONFLICT (real_job_id, skill_name) DO NOTHING
                            """
                        ),
                        {"real_job_id": real_job_id, "skill_name": skill},
                    )

        logger.info("Load complete: %s inserted, %s skipped (duplicates)", inserted, skipped)
        return {"inserted": inserted, "skipped": skipped}

    # ------------------------------------------------------------------
    # Read path (used by the dashboard)
    # ------------------------------------------------------------------

    def fetch_summary(self) -> pd.DataFrame:
        query = """
            SELECT
                COUNT(*) AS total_jobs,
                COUNT(DISTINCT company_name) AS unique_companies,
                COUNT(DISTINCT DATE(posted_at)) AS active_days
            FROM real_jobs;
        """
        return pd.read_sql(query, self.engine)

    def fetch_role_distribution(self) -> pd.DataFrame:
        query = """
            SELECT title, COUNT(*) AS total_jobs
            FROM real_jobs
            GROUP BY title
            ORDER BY total_jobs DESC
            LIMIT 20;
        """
        return pd.read_sql(query, self.engine)

    def fetch_company_distribution(self) -> pd.DataFrame:
        query = """
            SELECT company_name, COUNT(*) AS total_jobs
            FROM real_jobs
            GROUP BY company_name
            ORDER BY total_jobs DESC
            LIMIT 15;
        """
        return pd.read_sql(query, self.engine)

    def fetch_location_distribution(self) -> pd.DataFrame:
        query = """
            SELECT location, COUNT(*) AS total_jobs
            FROM real_jobs
            WHERE location IS NOT NULL
            GROUP BY location
            ORDER BY total_jobs DESC
            LIMIT 15;
        """
        return pd.read_sql(query, self.engine)

    def fetch_skill_trend(self) -> pd.DataFrame:
        query = """
            SELECT
                TO_CHAR(DATE_TRUNC('month', rj.posted_at), 'YYYY-MM') AS month,
                rjs.skill_name,
                COUNT(*) AS demand
            FROM real_job_skills rjs
            JOIN real_jobs rj ON rjs.real_job_id = rj.real_job_id
            WHERE rj.posted_at IS NOT NULL
            GROUP BY DATE_TRUNC('month', rj.posted_at), rjs.skill_name
            ORDER BY month;
        """
        return pd.read_sql(query, self.engine)

    def fetch_data_quality(self) -> pd.DataFrame:
        query = """
            SELECT
                COUNT(*) FILTER (WHERE location IS NULL OR location = '') AS missing_locations,
                COUNT(*) FILTER (WHERE posted_at IS NULL) AS missing_posted_at,
                COUNT(*) FILTER (WHERE description IS NULL OR description = '') AS missing_descriptions,
                (
                    SELECT COUNT(*) FROM real_jobs rj
                    LEFT JOIN real_job_skills rjs ON rj.real_job_id = rjs.real_job_id
                    WHERE rjs.real_job_id IS NULL
                ) AS jobs_without_skills
            FROM real_jobs;
        """
        return pd.read_sql(query, self.engine)

    def fetch_recent_jobs(self, limit: int = 200) -> pd.DataFrame:
        query = text(
            """
            SELECT title, company_name, location, employment_type, posted_at, ingested_at
            FROM real_jobs
            ORDER BY posted_at DESC NULLS LAST
            LIMIT :limit;
            """
        )
        return pd.read_sql(query, self.engine, params={"limit": limit})
