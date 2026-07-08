from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import connect, get_cursor
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {'Message': 'Hello welcome to my Student Progress tacker!'}


# registering a student
class RegisterStudent(BaseModel):
    name: str
    email: str
    password: str


@app.post('/register_student')
def register(user: RegisterStudent):
    cursor = get_cursor()
    cursor.execute(
        "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
        (user.name, user.email, user.password)
    )
    connect.commit()
    return {
        "message": "Student account created successfully!",
        "student_id": cursor.lastrowid,
        "name": user.name
    }


# the login end point
class LoginStudent(BaseModel):
    email: str
    password: str


@app.post("/login")
def login(user: LoginStudent):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM students WHERE email = ?", (user.email,))
    db_user = cursor.fetchone()

    if not db_user:
        return {"error": "Invalid email or password"}

    stored_password = db_user[3]
    if user.password != stored_password:
        return {"error": "Invalid email or password"}

    return {
        "message": "Login successful",
        "student_id": db_user[0],
        "name": db_user[1]
    }


# Subjects CRUD
class Subject(BaseModel):
    student_id: int
    name: str
    color: str


@app.post("/subjects")
def create_subject(subject: Subject):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO subjects (student_id, name, color)
        VALUES (?, ?, ?)
        """,
        (subject.student_id, subject.name, subject.color)
    )
    connect.commit()
    return {"message": "Subject created successfully"}


@app.get("/subjects")
def get_subjects(student_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM subjects WHERE student_id = ?", (student_id,))
    subjects = cursor.fetchall()
    return {"subjects": subjects}


@app.get("/subjects/{subject_id}")
def get_subject(subject_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
    subject = cursor.fetchone()

    if subject is None:
        return {"message": "Subject not found"}

    return {"subject": subject}


@app.put("/subjects/{subject_id}")
def update_subject(subject_id: int, subject: Subject):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE subjects
        SET student_id = ?, name = ?, color = ?
        WHERE subject_id = ?
        """,
        (subject.student_id, subject.name, subject.color, subject_id)
    )

    if cursor.rowcount == 0:
        return {"message": "Subject not found"}

    connect.commit()
    return {"message": "Subject updated successfully"}


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int):
    cursor = get_cursor()
    cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))

    if cursor.rowcount == 0:
        return {"message": "Subject not found"}

    connect.commit()
    return {"message": "Subject deleted successfully"}


# Topics CRUD
class Topic(BaseModel):
    student_id: int
    subject_id: int
    name: str


@app.post("/topics")
def create_topic(topic: Topic):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO topics (student_id, subject_id, name)
        VALUES (?, ?, ?)
        """,
        (topic.student_id, topic.subject_id, topic.name)
    )
    connect.commit()
    return {"message": "Topic created successfully"}


@app.get("/topics")
def get_topics(student_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM topics WHERE student_id = ?", (student_id,))
    topics = cursor.fetchall()
    return {"topics": topics}


@app.get("/topics/{topic_id}")
def get_topic(topic_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM topics WHERE topic_id = ?", (topic_id,))
    topic = cursor.fetchone()

    if topic is None:
        return {"message": "Topic not found"}

    return {"topic": topic}


@app.put("/topics/{topic_id}")
def update_topic(topic_id: int, topic: Topic):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE topics
        SET student_id = ?, subject_id = ?, name = ?
        WHERE topic_id = ?
        """,
        (topic.student_id, topic.subject_id, topic.name, topic_id)
    )

    if cursor.rowcount == 0:
        return {"message": "Topic not found"}

    connect.commit()
    return {"message": "Topic updated successfully"}


@app.delete("/topics/{topic_id}")
def delete_topic(topic_id: int):
    cursor = get_cursor()
    cursor.execute("DELETE FROM topics WHERE topic_id = ?", (topic_id,))

    if cursor.rowcount == 0:
        return {"message": "Topic not found"}

    connect.commit()
    return {"message": "Topic deleted successfully"}


# Study Sessions CRUD
class StudySession(BaseModel):
    student_id: int
    subject_id: int
    topic_id: int
    study_date: str
    hours: float
    notes: str


@app.post("/study_sessions")
def create_study_session(session: StudySession):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO study_sessions
        (student_id, subject_id, topic_id, study_date, hours, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session.student_id,
            session.subject_id,
            session.topic_id,
            session.study_date,
            session.hours,
            session.notes
        )
    )
    connect.commit()
    return {"message": "Study session created successfully"}


