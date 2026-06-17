# ClockedIn

ClockedIn is a job market analytics platform that collects real internship and job postings, stores them in PostgreSQL, extracts important skills from descriptions, and visualizes hiring trends through an interactive dashboard.

The goal is to move beyond static job boards and build a system that can answer questions like:

* Which skills are currently in demand?
* Which companies are hiring the most?
* Which locations have the highest number of opportunities?
* How is the internship market changing over time?

---

## What it does

* Fetches live jobs using the JSearch API
* Runs an ETL pipeline to clean and process the data
* Stores data in PostgreSQL
* Extracts technical skills from job descriptions
* Prevents duplicate job entries
* Displays analytics through a Streamlit dashboard

---

## Tech Stack

* Python
* PostgreSQL
* SQLAlchemy
* Streamlit
* Plotly
* PySpark
* JSearch API
* Git & GitHub

---

## Project Architecture

JSearch API

↓

Extract

↓

Transform

↓

Load

↓

PostgreSQL

↓

Streamlit Dashboard

---

## Current Dashboard Features

### Market Overview

View overall hiring activity and role distribution.

### Skills Analysis

Track demand for skills extracted from job descriptions.

### Company Insights

See which companies are hiring the most.

### Location Insights

Analyze hiring activity across different locations.

### Live Internship Feed

Browse recently ingested internship opportunities.

### Data Quality Checks

Monitor missing values and data consistency.

---

## Current Progress

### Completed

* Live API integration
* ETL pipeline
* PostgreSQL database design
* Skill extraction pipeline
* Duplicate detection
* Streamlit dashboard
* Real-time job ingestion

### Working On

* Better skill trend analysis
* Dashboard filters
* Historical tracking
* Automated ingestion jobs

---

## Sample Insights

Some of the most demanded skills currently identified by the platform include:

* Python
* SQL
* Machine Learning
* Git
* AWS
* Pandas
* PySpark

The dashboard also tracks hiring companies, locations, and internship opportunities in real time.

---

## Future Plans

* Airflow-based scheduling
* AWS S3 integration
* Salary analysis
* Skill demand forecasting
* Recommendation system for students
