"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { getStudent, isLoggedIn } from "../../lib/auth";

export default function QuizScoresPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [scores, setScores] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    subject_id: "",
    topic_id: "",
    score: "",
    total_marks: "",
    quiz_date: "",
  });

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  const loadScores = () => {
    api.getQuizScores().then((data) => setScores(data || [])).catch((err) => setStatusMessage(err.message));
  };
  const loadSubjects = () => {
    api.getSubjects().then((data) => setSubjects(data || [])).catch((err) => setStatusMessage(err.message));
  };
  const loadTopics = () => {
    api.getTopics().then((data) => setTopics(data || [])).catch((err) => setStatusMessage(err.message));
  };

  useEffect(() => {
    if (student) {
      loadScores();
      loadSubjects();
      loadTopics();
    }
  }, [student]);

  const topicName = (id) => topics.find((t) => t.topic_id === id)?.name || "Unknown";
  const subjectName = (id) => subjects.find((s) => s.subject_id === id)?.name || "Unknown";

  const scoreClass = (score, total) => {
    const pct = (score / total) * 100;
    if (pct >= 75) return styles.scoreHigh;
    if (pct >= 50) return styles.scoreMid;
    return styles.scoreLow;
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const resetForm = () => {
    setForm({ subject_id: "", topic_id: "", score: "", total_marks: "", quiz_date: "" });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    const payload = {
      subject_id: Number(form.subject_id),
      topic_id: Number(form.topic_id),
      score: Number(form.score),
      total_marks: Number(form.total_marks),
      quiz_date: form.quiz_date,
    };

    try {
      if (editingId) {
        await api.updateQuizScore(editingId, payload);
      } else {
        await api.createQuizScore(payload);
      }
      setStatusMessage(editingId ? "Score updated" : "Quiz score added");
      resetForm();
      loadScores();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleEdit = (q) => {
    setEditingId(q.score_id);
    setForm({
      subject_id: String(q.subject_id),
      topic_id: String(q.topic_id),
      score: String(q.score),
      total_marks: String(q.total_marks),
      quiz_date: q.quiz_date,
    });
  };

  const handleDelete = async (scoreId) => {
    if (!confirm("Delete this quiz score? This can't be undone.")) return;
    try {
      await api.deleteQuizScore(scoreId);
      loadScores();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  if (!student) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <div className={styles.header}>
        <span className={styles.eyebrow}>Readings</span>
        <h1>Quiz scores</h1>
      </div>

      <form onSubmit={handleSubmit} className={styles.formGrid}>
        <select name="subject_id" value={form.subject_id} onChange={handleChange} required>
          <option value="">Select subject</option>
          {subjects.map((s) => (
            <option key={s.subject_id} value={s.subject_id}>{s.name}</option>
          ))}
        </select>

        <select name="topic_id" value={form.topic_id} onChange={handleChange} required>
          <option value="">Select topic</option>
          {topics
            .filter((t) => String(t.subject_id) === String(form.subject_id))
            .map((t) => (
              <option key={t.topic_id} value={t.topic_id}>{t.name}</option>
            ))}
        </select>

        <input
          type="number"
          name="score"
          placeholder="Score"
          value={form.score}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="total_marks"
          placeholder="Out of"
          value={form.total_marks}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="quiz_date"
          value={form.quiz_date}
          onChange={handleChange}
          required
        />

        <button type="submit" className={styles.addButton}>
          {editingId ? "Update" : "Add score"}
        </button>
        {editingId && (
          <button type="button" className={styles.cancelButton} onClick={resetForm}>
            Cancel
          </button>
        )}
      </form>

      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}

      {scores.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No quiz scores logged yet</h3>
          <p>Add a score above to start tracking your quiz performance.</p>
        </div>
      ) : (
        <div className={styles.scoreList}>
          {scores.map((q) => (
            <div key={q.score_id} className={styles.scoreCard}>
              <div className={styles.scoreMain}>
                <div>
                  <div className={styles.scoreTopic}>{topicName(q.topic_id)}</div>
                  <div className={styles.scoreSubject}>{subjectName(q.subject_id)}</div>
                </div>
                <div className={`${styles.scoreValue} ${scoreClass(q.score, q.total_marks)}`}>
                  {q.score}/{q.total_marks}
                </div>
              </div>
              <div className={styles.scoreFooter}>
                <span className={styles.scoreDate}>{q.quiz_date}</span>
                <div className={styles.scoreActions}>
                  <button className={styles.actionButton} onClick={() => handleEdit(q)}>Edit</button>
                  <button
                    className={`${styles.actionButton} ${styles.deleteButton}`}
                    onClick={() => handleDelete(q.score_id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}