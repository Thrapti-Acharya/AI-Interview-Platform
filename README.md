# PrepAI – AI Interview & Placement Preparation Platform

PrepAI is an AI-powered interview and placement preparation platform designed to help students prepare for campus placements through aptitude practice, coding practice, mock interviews, resume analysis, company recommendations, career guidance, placement readiness prediction, and an AI chat assistant.

## 🎯 Project Overview

Students often use multiple platforms to prepare for placements. PrepAI brings important placement preparation activities together in a single platform.

The system allows students to:

- Create an account and log in
- Practice aptitude questions
- Practice coding problems
- Take AI-based mock interviews
- Analyze their resume
- Track preparation progress
- Check placement readiness
- Get company recommendations
- Explore a career roadmap
- Interact with an AI chat assistant
- View and manage their profile

## 🚀 Key Features

### 1. Student Registration & Login
Students can create an account using their personal and academic details and securely log in to the platform.

### 2. Aptitude Practice
Students can attempt aptitude questions covering basic quantitative and logical reasoning concepts.

The system automatically calculates and stores the student's score.

### 3. Coding Practice
Students can practice programming problems by submitting their code through the coding practice module.

### 4. AI Mock Interview
The mock interview module provides interview questions and evaluates the student's responses to generate a performance score and feedback.

### 5. Resume Analysis
Students can upload their resume in PDF format and receive a resume analysis score.

### 6. Progress Tracking
The progress dashboard displays performance in:

- Aptitude
- Coding
- Mock Interview
- Resume

An overall preparation percentage is also calculated.

### 7. Placement Readiness Prediction
PrepAI combines the student's preparation scores to calculate an overall placement readiness percentage.

The system categorizes the student as:

- Excellent
- Good
- Average
- Needs Improvement

### 8. Company Recommendations
Students can explore companies and placement opportunities based on their preparation.

### 9. Career Roadmap
The career roadmap module provides guidance for students planning their placement preparation and career path.

### 10. AI Chat Assistant
Students can interact with the AI chat assistant for placement and interview preparation guidance.

### 11. Profile Management
Students can view their personal and academic information through their profile.

### 12. Admin Panel
The administrator can access student and platform-related information.

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite
- Flask-SQLAlchemy

### Other Technologies / Libraries
- PyPDF2
- Font Awesome
- Google Fonts

---

## 🏗️ Project Structure

```text
AI-INTERVIEW-PLATFORM/
│
├── instance/
│   └── database.db
│
├── static/
│   ├── css/
│   │   ├── admin.css
│   │   ├── aptitude.css
│   │   ├── career.css
│   │   ├── chatbot.css
│   │   ├── coding.css
│   │   ├── companies.css
│   │   ├── dashboard.css
│   │   ├── interview.css
│   │   ├── login.css
│   │   ├── mock_interview.css
│   │   ├── placement.css
│   │   ├── profile.css
│   │   ├── progress.css
│   │   ├── readiness.css
│   │   ├── recommendation.css
│   │   ├── register.css
│   │   ├── resume.css
│   │   └── style.css
│   │
│   ├── images/
│   │   └── profile.png
│   │
│   └── js/
│       ├── aptitude.js
│       ├── chatbot.js
│       ├── dashboard.js
│       ├── login.js
│       ├── mock_interview.js
│       └── register.js
│
├── templates/
│   ├── admin.html
│   ├── aptitude.html
│   ├── career.html
│   ├── chatbot.html
│   ├── coding.html
│   ├── companies.html
│   ├── dashboard.html
│   ├── index.html
│   ├── interview.html
│   ├── interview_result.html
│   ├── login.html
│   ├── mock_interview.html
│   ├── placement.html
│   ├── profile.html
│   ├── progress.html
│   ├── readiness.html
│   ├── recommendation.html
│   ├── register.html
│   ├── resume.html
│   └── resume_result.html
│
├── uploads/
│   └── Resume files
│
├── app.py
│
└── README.md