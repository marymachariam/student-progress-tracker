"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";
import { getStudent } from "../../lib/auth";

export default function StudySessionsPage() {
  const [student, setStudent] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");

  const [form, setForm] = useState({
    subject_id: "",
    topic_id: "",
    study_date: "",
    hours: "",
    notes: "",
  });

  useEffect(() => {
    setStudent(getStudent());
  }, []);

  const loadSessions = (studentId) => {
    fetch(`http://localhost:8000/study_sessions?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setSessions(data.study_sessions || []));
  };

  const loadSubjects = (studentId) => {
    fetch(`http://localhost:8000/subjects?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setSubjects(data.subjects || []));
  };

  const loadTopics = (studentId) => {
    fetch(`http://localhost:8000/topics?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setTopics(data.topics || []));
  };

  useEffect(() => {
    if (student) {
      loadSessions(student.student_id);
      loadSubjects(student.student_id);
      loadTopics(student.student_id);
    }
  }, [student]);

  const subjectName = (id) => subjects.find((s) => s[0] === id)?.[2] || "Unknown";

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("Saving...");

    try {
      const res = await fetch("http://localhost:8000/study_sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: student.student_id,
          subject_id: Number(form.subject_id),
          topic_id: Number(form.topic_id),
          study_date: form.study_date,
          hours: Number(form.hours),
          notes: form.notes,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${JSON.stringify(data)}`);
        return;
      }

      setStatusMessage(data.message || "Session saved");
      setForm({ subject_id: "", topic_id: "", study_date: "", hours: "", notes: "" });
      loadSessions(student.student_id);
    } catch (err) {
      setStatusMessage(`Network error: ${err.message}`);
    }
  };

  if (!student) {
    return <p>Loading...</p>;
  }

  return (
    <div className={styles.layout}>
      <div className={styles.formCard}>
        <h2>Log a session</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label>Subject</label>
            <select name="subject_id" value={form.subject_id} onChange={handleChange} required>
              <option value="">Select subject</option>
              {subjects.map((s) => (
                <option key={s[0]} value={s[0]}>{s[2]}</option>
              ))}
            </select>
          </div>

          <div className={styles.field}>
            <label>Topic</label>
            <select name="topic_id" value={form.topic_id} onChange={handleChange} required>
              <option value="">Select topic</option>
              {topics
                .filter((t) => String(t[2]) === String(form.subject_id))
                .map((t) => (
                  <option key={t[0]} value={t[0]}>{t[3]}</option>
                ))}
            </select>
          </div>

          <div className={styles.field}>
            <label>Date</label>
            <input type="date" name="study_date" value={form.study_date} onChange={handleChange} required />
          </div>

          <div className={styles.field}>
            <label>Hours</label>
            <input type="number" step="0.1" name="hours" value={form.hours} onChange={handleChange} required />
          </div>

          <div className={styles.field}>
            <label>Notes</label>
            <textarea name="notes" value={form.notes} onChange={handleChange} rows={3} />
          </div>

          <button type="submit" className={styles.submitButton}>Save session</button>
        </form>

        {statusMessage && (
          <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>{statusMessage}</p>
        )}
      </div>

      <div>
        <h2>Recent sessions</h2>
        <div className={styles.logList}>
          {sessions.map((s) => (
            <div key={s[0]} className={styles.logEntry}>
              <span className={styles.logDate}>{s[4]}</span>
              <div className={styles.logBody}>
                <div>
                  <span className={styles.logSubject}>{subjectName(s[2])}</span>
                  {" — "}
                  <span className={styles.logHours}>{s[5]}h</span>
                </div>
                {s[6] && <div className={styles.logNotes}>{s[6]}</div>}
              </div>
            </div>
          ))}
          {sessions.length === 0 && <p>No sessions logged yet.</p>}
        </div>
      </div>
    </div>
  );
}