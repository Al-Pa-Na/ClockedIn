# ClockedIn

## Problem Statement

Current job platforms only show available opportunities at a given point in time.

They do not provide visibility into:

- How hiring requirements evolve
- Which skills are gaining demand
- Which technologies are becoming obsolete
- How stipend and salary ranges change
- Which companies are increasing hiring activity

This information exists but is scattered across multiple platforms and is not stored historically.

---

## Solution

ClockedIn is a Job Market Intelligence Platform that continuously collects job and internship postings, stores historical snapshots, validates data quality, and generates trend analytics.

---

## Data Sources

Phase 1:
- Sample dataset

Phase 2:
- LinkedIn
- Internshala
- Wellfound

Phase 3:
- Company career pages

---

## Core Features

### Historical Job Tracking

Store changes in:

- skills
- salary
- requirements
- locations

over time.

### Skill Demand Analytics

Track:

- Python
- SQL
- Spark
- AWS
- Docker
- Airflow

and their demand evolution.

### Company Hiring Trends

Track hiring activity over time.

### Data Quality Reports

Detect:

- duplicate jobs
- missing salary
- missing company names
- invalid dates

---

## Planned Tech Stack

- Python
- PostgreSQL
- PySpark
- AWS S3
- Streamlit

---

## Data Engineering Components

- Extract
- Transform
- Load
- Data Validation
- Data Quality Monitoring
- Historical Warehousing