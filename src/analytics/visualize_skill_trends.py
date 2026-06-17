import pandas as pd
import matplotlib.pyplot as plt
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
ORDER BY month;
"""

df = pd.read_sql(query, engine)

skills_to_plot = ["Python", "SQL", "AWS", "PySpark"]

plt.figure(figsize=(10, 6))

for skill in skills_to_plot:
    skill_df = df[df["skill_name"] == skill]
    plt.plot(
        skill_df["month"],
        skill_df["demand"],
        marker="o",
        label=skill
    )

plt.title("Skill Demand Over Time")
plt.xlabel("Month")
plt.ylabel("Demand")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()