"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { getStudent, isLoggedIn } from "../../lib/auth";

export default function TopicsPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [topics, setTopics] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [name, setName] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  const loadTopics = () => {
    api.getTopics().then((data) => setTopics(data || [])).catch((err) => setStatusMessage(err.message));
  };

  const loadSubjects = () => {
    api.getSubjects().then((data) => setSubjects(data || [])).catch((err) => setStatusMessage(err.message));
  };

  useEffect(() => {
    if (student) {
      loadTopics();
      loadSubjects();
    }
  }, [student]);

  const subjectName = (id) => {
    const match = subjects.find((s) => s.subject_id === id);
    return match ? match.name : "Unknown";
  };

  const resetForm = () => {
    setName("");
    setSubjectId("");
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");
    try {
      if (editingId) {
        await api.updateTopic(editingId, { name, subject_id: Number(subjectId) });
      } else {
        await api.createTopic({ name, subject_id: Number(subjectId) });
      }
      resetForm();
      loadTopics();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleEdit = (topic) => {
    setEditingId(topic.topic_id);
    setName(topic.name);
    setSubjectId(String(topic.subject_id));
  };

  const handleDelete = async (topicId) => {
    if (!confirm("Delete this topic? This can't be undone.")) return;
    try {
      await api.deleteTopic(topicId);
      loadTopics();
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
        <span className={styles.eyebrow}>Index</span>
        <h1>Topics</h1>
      </div>

      <form onSubmit={handleSubmit} className={styles.formRow}>
        <select value={subjectId} onChange={(e) => setSubjectId(e.target.value)} required>
          <option value="">Select subject</option>
          {subjects.map((s) => (
            <option key={s.subject_id} value={s.subject_id}>{s.name}</option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Topic name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <button type="submit" className={styles.addButton}>
          {editingId ? "Update topic" : "Add topic"}
        </button>
        {editingId && (
          <button type="button" className={styles.cancelButton} onClick={resetForm}>
            Cancel
          </button>
        )}
      </form>

      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}

      {topics.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No topics added yet</h3>
          <p>Add a topic under one of your subjects to start tracking it.</p>
        </div>
      ) : (
        <div className={styles.list}>
          {topics.map((t) => (
            <div key={t.topic_id} className={styles.row}>
              <div className={styles.rowMain}>
                <span className={styles.topicName}>{t.name}</span>
                <span className={styles.subjectBadge}>{subjectName(t.subject_id)}</span>
              </div>
              <div className={styles.rowActions}>
                <button className={styles.actionButton} onClick={() => handleEdit(t)}>Edit</button>
                <button
                  className={`${styles.actionButton} ${styles.deleteButton}`}
                  onClick={() => handleDelete(t.topic_id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}