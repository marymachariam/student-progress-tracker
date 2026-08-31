# Student Progress Dashboard

A web application that helps students track their academic journey by logging study sessions, recording quiz scores, and setting goals — all visualized through intuitive charts and progress statistics.

## Overview

Staying on top of study habits and academic performance can be difficult without the right tools. The Student Progress Dashboard gives students a centralized place to log their study activity, monitor quiz performance over time, and set measurable goals, helping them build consistency and make data-informed decisions about where to focus their efforts.

## Features

- **Study Session Logging** — Record study sessions by subject and topic, including time spent.
- **Quiz Score Tracking** — Log quiz results to monitor performance trends across subjects and topics.
- **Goal Setting** — Set and track academic goals tied to specific subjects or topics.
- **Progress Visualization** — View charts and statistics summarizing study habits, quiz performance, and goal progress.

## Tech Stack

| Layer      | Technology   |
|------------|--------------|
| Frontend   | Next.js      |
| Backend    | Flask        |
| Database   | SQLite       |

## Data Model

The application is built around the following core entities:

- **Users** — Student accounts and profile information.
- **Subjects** — High-level academic subjects (e.g., Mathematics, Biology).
- **Topics** — Specific topics nested within a subject.
- **Study Sessions** — Records of time spent studying a given topic.
- **Quiz Scores** — Results from quizzes tied to a subject/topic.
- **Goals** — Student-defined academic targets and their progress.

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm/yarn
- SQLite3

### Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  (On Windows: venv\Scripts\activate)
pip install -r requirements.txt
flask run

### Frontend Setup

cd frontend
npm install
npm run dev

The frontend will be available at http://localhost:3000 and the backend API at http://localhost:5000 (adjust ports as configured).

## Project Structure

student-progress-dashboard/
├── backend/          (Flask API and SQLite database)
├── frontend/         (Next.js application)
└── README.md

## Roadmap

- [ ] User authentication
- [ ] Export progress reports
- [ ] Reminders/notifications for study goals
- [ ] Mobile-responsive dashboard improvements


## Author

**Mary Macharia**
