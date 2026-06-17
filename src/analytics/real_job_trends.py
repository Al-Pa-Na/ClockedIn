import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

df = pd.read_sql(
    """
    SELECT
        title,
        company_name,
        location,
        employment_type,
        posted_at
    FROM real_jobs
    """,
    engine
)

skills = {
    "Python": ["python"],
    "SQL": ["sql"],
    "AWS": ["aws"],
    "PySpark": ["pyspark", "spark"],
    "Docker": ["docker"],
    "Airflow": ["airflow"],
    "Snowflake": ["snowflake"],
    "Machine Learning": ["machine learning", "ml"],
    "AI": ["artificial intelligence", "ai"],
    "Data Engineering": ["data engineer"],
    "Backend": ["backend"],
}

skill_counts = {}

for skill, keywords in skills.items():

    count = 0

    for title in df["title"].fillna(""):

        title_lower = title.lower()

        if any(keyword in title_lower for keyword in keywords):
            count += 1

    skill_counts[skill] = count

result = (
    pd.DataFrame(
        skill_counts.items(),
        columns=["skill", "count"]
    )
    .sort_values("count", ascending=False)
)

print("\nLIVE SKILL DEMAND\n")
print(result)