from pyspark.sql import SparkSession
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

query = """
SELECT
    j.role,
    c.company_name,
    js.location,
    js.snapshot_date,
    s.skill_name
FROM jobs j
JOIN companies c
    ON j.company_id = c.company_id
JOIN job_snapshots js
    ON j.job_id = js.job_id
JOIN job_skills jsk
    ON js.snapshot_id = jsk.snapshot_id
JOIN skills s
    ON jsk.skill_id = s.skill_id;
"""

pdf = pd.read_sql(query, engine)

spark = SparkSession.builder \
    .appName("ClockedIn") \
    .getOrCreate()

df = spark.createDataFrame(pdf)

print("\nTOP SKILLS\n")

df.groupBy("skill_name") \
    .count() \
    .orderBy("count", ascending=False) \
    .show()

print("\nTOP LOCATIONS\n")

df.groupBy("location") \
    .count() \
    .orderBy("count", ascending=False) \
    .show()

print("\nTOP ROLES\n")

df.groupBy("role") \
    .count() \
    .orderBy("count", ascending=False) \
    .show()

spark.stop()