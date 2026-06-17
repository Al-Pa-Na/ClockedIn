"""CLI entrypoint for running the job ingestion pipeline.

Usage:
    python scripts/run_etl.py --query "software engineer intern in India" --pages 2
"""

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from etl.pipeline import JobIngestionPipeline  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Run ClockedIn job ingestion.")
    parser.add_argument("--query", required=True, help="Search query, e.g. 'software engineer intern in India'")
    parser.add_argument("--pages", type=int, default=1, help="Number of result pages to fetch")
    args = parser.parse_args()

    pipeline = JobIngestionPipeline()
    summary = pipeline.run(args.query, args.pages)
    print(summary)


if __name__ == "__main__":
    main()
