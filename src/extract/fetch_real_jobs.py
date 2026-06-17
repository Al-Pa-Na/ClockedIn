import requests
import pandas as pd
from sqlalchemy import create_engine, text

API_KEY = "03373b7f80msh5dd53310871cf90p1ef7aejsn82b624543cfa"

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

SEARCH_TERMS = [
    "data engineer intern india",
    "software engineer intern india",
    "backend intern india",
    "machine learning intern india",
    "data analyst intern india"
]

all_jobs = []

for term in SEARCH_TERMS:

    print(f"Fetching: {term}")

    response = requests.get(
        "https://jsearch.p.rapidapi.com/search",
        headers={
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        },
        params={
            "query": term,
            "page": "1",
            "num_pages": "1"
        }
    )

    if response.status_code != 200:
        print(f"Failed: {term}")
        continue

    jobs = response.json().get("data", [])
    all_jobs.extend(jobs)

df = pd.DataFrame(all_jobs)

if df.empty:
    print("No jobs fetched.")
    exit()

df = df.drop_duplicates(subset=["job_id"])

df = df[
    [
        "job_id",
        "job_title",
        "employer_name",
        "job_location",
        "job_employment_type",
        "job_posted_at_datetime_utc",
        "job_apply_link",
        "job_description"
    ]
].copy()

df.columns = [
    "job_id",
    "title",
    "company_name",
    "location",
    "employment_type",
    "posted_at",
    "apply_link",
    "description"
]

df["source"] = "JSearch"

with engine.begin() as conn:

    existing = pd.read_sql(
        "SELECT job_id FROM real_jobs",
        conn
    )

    if not existing.empty:
        df = df[
            ~df["job_id"].isin(existing["job_id"])
        ]

if df.empty:
    print("No new jobs found.")
    exit()

df.to_sql(
    "real_jobs",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print(f"Inserted {len(df)} new jobs.")