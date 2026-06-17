import random
from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "Alcoco9"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "clockedin"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

companies = [
    "Google", "Microsoft", "Amazon", "Atlassian", "Razorpay",
    "KFinTech", "Adobe", "Swiggy", "Flipkart", "Paytm"
]

roles = [
    "Software Engineer Intern",
    "Backend Intern",
    "Frontend Intern",
    "Full Stack Intern",
    "Data Engineering Intern",
    "Data Analyst Intern",
    "ML Intern",
    "AI Intern",
    "DevOps Intern"
]

skills_map = {
    "Software Engineer Intern": ["Python", "SQL", "Git"],
    "Backend Intern": ["Python", "SQL", "Docker"],
    "Frontend Intern": ["JavaScript", "React", "Git"],
    "Full Stack Intern": ["JavaScript", "React", "SQL"],
    "Data Engineering Intern": ["Python", "SQL", "PySpark", "AWS"],
    "Data Analyst Intern": ["Python", "SQL", "Excel"],
    "ML Intern": ["Python", "ML", "SQL"],
    "AI Intern": ["Python", "LLM", "SQL"],
    "DevOps Intern": ["Docker", "AWS", "Linux"]
}

locations = [
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Remote",
    "Bhubaneswar"
]

with engine.begin() as conn:

    for company in companies:
        conn.execute(
            text("""
                INSERT INTO companies (company_name)
                VALUES (:name)
                ON CONFLICT (company_name) DO NOTHING
            """),
            {"name": company}
        )

    skill_ids = {}

    all_skills = set()
    for x in skills_map.values():
        all_skills.update(x)

    for skill in all_skills:
        conn.execute(
            text("""
                INSERT INTO skills(skill_name)
                VALUES(:skill)
                ON CONFLICT(skill_name) DO NOTHING
            """),
            {"skill": skill}
        )

    rows = conn.execute(
        text("SELECT skill_id, skill_name FROM skills")
    ).fetchall()

    for sid, sname in rows:
        skill_ids[sname] = sid

    company_lookup = dict(
        conn.execute(
            text("SELECT company_id, company_name FROM companies")
        ).fetchall()
    )

    reverse_company = {v: k for k, v in company_lookup.items()}

    for _ in range(200):

        company = random.choice(companies)
        role = random.choice(roles)

        job_id = conn.execute(
            text("""
                INSERT INTO jobs(company_id, role, source)
                VALUES(:cid, :role, 'Generated')
                RETURNING job_id
            """),
            {
                "cid": reverse_company[company],
                "role": role
            }
        ).scalar()

        snapshot_id = conn.execute(
            text("""
                INSERT INTO job_snapshots(
                    job_id,
                    snapshot_date,
                    location,
                    stipend,
                    experience_required
                )
                VALUES(
                    :job_id,
                    CURRENT_DATE,
                    :location,
                    :stipend,
                    '0-1 years'
                )
                RETURNING snapshot_id
            """),
            {
                "job_id": job_id,
                "location": random.choice(locations),
                "stipend": str(random.randint(15000, 60000))
            }
        ).scalar()

        for skill in skills_map[role]:
            conn.execute(
                text("""
                    INSERT INTO job_skills(
                        snapshot_id,
                        skill_id
                    )
                    VALUES(:snapshot_id, :skill_id)
                """),
                {
                    "snapshot_id": snapshot_id,
                    "skill_id": skill_ids[skill]
                }
            )

print("Inserted 200 jobs successfully.")