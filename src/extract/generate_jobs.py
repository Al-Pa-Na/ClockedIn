import random
from datetime import date, timedelta
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:Alcoco9@localhost:5432/clockedin"

TOTAL_SNAPSHOTS = 500
NUM_MONTHS = 6
DAYS_PER_MONTH = 30

MONTHLY_SNAPSHOT_COUNTS = [83, 83, 83, 83, 84, 84]

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Atlassian", "Razorpay",
    "KFinTech", "Adobe", "Swiggy", "Flipkart", "Paytm",
]

ROLES = [
    "Software Engineer Intern",
    "Backend Intern",
    "Frontend Intern",
    "Full Stack Intern",
    "Data Engineering Intern",
    "Data Analyst Intern",
    "ML Intern",
    "AI Intern",
    "DevOps Intern",
]

SKILLS_MAP = {
    "Software Engineer Intern": ["Python", "SQL", "Git"],
    "Backend Intern": ["Python", "SQL", "Docker"],
    "Frontend Intern": ["JavaScript", "React", "Git"],
    "Full Stack Intern": ["JavaScript", "React", "SQL"],
    "Data Engineering Intern": ["Python", "SQL", "PySpark", "AWS"],
    "Data Analyst Intern": ["Python", "SQL", "Excel"],
    "ML Intern": ["Python", "ML", "SQL"],
    "AI Intern": ["Python", "LLM", "SQL"],
    "DevOps Intern": ["Docker", "AWS", "Linux"],
}

LOCATIONS = ["Bangalore", "Hyderabad", "Pune", "Remote", "Bhubaneswar"]

BASE_STIPEND_BY_ROLE = {
    "Software Engineer Intern": 30000,
    "Backend Intern": 32000,
    "Frontend Intern": 28000,
    "Full Stack Intern": 33000,
    "Data Engineering Intern": 38000,
    "Data Analyst Intern": 30000,
    "ML Intern": 36000,
    "AI Intern": 37000,
    "DevOps Intern": 34000,
}

ROLE_WEIGHTS_BY_MONTH = [
    [30, 10, 25, 10, 5, 8, 5, 3, 4],
    [28, 12, 23, 10, 5, 8, 6, 4, 4],
    [20, 22, 15, 10, 7, 8, 8, 5, 5],
    [15, 25, 12, 10, 9, 8, 9, 6, 6],
    [10, 15, 8, 8, 10, 7, 10, 7, 25],
    [8, 10, 6, 6, 25, 6, 11, 8, 20],
]

TREND_SKILL_PROBABILITY = {
    "Docker": [0.00, 0.05, 0.35, 0.55, 0.50, 0.45],
    "AWS": [0.00, 0.00, 0.05, 0.10, 0.60, 0.65],
    "PySpark": [0.00, 0.00, 0.00, 0.05, 0.15, 0.60],
}


def get_engine():
    return create_engine(DATABASE_URL)


def seed_lookup_tables(conn, all_skills):
    for company in COMPANIES:
        conn.execute(
            text(
                """
                INSERT INTO companies (company_name)
                VALUES (:name)
                ON CONFLICT (company_name) DO NOTHING
                """
            ),
            {"name": company},
        )

    for skill in all_skills:
        conn.execute(
            text(
                """
                INSERT INTO skills (skill_name)
                VALUES (:skill)
                ON CONFLICT (skill_name) DO NOTHING
                """
            ),
            {"skill": skill},
        )

    company_rows = conn.execute(
        text("SELECT company_id, company_name FROM companies")
    ).fetchall()
    company_lookup = {name: cid for cid, name in company_rows}

    skill_rows = conn.execute(
        text("SELECT skill_id, skill_name FROM skills")
    ).fetchall()
    skill_lookup = {name: sid for sid, name in skill_rows}

    return company_lookup, skill_lookup


def snapshot_date_for_month(month_index):
    chunk_from_today = (NUM_MONTHS - 1) - month_index
    day_lower = chunk_from_today * DAYS_PER_MONTH
    day_upper = day_lower + (DAYS_PER_MONTH - 1)
    days_ago = random.randint(day_lower, day_upper)
    return date.today() - timedelta(days=days_ago)


def choose_role(month_index):
    weights = ROLE_WEIGHTS_BY_MONTH[month_index]
    return random.choices(ROLES, weights=weights, k=1)[0]


def choose_skills(role, month_index):
    skill_set = set(SKILLS_MAP[role])
    for trend_skill, probabilities in TREND_SKILL_PROBABILITY.items():
        if random.random() < probabilities[month_index]:
            skill_set.add(trend_skill)
    return skill_set


def generate_stipend(role, month_index):
    base = BASE_STIPEND_BY_ROLE[role]
    monthly_drift = month_index * 1200
    jitter = random.randint(-1500, 1500)
    stipend = base + monthly_drift + jitter
    return str(max(15000, min(stipend, 65000)))


def main():
    all_skills = set()
    for skill_list in SKILLS_MAP.values():
        all_skills.update(skill_list)

    engine = get_engine()
    inserted = 0

    with engine.begin() as conn:
        company_lookup, skill_lookup = seed_lookup_tables(conn, all_skills)

        for month_index, count in enumerate(MONTHLY_SNAPSHOT_COUNTS):
            for _ in range(count):
                company = random.choice(COMPANIES)
                role = choose_role(month_index)

                job_id = conn.execute(
                    text(
                        """
                        INSERT INTO jobs (company_id, role, source)
                        VALUES (:company_id, :role, 'Generated')
                        RETURNING job_id
                        """
                    ),
                    {
                        "company_id": company_lookup[company],
                        "role": role,
                    },
                ).scalar()

                snapshot_date = snapshot_date_for_month(month_index)
                stipend = generate_stipend(role, month_index)

                snapshot_id = conn.execute(
                    text(
                        """
                        INSERT INTO job_snapshots (
                            job_id,
                            snapshot_date,
                            location,
                            stipend,
                            experience_required
                        )
                        VALUES (
                            :job_id,
                            :snapshot_date,
                            :location,
                            :stipend,
                            '0-1 years'
                        )
                        RETURNING snapshot_id
                        """
                    ),
                    {
                        "job_id": job_id,
                        "snapshot_date": snapshot_date,
                        "location": random.choice(LOCATIONS),
                        "stipend": stipend,
                    },
                ).scalar()

                for skill in choose_skills(role, month_index):
                    conn.execute(
                        text(
                            """
                            INSERT INTO job_skills (snapshot_id, skill_id)
                            VALUES (:snapshot_id, :skill_id)
                            """
                        ),
                        {
                            "snapshot_id": snapshot_id,
                            "skill_id": skill_lookup[skill],
                        },
                    )

                inserted += 1

    print(f"Inserted {inserted} evolving historical job snapshots.")


if __name__ == "__main__":
    main()