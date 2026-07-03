"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState([]);
  const [name, setName] = useState("");
  const [color, setColor] = useState("#3F6B4F");
  const [showForm, setShowForm] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const loadSubjects = () => {
    fetch("http://localhost:8000/subjects")
      .then((res) => res.json())
      .then((data) => setSubjects(data.subjects || []));
  };

  useEffect(() => {
    loadSubjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    try {
      const res = await fetch("http://localhost:8000/subjects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: 1, name, color }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${JSON.stringify(data)}`);
        return;
      }

      setStatusMessage(data.message || "Subject added");
      setName("");
      setShowForm(false);
      loadSubjects();
    } catch (err) {
      setStatusMessage(`Network error: ${err.message}`);
    }
  };

  return (
    <div>
      <div className={styles.header}>
        <div>
          <span className={styles.eyebrow}>Catalog</span>
          <h1>Subjects</h1>
        </div>
        <button className={styles.addButton} onClick={() => setShowForm(!showForm)}>
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
          <button type="submit" className={styles.addButton}>Save</button>
        </form>
      )}

      {statusMessage && (
        <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>{statusMessage}</p>
      )}

      {subjects.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No subjects logged yet</h3>
          <p>Add your first subject to start tracking study sessions against it.</p>
        </div>
      ) : (
        <div className={styles.grid}>
          {subjects.map((s) => (
            <div key={s[0]} className={styles.specimenCard}>
              <span className={styles.colorTag} style={{ background: s[3] || "#3F6B4F" }} />
              <div className={styles.subjectName}>{s[2]}</div>
              <div className={styles.subjectMeta}>ID {String(s[0]).padStart(3, "0")}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}