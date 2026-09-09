"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { getStudent, isLoggedIn } from "../../lib/auth";

export default function StudySessionsPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    subject_id: "",
    topic_id: "",
    study_date: "",
    hours: "",
    notes: "",
  });

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  const loadSessions = () => {
    api
      .getStudySessions()
      .then((data) => setSessions(data || []))
      .catch((err) => setStatusMessage(err.message));
  };
  const loadSubjects = () => {
    api
      .getSubjects()
      .then((data) => setSubjects(data || []))
      .catch((err) => setStatusMessage(err.message));
  };
  const loadTopics = () => {
    api
      .getTopics()
      .then((data) => setTopics(data || []))
      .catch((err) => setStatusMessage(err.message));
  };

  useEffect(() => {
    if (student) {
      loadSessions();
      loadSubjects();
      loadTopics();
    }
  }, [student]);

  const subjectName = (id) =>
    subjects.find((s) => s.subject_id === id)?.name || "Unknown";

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const resetForm = () => {
    setForm({
      subject_id: "",
      topic_id: "",
      study_date: "",
      hours: "",
      notes: "",
    });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("Saving...");

    const payload = {
      subject_id: Number(form.subject_id),
      topic_id: Number(form.topic_id),
      study_date: form.study_date,
      hours: Number(form.hours),
      notes: form.notes,
    };

    try {
      if (editingId) {
        await api.updateStudySession(editingId, payload);
      } else {
        await api.createStudySession(payload);
      }
      setStatusMessage(editingId ? "Session updated" : "Session saved");
      resetForm();
      loadSessions();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleEdit = (s) => {
    setEditingId(s.session_id);
    setForm({
      subject_id: String(s.subject_id),
      topic_id: String(s.topic_id),
      study_date: s.study_date,
      hours: String(s.hours),
      notes: s.notes || "",
    });
  };

  const handleDelete = async (sessionId) => {
    if (!confirm("Delete this session? This can't be undone.")) return;
    try {
      await api.deleteStudySession(sessionId);
      loadSessions();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  if (!student) {
    return <p>Loading...</p>;
  }

  return (
    <div className={styles.layout}>
      <div className={styles.formCard}>
        <h2>{editingId ? "Edit session" : "Log a session"}</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label>Subject</label>
            <select
              name="subject_id"
              value={form.subject_id}
              onChange={handleChange}
              required
            >
              <option value="">Select subject</option>
              {subjects.map((s) => (
                <option key={s.subject_id} value={s.subject_id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.field}>
            <label>Topic</label>
            <select
              name="topic_id"
              value={form.topic_id}
              onChange={handleChange}
              required
              disabled={!form.subject_id}
            >
              <option value="">
                {form.subject_id ? "Select topic" : "Select a subject first"}
              </option>
              {topics
                .filter((t) => String(t.subject_id) === String(form.subject_id))
                .map((t) => (
                  <option key={t.topic_id} value={t.topic_id}>
                    {t.name}
                  </option>
                ))}
            </select>
          </div>

          <div className={styles.field}>
            <label>Date</label>
            <input
              type="date"
              name="study_date"
              value={form.study_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className={styles.field}>
            <label>Hours</label>
            <input
              type="number"
              step="0.1"
              name="hours"
              value={form.hours}
              onChange={handleChange}
              required
            />
          </div>

          <div className={styles.field}>
            <label>Notes</label>
            <textarea
              name="notes"
              value={form.notes}
              onChange={handleChange}
              rows={3}
            />
          </div>

          <div className={styles.formButtons}>
            <button type="submit" className={styles.submitButton}>
              {editingId ? "Update session" : "Save session"}
            </button>
            {editingId && (
              <button
                type="button"
                className={styles.cancelButton}
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>

        {statusMessage && (
          <p className={styles.statusMessage}>{statusMessage}</p>
        )}
      </div>

      <div className={styles.logSection}>
        <h2>Recent sessions</h2>
        {sessions.length === 0 ? (
          <p className={styles.emptyText}>No sessions logged yet.</p>
        ) : (
          <div className={styles.logList}>
            {sessions.map((s) => (
              <div key={s.session_id} className={styles.logEntry}>
                <div className={styles.logHeader}>
                  <span className={styles.logDate}>{s.study_date}</span>
                  <div className={styles.logActions}>
                    <button
                      className={styles.actionButton}
                      onClick={() => handleEdit(s)}
                    >
                      Edit
                    </button>
                    <button
                      className={`${styles.actionButton} ${styles.deleteButton}`}
                      onClick={() => handleDelete(s.session_id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
                <div className={styles.logBody}>
                  <span className={styles.logSubject}>
                    {subjectName(s.subject_id)}
                  </span>
                  {" — "}
                  <span className={styles.logHours}>{s.hours}h</span>
                </div>
                {s.notes && <div className={styles.logNotes}>{s.notes}</div>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
