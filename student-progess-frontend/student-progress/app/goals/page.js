"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";
import GrowthRing from "../components/GrowthRing";
import { getStudent } from "../../lib/auth";

export default function GoalsPage() {
  const [student, setStudent] = useState(null);
  const [goals, setGoals] = useState([]);
  const [progress, setProgress] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");

  const [form, setForm] = useState({
    title: "",
    target_type: "hours",
    target_value: "",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    setStudent(getStudent());
  }, []);

  const loadGoals = (studentId) => {
    fetch(`http://localhost:8000/goals?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setGoals(data.goals || []));
  };

  const loadProgress = (studentId) => {
    fetch(`http://localhost:8000/dashboard/goal-progress?student_id=${studentId}`)
      .then((res) => res.json())
      .then((data) => setProgress(data.goal_progress || []));
  };

  useEffect(() => {
    if (student) {
      loadGoals(student.student_id);
      loadProgress(student.student_id);
    }
  }, [student]);

  const progressFor = (goalId) => progress.find((p) => p.goal_id === goalId);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    try {
      const res = await fetch("http://localhost:8000/goals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: student.student_id,
          title: form.title,
          target_type: form.target_type,
          target_value: Number(form.target_value),
          start_date: form.start_date,
          end_date: form.end_date,
          is_completed: 0,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${JSON.stringify(data)}`);
        return;
      }

      setStatusMessage(data.message || "Goal added");
      setForm({ title: "", target_type: "hours", target_value: "", start_date: "", end_date: "" });
      loadGoals(student.student_id);
      loadProgress(student.student_id);
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
        <span className={styles.eyebrow}>Targets</span>
        <h1>Goals</h1>
      </div>

      <form onSubmit={handleSubmit} className={styles.formRow}>
        <input
          type="text"
          name="title"
          placeholder="Goal title"
          value={form.title}
          onChange={handleChange}
          required
        />

        <select name="target_type" value={form.target_type} onChange={handleChange}>
          <option value="hours">Hours</option>
        </select>

        <input
          type="number"
          step="0.1"
          name="target_value"
          placeholder="Target"
          value={form.target_value}
          onChange={handleChange}
          required
          style={{ width: "90px" }}
        />

        <input
          type="date"
          name="start_date"
          value={form.start_date}
          onChange={handleChange}
          required
        />

        <input
          type="date"
          name="end_date"
          value={form.end_date}
          onChange={handleChange}
          required
        />

        <button type="submit" className={styles.addButton}>Add goal</button>
      </form>

      {statusMessage && (
        <p style={{ marginBottom: "1rem", fontSize: "0.85rem" }}>{statusMessage}</p>
      )}

      {goals.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No goals set yet</h3>
          <p>Add a goal to start tracking progress toward it.</p>
        </div>
      ) : (
        <div className={styles.goalGrid}>
          {goals.map((g) => {
            const p = progressFor(g[0]);
            return (
              <div key={g[0]} className={styles.goalCard}>
                <GrowthRing
                  title={g[2]}
                  percent={p ? p.percent_complete : 0}
                  actual={p ? p.actual_progress : 0}
                  target={g[4]}
                />
                <div className={styles.goalDates}>{g[5]} → {g[6]}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}