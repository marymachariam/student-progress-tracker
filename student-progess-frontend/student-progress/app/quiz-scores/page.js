"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

export default function QuizScoresPage() {
  const [scores, setScores] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");

  const [form, setForm] = useState({
    subject_id: "",
    topic_id: "",
    score: "",
    total_marks: "",
    quiz_date: "",
  });

  const loadScores = () => {
    fetch("http://localhost:8000/quiz_scores")
      .then((res) => res.json())
      .then((data) => setScores(data.quiz_scores || []));
  };

  useEffect(() => {
    loadScores();
    fetch("http://localhost:8000/subjects")
      .then((res) => res.json())
      .then((data) => setSubjects(data.subjects || []));
    fetch("http://localhost:8000/topics")
      .then((res) => res.json())
      .then((data) => setTopics(data.topics || []));
  }, []);

  const topicName = (id) => topics.find((t) => t[0] === id)?.[3] || "Unknown";

  const scoreClass = (score, total) => {
    const pct = (score / total) * 100;
    if (pct >= 75) return styles.scoreHigh;
    if (pct >= 50) return styles.scoreMid;
    return styles.scoreLow;
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    try {
      const res = await fetch("http://localhost:8000/quiz_scores", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: 1,
          subject_id: Number(form.subject_id),
          topic_id: Number(form.topic_id),
          score: Number(form.score),
          total_marks: Number(form.total_marks),
          quiz_date: form.quiz_date,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${JSON.stringify(data)}`);
        return;
      }

      setStatusMessage(data.message || "Quiz score added");
      setForm({ subject_id: "", topic_id: "", score: "", total_marks: "", quiz_date: "" });
      loadScores();
    } catch (err) {
      setStatusMessage(`Network error: ${err.message}`);
    }
  };

  return (
    <div>
      <div className={styles.header}>
        <span className={styles.eyebrow}>Readings</span>
        <h1>Quiz scores</h1>
      </div>

      <form onSubmit={handleSubmit} className={styles.formRow}>
        <select name="subject_id" value={form.subject_id} onChange={handleChange} required>
          <option value="">Select subject</option>
          {subjects.map((s) => (
            <option key={s[0]} value={s[0]}>{s[2]}</option>
          ))}
        </select>

        <select name="topic_id" value={form.topic_id} onChange={handleChange} required>
          <option value="">Select topic</option>
          {topics
            .filter((t) => String(t[2]) === String(form.subject_id))
            .map((t) => (
              <option key={t[0]} value={t[0]}>{t[3]}</option>
            ))}
        </select>

        <input
          type="number"
          name="score"
          placeholder="Score"
          value={form.score}
          onChange={handleChange}
          required
          style={{ width: "90px" }}
        />
        <input
          type="number"
          name="total_marks"
          placeholder="Out of"
          value={form.total_marks}
          onChange={handleChange}
          required
          style={{ width: "90px" }}
        />
        <input
          type="date"
          name="quiz_date"
          value={form.quiz_date}
          onChange={handleChange}
          required
        />

        <button type="submit" className={styles.addButton}>Add score</button>
      </form>

      {statusMessage && (
        <p style={{ marginBottom: "1rem", fontSize: "0.85rem" }}>{statusMessage}</p>
      )}
    <div className={styles.tableWrapper}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Topic</th>
            <th>Score</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {scores.map((q) => (
            <tr key={q[0]}>
              <td>{topicName(q[3])}</td>
              <td className={`${styles.scoreValue} ${scoreClass(q[4], q[5])}`}>
                {q[4]}/{q[5]}
              </td>
              <td>{q[6]}</td>
            </tr>
          ))}
          {scores.length === 0 && (
            <tr><td colSpan={3}>No quiz scores logged yet.</td></tr>
          )}
        </tbody>
      </table>
      </div>
    </div>
  );
}