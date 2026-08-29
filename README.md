# 🤖 JobMatch AI

### AI-Powered Job Matching Platform for Students & Freshers

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Vite](https://img.shields.io/badge/Vite-Build%20Tool-646CFF?logo=vite)

JobMatch AI is a full-stack web application that brings job opportunities from multiple sources into one place and helps students and freshers discover jobs that match their **education, skills, experience, location, and preferences**.

Instead of checking multiple job websites separately, users can discover relevant opportunities through a unified platform with **profile-based job matching, match scores, match explanations, and application tracking**.

---
## 📸 Screenshots

### 🔐 Login & Registration

The authentication interface allows students and companies to securely create accounts and log in.

### 🎯 Student Dashboard

The dashboard displays profile information, matching job statistics, recommended jobs and profile completion.

### 💼 Recommended Jobs

Jobs are displayed with match percentages, job details, filters and explanations showing why each job matches the student's profile.

### 📄 Application Tracking

Students can view, edit and delete their job applications and track their application status.

### 🏢 Company Dashboard

Companies can view their posted jobs and manage applications received from students.



## ✨ Project Highlights

- 🎯 **Profile-based job matching** with percentage scores
- 💼 **Multi-source job aggregation** from Jooble, Adzuna and JobDataLake
- 🧠 **Match explanations** showing why a job matches the student's profile
- 🔎 **Advanced job search and filtering**
- 📄 **Application tracking** with status management
- 👤 **Student profile, education and skills management**
- 🔐 **Session-based authentication**
- 📱 **Responsive React interface**

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

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, JavaScript, CSS, Vite |
| **Backend** | Python, FastAPI, SQLAlchemy |
| **Database** | PostgreSQL |
| **External APIs** | Jooble, Adzuna, JobDataLake |
| **Authentication** | Session-based authentication |
| **API Communication** | REST APIs |

### Frontend

- ⚛️ React
- JavaScript
- CSS
- Vite

### Backend

- 🐍 Python
- ⚡ FastAPI
- SQLAlchemy

### Database

- 🐘 PostgreSQL

### External Job Sources

- Jooble
- Adzuna
- JobDataLake

## 🔄 How It Works

JobMatch AI follows a simple profile-to-job matching workflow:

```text
┌──────────────────────┐
│   Create Account     │
│      / Login         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Complete Profile   │
│ Education • Skills   │
│ Preferences • etc.   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Collect Jobs       │
│ Jooble • Adzuna      │
│ • JobDataLake        │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Matching Engine    │
│ Compare profile with │
│ job requirements     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Match Score +      │
│   Match Reasons      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   View Job Details   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Apply & Track      │
│    Applications      │
└──────────────────────┘


## 📁 Project Structure

```text
JobMatchAI/
│
├── backend/
│   ├── auth/              # Authentication and sessions
│   ├── applications/      # Job application management
│   ├── external_jobs/     # External job source integrations
│   ├── jobs/              # Job management
│   ├── matching/          # Profile-based job matching
│   ├── models/            # SQLAlchemy database models
│   ├── preferences/       # Student job preferences
│   ├── profile/           # Student/company profiles
│   ├── resume/            # Resume management
│   ├── database.py        # Database connection
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Environment variable template
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React application
│   │   ├── App.css        # Application styling
│   │   └── main.jsx       # React entry point
│   ├── package.json
│   └── vite.config.js
│
├── database/              # Database-related resources
├── jobs/                  # Project job resources
├── tests/                 # Test resources
├── .gitignore
└── README.md


## 🚀 Local Setup

Follow these steps to run JobMatch AI locally.

### Prerequisites

Make sure you have installed:

- Python 3.x
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/bhanu798181-art/JobMatchAI.git
cd JobMatchAI

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

## 📌 Project Status

### Working Prototype

JobMatch AI is currently a working full-stack prototype developed and tested locally.

The main implemented features include:

- ✅ User authentication
- ✅ Student profile management
- ✅ Education and skills management
- ✅ Job preferences
- ✅ External job aggregation
- ✅ Profile-based job matching
- ✅ Job match percentage
- ✅ Match explanations
- ✅ Job search and filtering
- ✅ Job details
- ✅ Job applications
- ✅ Application tracking
- ✅ Company job management
- ✅ Application status management

The application has been tested locally with the configured job-source integrations.

---

## 🔮 Future Improvements

Planned improvements include:

- 🌐 Add more job sources
- 🧠 Improve matching algorithms
- 🔎 Add advanced search capabilities
- 🔔 Add application and job notifications
- 📊 Add analytics and dashboards
- 🎨 Further improve UI/UX
- 📍 Expand job collection locations
- 📝 Improve job-description processing
- ⚡ Improve matching and job-collection performance
- ☁️ Deploy the application to a production environment

## 👨‍💻 About the Project

JobMatch AI is an independently developed project created to explore practical **full-stack web development, API integration, database design, authentication, and profile-based job matching**.

The project brings together multiple technologies into a single career-focused application designed for students and freshers.

### What This Project Demonstrates

- ⚛️ React frontend development
- 🐍 Python and FastAPI backend development
- 🐘 PostgreSQL database design
- 🔗 REST API development and integration
- 🔐 Authentication and session management
- 💼 External job API integration
- 🎯 Profile-based job matching
- 📊 Application and data management
- 🧩 Full-stack application architecture

### 👤 Developer

**Bhanu Prakash**

Built as a practical full-stack project to learn, experiment, and develop real-world software engineering skills.

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.