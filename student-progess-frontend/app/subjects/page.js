"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { getStudent, isLoggedIn } from "../../lib/auth";

export default function SubjectsPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [name, setName] = useState("");
  const [color, setColor] = useState("#3F6B4F");
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  const loadSubjects = () => {
    api.getSubjects()
      .then((data) => setSubjects(data || []))
      .catch((err) => setStatusMessage(err.message));
  };

  useEffect(() => {
    if (student) loadSubjects();
  }, [student]);

  const resetForm = () => {
    setName("");
    setColor("#3F6B4F");
    setEditingId(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");
    try {
      if (editingId) {
        await api.updateSubject(editingId, { name, color });
      } else {
        await api.createSubject({ name, color });
      }
      resetForm();
      loadSubjects();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleEdit = (subject) => {
    setEditingId(subject.subject_id);
    setName(subject.name);
    setColor(subject.color || "#3F6B4F");
    setShowForm(true);
  };

  const handleDelete = async (subjectId) => {
    if (!confirm("Delete this subject? This can't be undone.")) return;
    try {
      await api.deleteSubject(subjectId);
      loadSubjects();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const toggleFavorite = async (subject) => {
    try {
      await api.updateSubject(subject.subject_id, { is_favorite: !subject.is_favorite });
      loadSubjects();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  if (!student) {
    return <p>Loading...</p>;
  }

  const sorted = [...subjects].sort((a, b) => (b.is_favorite ? 1 : 0) - (a.is_favorite ? 1 : 0));

  return (
    <div>
      <div className={styles.header}>
        <div>
          <span className={styles.eyebrow}>Catalog</span>
          <h1>Subjects</h1>
        </div>
        <button
          className={styles.addButton}
          onClick={() => (showForm ? resetForm() : setShowForm(true))}
        >
          {showForm ? "Cancel" : "+ Add subject"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className={styles.formRow}>
          <input
            type="text"
            placeholder="Subject name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input type="color" value={color} onChange={(e) => setColor(e.target.value)} />
          <button type="submit" className={styles.addButton}>
            {editingId ? "Update" : "Save"}
          </button>
        </form>
      )}

      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}

      {sorted.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No subjects logged yet</h3>
          <p>Add your first subject to start tracking study sessions against it.</p>
        </div>
      ) : (
        <div className={styles.grid}>
          {sorted.map((s) => (
            <div key={s.subject_id} className={styles.specimenCard}>
              <button
                className={styles.favoriteButton}
                onClick={() => toggleFavorite(s)}
                aria-label={s.is_favorite ? "Unfavorite" : "Favorite"}
              >
                {s.is_favorite ? "★" : "☆"}
              </button>

              <span className={styles.colorTag} style={{ background: s.color || "#3F6B4F" }} />
              <div className={styles.subjectName}>{s.name}</div>
              <div className={styles.subjectMeta}>ID {String(s.subject_id).padStart(3, "0")}</div>

              <div className={styles.cardActions}>
                <button className={styles.actionButton} onClick={() => handleEdit(s)}>Edit</button>
                <button
                  className={`${styles.actionButton} ${styles.deleteButton}`}
                  onClick={() => handleDelete(s.subject_id)}
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