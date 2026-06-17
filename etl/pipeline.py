"""Orchestrates the full extract -> transform -> load pipeline."""

from etl.extract import JSearchExtractor
from etl.load import JobLoader
from etl.transform import JobTransformer
from utils.logger import get_logger

logger = get_logger(__name__)


class JobIngestionPipeline:
    def __init__(self):
        self.extractor = JSearchExtractor()
        self.transformer = JobTransformer()
        self.loader = JobLoader()

    def run(self, query: str, num_pages: int = 1) -> dict:
        logger.info("Starting ingestion run: query='%s' pages=%s", query, num_pages)

        raw_jobs = self.extractor.fetch_jobs(query, num_pages)
        cleaned_jobs = self.transformer.transform_many(raw_jobs)
        result = self.loader.load(cleaned_jobs)

        summary = {
            "query": query,
            "fetched": len(raw_jobs),
            "validated": len(cleaned_jobs),
            "inserted": result["inserted"],
            "skipped_duplicates": result["skipped"],
        }
        logger.info("Ingestion run complete: %s", summary)
        return summary
