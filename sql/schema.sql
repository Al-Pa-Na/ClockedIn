CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(company_id),
    role VARCHAR(255) NOT NULL,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE job_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    job_id INT REFERENCES jobs(job_id),
    snapshot_date DATE NOT NULL,
    location VARCHAR(255),
    stipend VARCHAR(100),
    experience_required VARCHAR(100)
);

CREATE TABLE job_skills (
    snapshot_id INT REFERENCES job_snapshots(snapshot_id),
    skill_id INT REFERENCES skills(skill_id),
    PRIMARY KEY (snapshot_id, skill_id)
);