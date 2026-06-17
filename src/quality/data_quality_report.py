import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

checks = {
    "total_jobs": """
        SELECT COUNT(*) FROM jobs;
    """,

    "total_snapshots": """
        SELECT COUNT(*) FROM job_snapshots;
    """,

    "missing_locations": """
        SELECT COUNT(*)
        FROM job_snapshots
        WHERE location IS NULL;
    """,

    "missing_stipends": """
        SELECT COUNT(*)
        FROM job_snapshots
        WHERE stipend IS NULL;
    """,

    "orphan_skills": """
        SELECT COUNT(*)
        FROM skills s
        LEFT JOIN job_skills js
            ON s.skill_id = js.skill_id
        WHERE js.skill_id IS NULL;
    """,

    "repeated_role_company_pairs": """
        SELECT COUNT(*)
        FROM (
            SELECT
                company_id,
                role
            FROM jobs
            GROUP BY company_id, role
            HAVING COUNT(*) > 1
        ) t;
    """
}

print("\nDATA QUALITY REPORT\n")

for check_name, query in checks.items():
    value = pd.read_sql(query, engine).iloc[0, 0]
    print(f"{check_name}: {value}")