@app.get("/study_sessions")
def get_study_sessions(student_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE student_id = ?", (student_id,))
    sessions = cursor.fetchall()
    return {"study_sessions": sessions}


@app.get("/study_sessions/{session_id}")
def get_study_session(session_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM study_sessions WHERE session_id = ?", (session_id,))
    session = cursor.fetchone()

    if session is None:
        return {"message": "Study session not found"}

    return {"study_session": session}


@app.put("/study_sessions/{session_id}")
def update_study_session(session_id: int, session: StudySession):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE study_sessions
        SET student_id = ?, subject_id = ?, topic_id = ?, study_date = ?, hours = ?, notes = ?
        WHERE session_id = ?
        """,
        (
            session.student_id,
            session.subject_id,
            session.topic_id,
            session.study_date,
            session.hours,
            session.notes,
            session_id
        )
    )

    if cursor.rowcount == 0:
        return {"message": "Study session not found"}

    connect.commit()
    return {"message": "Study session updated successfully"}


@app.delete("/study_sessions/{session_id}")
def delete_study_session(session_id: int):
    cursor = get_cursor()
    cursor.execute("DELETE FROM study_sessions WHERE session_id = ?", (session_id,))

    if cursor.rowcount == 0:
        return {"message": "Study session not found"}

    connect.commit()
    return {"message": "Study session deleted successfully"}


# Quiz Scores CRUD
class QuizScore(BaseModel):
    student_id: int
    subject_id: int
    topic_id: int
    score: int
    total_marks: int
    quiz_date: str


@app.post("/quiz_scores")
def create_quiz_score(quiz: QuizScore):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO quiz_scores
        (student_id, subject_id, topic_id, score, total_marks, quiz_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            quiz.student_id,
            quiz.subject_id,
            quiz.topic_id,
            quiz.score,
            quiz.total_marks,
            quiz.quiz_date
        )
    )
    connect.commit()
    return {"message": "Quiz score added successfully"}


@app.get("/quiz_scores")
def get_quiz_scores(student_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM quiz_scores WHERE student_id = ?", (student_id,))
    quiz_scores = cursor.fetchall()
    return {"quiz_scores": quiz_scores}


@app.get("/quiz_scores/{quiz_id}")
def get_quiz_score(quiz_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM quiz_scores WHERE score_id = ?", (quiz_id,))
    quiz = cursor.fetchone()

    if quiz is None:
        return {"message": "Quiz score not found"}

    return {"quiz_score": quiz}


@app.put("/quiz_scores/{quiz_id}")
def update_quiz_score(quiz_id: int, quiz: QuizScore):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE quiz_scores
        SET student_id = ?, subject_id = ?, topic_id = ?, score = ?, total_marks = ?, quiz_date = ?
        WHERE score_id = ?
        """,
        (
            quiz.student_id,
            quiz.subject_id,
            quiz.topic_id,
            quiz.score,
            quiz.total_marks,
            quiz.quiz_date,
            quiz_id
        )
    )

    if cursor.rowcount == 0:
        return {"message": "Quiz score not found"}

    connect.commit()
    return {"message": "Quiz score updated successfully"}


@app.delete("/quiz_scores/{quiz_id}")
def delete_quiz_score(quiz_id: int):
    cursor = get_cursor()
    cursor.execute("DELETE FROM quiz_scores WHERE score_id = ?", (quiz_id,))

    if cursor.rowcount == 0:
        return {"message": "Quiz score not found"}

    connect.commit()
    return {"message": "Quiz score deleted successfully"}


# Goals CRUD
class Goal(BaseModel):
    student_id: int
    title: str
    target_type: str
    target_value: float
    start_date: str
    end_date: str
    is_completed: int = 0


@app.post("/goals")
def create_goal(goal: Goal):
    cursor = get_cursor()
    cursor.execute(
        """
        INSERT INTO goals
        (student_id, title, target_type, target_value, start_date, end_date, is_completed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            goal.student_id,
            goal.title,
            goal.target_type,
            goal.target_value,
            goal.start_date,
            goal.end_date,
            goal.is_completed
        )
    )
    connect.commit()
    return {"message": "Goal created successfully"}


@app.get("/goals")
def get_goals(student_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM goals WHERE student_id = ?", (student_id,))
    goals = cursor.fetchall()
    return {"goals": goals}


@app.get("/goals/{goal_id}")
def get_goal(goal_id: int):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM goals WHERE goal_id = ?", (goal_id,))
    goal = cursor.fetchone()

    if goal is None:
        return {"message": "Goal not found"}

    return {"goal": goal}


@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal: Goal):
    cursor = get_cursor()
    cursor.execute(
        """
        UPDATE goals
        SET student_id = ?, title = ?, target_type = ?, target_value = ?,
            start_date = ?, end_date = ?, is_completed = ?
        WHERE goal_id = ?
        """,
        (
            goal.student_id,
            goal.title,
            goal.target_type,
            goal.target_value,
            goal.start_date,
            goal.end_date,
            goal.is_completed,
            goal_id
        )
    )

    if cursor.rowcount == 0:
        return {"message": "Goal not found"}

    connect.commit()
    return {"message": "Goal updated successfully"}


@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int):
    cursor = get_cursor()
    cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))

    if cursor.rowcount == 0:
        return {"message": "Goal not found"}

    connect.commit()
    return {"message": "Goal deleted successfully"}


# ---- the logic / dashboard side ----

@app.get("/dashboard")
def dashboard(student_id: int):
    cursor = get_cursor()

    cursor.execute("SELECT SUM(hours) FROM study_sessions WHERE student_id = ?", (student_id,))
    total_hours = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(score * 1.0 / total_marks) FROM quiz_scores WHERE student_id = ?", (student_id,))
    avg_score = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM goals WHERE is_completed = 0 AND student_id = ?", (student_id,))
    active_goals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM goals WHERE is_completed = 1 AND student_id = ?", (student_id,))
    completed_goals = cursor.fetchone()[0]

    cursor.execute("""
        SELECT s.name, SUM(ss.hours) AS total
        FROM study_sessions ss
        JOIN subjects s ON ss.subject_id = s.subject_id
        WHERE ss.student_id = ?
        GROUP BY ss.subject_id
        ORDER BY total DESC
        LIMIT 1
    """, (student_id,))
    top_subject_row = cursor.fetchone()
    top_subject = top_subject_row[0] if top_subject_row else "None"

    return {
        "total_hours_studied": round(total_hours, 2),
        "average_quiz_score_percent": round(avg_score * 100, 1),
        "active_goals": active_goals,
        "completed_goals": completed_goals,
        "top_subject": top_subject
    }


@app.get("/dashboard/subject-breakdown")
def subject_breakdown(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT s.name, SUM(ss.hours) AS total_hours
        FROM study_sessions ss
        JOIN subjects s ON ss.subject_id = s.subject_id
        WHERE ss.student_id = ?
        GROUP BY ss.subject_id
        ORDER BY total_hours DESC
    """, (student_id,))

    rows = cursor.fetchall()
    breakdown = [{"subject": row[0], "hours": row[1]} for row in rows]
    return {"subject_breakdown": breakdown}


@app.get("/dashboard/progress-over-time")
def progress_over_time(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT strftime('%Y-W%W', study_date) AS week, SUM(hours) AS total_hours
        FROM study_sessions
        WHERE student_id = ?
        GROUP BY week
        ORDER BY week
    """, (student_id,))

    rows = cursor.fetchall()
    result = [{"week": row[0], "hours": row[1]} for row in rows]
    return {"progress_over_time": result}


@app.get("/dashboard/quiz-trend")
def quiz_trend(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT t.name, AVG(q.score * 1.0 / q.total_marks) AS avg_score
        FROM quiz_scores q
        JOIN topics t ON q.topic_id = t.topic_id
        WHERE q.student_id = ?
        GROUP BY q.topic_id
        ORDER BY avg_score DESC
    """, (student_id,))

    rows = cursor.fetchall()
    result = [{"topic": row[0], "average_score_percent": round(row[1] * 100, 1)} for row in rows]
    return {"quiz_trend": result}


@app.get("/dashboard/weakest-topic")
def weakest_topic(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT t.name, AVG(q.score * 1.0 / q.total_marks) AS avg_score
        FROM quiz_scores q
        JOIN topics t ON q.topic_id = t.topic_id
        WHERE q.student_id = ?
        GROUP BY q.topic_id
        ORDER BY avg_score ASC
        LIMIT 1
    """, (student_id,))

    row = cursor.fetchone()
    if not row:
        return {"weakest_topic": None}

    return {
        "weakest_topic": {
            "topic": row[0],
            "average_score_percent": round(row[1] * 100, 1)
        }
    }


@app.get("/dashboard/goal-progress")
def goal_progress(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT goal_id, title, target_type, target_value, start_date, end_date
        FROM goals
        WHERE is_completed = 0 AND student_id = ?
    """, (student_id,))

    goals = cursor.fetchall()
    result = []

    for goal in goals:
        goal_id, title, target_type, target_value, start_date, end_date = goal

        if target_type == "hours":
            cursor.execute("""
                SELECT SUM(hours) FROM study_sessions
                WHERE study_date >= ? AND student_id = ?
            """, (start_date, student_id))
            actual = cursor.fetchone()[0] or 0
        else:
            actual = 0

        percent_complete = (actual / target_value * 100) if target_value else 0

        result.append({
            "goal_id": goal_id,
            "title": title,
            "target_value": target_value,
            "actual_progress": actual,
            "percent_complete": round(percent_complete, 1),
            "end_date": end_date
        })

    return {"goal_progress": result}


@app.get("/dashboard/study-streak")
def study_streak(student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT DISTINCT study_date FROM study_sessions
        WHERE student_id = ?
        ORDER BY study_date DESC
    """, (student_id,))

    rows = cursor.fetchall()
    study_dates = {
        datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
        for row in rows
    }

    streak = 0
    current_day = datetime.date.today()

    while current_day in study_dates:
        streak += 1
        current_day -= datetime.timedelta(days=1)

    return {"current_streak_days": streak}


@app.get("/dashboard/prediction/{goal_id}")
def goal_prediction(goal_id: int, student_id: int):
    cursor = get_cursor()
    cursor.execute("""
        SELECT target_value, start_date, end_date
        FROM goals
        WHERE goal_id = ? AND student_id = ?
    """, (goal_id, student_id))

    goal = cursor.fetchone()
    if not goal:
        return {"message": "Goal not found"}

    target_value, start_date, end_date = goal

    cursor.execute("""
        SELECT SUM(hours) FROM study_sessions
        WHERE study_date >= ? AND student_id = ?
    """, (start_date, student_id))
    actual_so_far = cursor.fetchone()[0] or 0

    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    today = datetime.date.today()

    days_elapsed = max((today - start).days, 1)
    days_total = max((end - start).days, 1)

    daily_avg = actual_so_far / days_elapsed
    predicted_total = daily_avg * days_total

    on_track = predicted_total >= target_value

    return {
        "goal_id": goal_id,
        "target_value": target_value,
        "actual_so_far": actual_so_far,
        "predicted_final_total": round(predicted_total, 2),
        "on_track": on_track
    }


@app.get("/dashboard/alerts")
def dashboard_alerts(student_id: int):
    cursor = get_cursor()
    alerts = []

    cursor.execute("""
        SELECT goal_id, title, target_type, target_value, start_date, end_date
        FROM goals
        WHERE is_completed = 0 AND student_id = ?
    """, (student_id,))

    for goal_id, title, target_type, target_value, start_date, end_date in cursor.fetchall():
        if target_type != "hours":
            continue

        start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        today = datetime.date.today()

        days_elapsed = max((today - start).days, 1)
        days_total = max((end - start).days, 1)
        expected_progress = target_value * (days_elapsed / days_total)

        cursor.execute("""
            SELECT SUM(hours) FROM study_sessions
            WHERE study_date >= ? AND student_id = ?
        """, (start_date, student_id))
        actual = cursor.fetchone()[0] or 0

        if actual < expected_progress:
            alerts.append({
                "type": "goal_behind_schedule",
                "goal": title,
                "expected_by_now": round(expected_progress, 1),
                "actual": actual
            })

    cursor.execute("SELECT subject_id, name FROM subjects WHERE student_id = ?", (student_id,))
    subjects = cursor.fetchall()

    for subject_id, name in subjects:
        cursor.execute("""
            SELECT MAX(study_date) FROM study_sessions
            WHERE subject_id = ? AND student_id = ?
        """, (subject_id, student_id))
        last_date_row = cursor.fetchone()[0]

        if last_date_row is None:
            alerts.append({"type": "no_sessions_logged", "subject": name})
            continue

        last_date = datetime.datetime.strptime(last_date_row, "%Y-%m-%d").date()
        days_since = (datetime.date.today() - last_date).days

        if days_since >= 3:
            alerts.append({
                "type": "subject_inactive",
                "subject": name,
                "days_since_last_session": days_since
            })

    return {"alerts": alerts}