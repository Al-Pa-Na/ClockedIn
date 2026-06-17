import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

query = """
SELECT
    s.skill_name,
    COUNT(*) as demand
FROM job_skills js
JOIN skills s
ON js.skill_id = s.skill_id
GROUP BY s.skill_name
ORDER BY demand DESC;
"""

df = pd.read_sql(query, engine)

print(df)