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