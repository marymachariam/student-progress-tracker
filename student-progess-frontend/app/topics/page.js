"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";
import { getStudent } from "../../lib/auth";

export default function TopicsPage() {
  const [student, setStudent] = useState(null);
  const [topics, setTopics] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [name, setName] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    setStudent(getStudent());
  }, []);

  const loadTopics = (studentId) => {
    fetch(`http://localhost:8000/topics?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setTopics(data.topics || []));
  };

  const loadSubjects = (studentId) => {
    fetch(`http://localhost:8000/subjects?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setSubjects(data.subjects || []));
  };

  useEffect(() => {
    if (student) {
      loadTopics(student.student_id);
      loadSubjects(student.student_id);
    }
  }, [student]);

  const subjectName = (id) => {
    const match = subjects.find((s) => s[0] === id);
    return match ? match[2] : "Unknown";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    try {
      const res = await fetch("http://localhost:8000/topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: student.student_id,
          subject_id: Number(subjectId),
          name,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${JSON.stringify(data)}`);
        return;
      }

      setStatusMessage(data.message || "Topic added");
      setName("");
      setSubjectId("");
      loadTopics(student.student_id);
    } catch (err) {
      setStatusMessage(`Network error: ${err.message}`);
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
            <option key={s[0]} value={s[0]}>{s[2]}</option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Topic name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <button type="submit" className={styles.addButton}>Add topic</button>
      </form>

      {statusMessage && (
        <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>{statusMessage}</p>
      )}

      <div className={styles.list}>
        {topics.map((t) => (
          <div key={t[0]} className={styles.row}>
            <span className={styles.topicName}>{t[3]}</span>
            <span className={styles.subjectBadge}>{subjectName(t[2])}</span>
          </div>
        ))}
        {topics.length === 0 && <p>No topics added yet.</p>}
      </div>
    </div>
  );
}