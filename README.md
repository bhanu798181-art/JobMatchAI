# JobMatch AI

JobMatch AI is a full-stack web application that brings job opportunities from multiple sources into one place and helps students and freshers discover jobs that match their profile.

The application combines external job aggregation with profile-based job matching, allowing users to search for relevant opportunities without checking multiple job sources separately.

## Features

- Student registration and login
- Student profile management
- Education details
- Skills and proficiency management
- Job preferences
- Job search and filtering
- Automated job matching
- Job match percentage
- Match reasons explaining job eligibility
- External job aggregation
- External application links
- Application tracking
- Resume management
- Responsive React interface

## Job Sources

JobMatch AI currently collects jobs from:

- Jooble
- Adzuna
- JobDataLake

Jobs from these sources are collected and stored in the application database and displayed through a unified interface.

## Matching System

The matching engine compares job requirements with information in the student's profile.

It considers:

- Education
- Branch and qualification
- Academic performance
- Experience
- Location
- Work mode
- Employment preferences
- Skills

The application also provides reasons explaining why a job matches or does not match the user's profile.

## Technology Stack

### Frontend

- React
- JavaScript
- CSS
- Vite

### Backend

- Python
- FastAPI
- SQLAlchemy

### Database

- PostgreSQL

### External APIs

- Jooble
- Adzuna
- JobDataLake

## How It Works

```text
User
  |
  v
Create Account / Login
  |
  v
Complete Profile
  |
  v
Add Education, Skills and Preferences
  |
  v
Jobs collected from external sources
  |
  v
Matching Engine
  |
  v
Relevant Jobs
  |
  v
View Job Details
  |
  v
Apply
  |
  v
Track Application

Project Structure

JobMatchAI/
|
|-- backend/
|   |-- auth/
|   |-- applications/
|   |-- external_jobs/
|   |   |-- adzuna.py
|   |   |-- jooble.py
|   |   |-- jobdatalake.py
|   |   |-- models.py
|   |   |-- routes.py
|   |   `-- scheduler.py
|   |-- jobs/
|   |-- matching/
|   |-- models/
|   |-- preferences/
|   |-- profile/
|   |-- resume/
|   |-- database.py
|   |-- main.py
|   |-- requirements.txt
|   `-- .env.example
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- App.css
|   |   `-- main.jsx
|   |-- package.json
|   `-- vite.config.js
|
|-- .gitignore
`-- README.md


Local Setup
Backend

Open a terminal in the project folder and run:

cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a file:

backend/.env

Use:

backend/.env.example

as the template.

Required environment variables:

DATABASE_URL=
SECRET_KEY=
ADZUNA_APP_ID=
ADZUNA_APP_KEY=
JOOBLE_API_KEY=
JOBDATALAKE_API_KEY=

Do not publish the real .env file or API keys.

Start the backend:

python -m uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Open the URL shown by Vite, normally:

http://localhost:5173
Job Collection

JobMatch AI supports collecting jobs from multiple external sources.

The current collection system supports:

Jooble
Adzuna
JobDataLake

The scheduler performs configured searches and stores new jobs in the PostgreSQL database.

Duplicate jobs are detected using the external source and external job ID.

Project Status
Working Prototype

The main application features are currently working locally, including:

Authentication
Student profiles
Education
Skills
Preferences
External job collection
Job matching
Job search
Job filtering
Job details
Applications
Resume management

The application has been tested locally with all three configured external job sources.

Future Improvements
Add more job sources
Improve matching algorithms
Improve duplicate-job detection
Add advanced search
Add notifications
Improve analytics
Further UI/UX improvements
Add more job collection locations
Improve job description processing
About

JobMatch AI is an independently developed personal project created to explore practical full-stack development.

The project demonstrates experience with:

React
FastAPI
Python
PostgreSQL
SQLAlchemy
REST APIs
External API integration
Authentication
Job aggregation
Profile-based matching
Database design