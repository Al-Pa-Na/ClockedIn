import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

query = """
SELECT
    TO_CHAR(
        DATE_TRUNC('month', jsn.snapshot_date),
        'YYYY-MM'
    ) AS month,
    s.skill_name,
    COUNT(*) AS demand
FROM job_skills jsk
JOIN job_snapshots jsn
    ON jsk.snapshot_id = jsn.snapshot_id
JOIN skills s
    ON jsk.skill_id = s.skill_id
GROUP BY
    DATE_TRUNC('month', jsn.snapshot_date),
    s.skill_name
ORDER BY
    month,
    demand DESC;
"""

df = pd.read_sql(query, engine)

print(df)