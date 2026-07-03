import sqlite3

def get_connection():
    connect = sqlite3.connect('student_tracker.db', check_same_thread=False)
    connect.execute("PRAGMA foreign_keys = ON")
    return connect

connect = get_connection()

def get_cursor():
    return connect.cursor()

cursor = connect.cursor()

#students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
connect.commit()

#subjects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
''')
connect.commit()

#topics table
cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
''')
connect.commit()

#study sessions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS study_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,

    study_date DATE NOT NULL,
    hours REAL NOT NULL,
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);
''')
connect.commit()

# quiz scores table
cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,

    score INTEGER NOT NULL,
    total_marks INTEGER NOT NULL,
    quiz_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);
''')
connect.commit()

#goals table
cursor.execute('''
CREATE TABLE IF NOT EXISTS goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,

    title TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_value REAL NOT NULL,

    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    is_completed INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
''')
connect.commit()