from sqlalchemy import create_engine
import pandas as pd

DB_USER = "postgres"
DB_PASSWORD = "Alcoco9"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "clockedin"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

query = """
SELECT *
FROM companies;
"""

df = pd.read_sql(query, engine)

print(df)