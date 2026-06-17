import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine(
    "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"
)

st.set_page_config(
    page_title="ClockedIn",
    layout="wide"
)

st.title("ClockedIn")
st.caption("Tracking how job market requirements evolve over time")

skill_query = """
SELECT
    TO_CHAR(
        DATE_TRUNC('month', jsn.snapshot_date),
        'YYYY-MM'
    ) AS month,
    s.skill_name,
    COUNT(*) AS demand
FROM job_skills jsk
JOIN job_snapshots jsn ON jsk.snapshot_id = jsn.snapshot_id
JOIN skills s ON jsk.skill_id = s.skill_id
GROUP BY
    DATE_TRUNC('month', jsn.snapshot_date),
    s.skill_name
ORDER BY month;
"""

role_query = """
SELECT
    role,
    COUNT(*) AS total_jobs
FROM jobs
GROUP BY role
ORDER BY total_jobs DESC;
"""

company_query = """
SELECT
    c.company_name,
    COUNT(*) AS total_jobs
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
GROUP BY c.company_name
ORDER BY total_jobs DESC;
"""

location_query = """
SELECT
    location,
    COUNT(*) AS total_jobs
FROM job_snapshots
GROUP BY location
ORDER BY total_jobs DESC;
"""

summary_query = """
SELECT
    COUNT(*) AS total_snapshots,
    COUNT(DISTINCT job_id) AS unique_jobs,
    COUNT(DISTINCT snapshot_date) AS active_days
FROM job_snapshots;
"""

skill_df = pd.read_sql(skill_query, engine)
role_df = pd.read_sql(role_query, engine)
company_df = pd.read_sql(company_query, engine)
location_df = pd.read_sql(location_query, engine)
summary_df = pd.read_sql(summary_query, engine)

col1, col2, col3 = st.columns(3)
col1.metric("Snapshots", int(summary_df["total_snapshots"][0]))
col2.metric("Jobs", int(summary_df["unique_jobs"][0]))
col3.metric("Active Days", int(summary_df["active_days"][0]))

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Market Overview",
        "Skills",
        "Companies",
        "Locations"
    ]
)

with tab1:
    st.subheader("Role Distribution")
    role_fig = px.bar(
        role_df,
        x="role",
        y="total_jobs"
    )
    st.plotly_chart(
        role_fig,
        use_container_width=True
    )

    st.subheader("Top Growing Skills")
    growth_rows = []

    for skill in skill_df["skill_name"].unique():
        temp = skill_df[skill_df["skill_name"] == skill].sort_values("month")
        if len(temp) < 2:
            continue
        start = temp["demand"].iloc[0]
        end = temp["demand"].iloc[-1]
        growth_rows.append(
            {
                "skill": skill,
                "growth": end - start
            }
        )

    growth_df = pd.DataFrame(growth_rows).sort_values("growth", ascending=False)
    st.dataframe(
        growth_df.head(10),
        use_container_width=True
    )

with tab2:
    skills = sorted(skill_df["skill_name"].unique())
    selected_skills = st.multiselect(
        "Skills",
        skills,
        default=["Python", "SQL", "AWS", "PySpark"]
    )
    filtered = skill_df[skill_df["skill_name"].isin(selected_skills)]
    skill_fig = px.line(
        filtered,
        x="month",
        y="demand",
        color="skill_name",
        markers=True
    )
    st.plotly_chart(
        skill_fig,
        use_container_width=True
    )

with tab3:
    company_fig = px.bar(
        company_df.head(10),
        x="company_name",
        y="total_jobs"
    )
    st.plotly_chart(
        company_fig,
        use_container_width=True
    )

with tab4:
    location_fig = px.bar(
        location_df,
        x="location",
        y="total_jobs"
    )
    st.plotly_chart(
        location_fig,
        use_container_width=True
    )