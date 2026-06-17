INSERT INTO companies (company_name)
VALUES
('Google'),
('Atlassian'),
('KFinTech'),
('Microsoft'),
('Razorpay');

INSERT INTO jobs (company_id, role, source)
VALUES
(1, 'Software Engineer Intern', 'LinkedIn'),
(2, 'Backend Intern', 'Wellfound'),
(3, 'Data Engineering Intern', 'LinkedIn'),
(4, 'Software Engineer Intern', 'Internshala'),
(5, 'Data Analyst Intern', 'LinkedIn');

INSERT INTO skills (skill_name)
VALUES
('Python'),
('SQL'),
('PySpark'),
('AWS'),
('Docker'),
('Airflow'),
('Git');

INSERT INTO job_snapshots (
    job_id,
    snapshot_date,
    location,
    stipend,
    experience_required
)
VALUES
(1, '2026-06-17', 'Bangalore', '50000', '0-1 years'),
(2, '2026-06-17', 'Remote', '40000', '0-1 years'),
(3, '2026-06-17', 'Bhubaneswar', '20000', '0-1 years'),
(4, '2026-06-17', 'Hyderabad', '45000', '0-1 years'),
(5, '2026-06-17', 'Remote', '35000', '0-1 years');

INSERT INTO job_skills VALUES
(1,1),(1,2),(1,7),
(2,1),(2,2),(2,5),
(3,1),(3,2),(3,3),(3,4),(3,6),
(4,1),(4,2),(4,5),
(5,1),(5,2);