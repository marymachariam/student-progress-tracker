"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { getStudent, isLoggedIn } from "../../lib/auth";

export default function GoalsPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [goals, setGoals] = useState([]);
  const [statusMessage, setStatusMessage] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [goalUpdating, setGoalUpdating] = useState(null);
  const [progressInput, setProgressInput] = useState("");

  const [form, setForm] = useState({
    title: "",
    target_type: "hours",
    target_value: "",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  const loadGoals = () => {
    api.getGoals().then((data) => setGoals(data || [])).catch((err) => setStatusMessage(err.message));
  };

  useEffect(() => {
    if (student) {
      loadGoals();
    }
  }, [student]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const resetForm = () => {
    setForm({ title: "", target_type: "hours", target_value: "", start_date: "", end_date: "" });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatusMessage("");

    const payload = {
      title: form.title,
      target_type: form.target_type,
      target_value: Number(form.target_value),
      start_date: form.start_date,
      end_date: form.end_date,
    };

    try {
      if (editingId) {
        await api.updateGoal(editingId, payload);
      } else {
        await api.createGoal(payload);
      }
      setStatusMessage(editingId ? "Goal updated" : "Goal added");
      resetForm();
      loadGoals();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleEdit = (g) => {
    setEditingId(g.goal_id);
    setForm({
      title: g.title,
      target_type: g.target_type,
      target_value: String(g.target_value),
      start_date: g.start_date,
      end_date: g.end_date,
    });
  };

  const handleDelete = async (goalId) => {
    if (!confirm("Delete this goal? This can't be undone.")) return;
    try {
      await api.deleteGoal(goalId);
      loadGoals();
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleUpdateProgress = async (goalId, value) => {
    try {
      await api.updateGoal(goalId, { current_value: Number(value) });
      setGoalUpdating(null);
      loadGoals();
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
          <option value="topics">Topics</option>
          <option value="quizzes">Quizzes</option>
          <option value="sessions">Sessions</option>
        </select>

        <input
          type="number"
          name="target_value"
          placeholder="Target"
          value={form.target_value}
          onChange={handleChange}
          required
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

        <button type="submit" className={styles.addButton}>
          {editingId ? "Update" : "Add goal"}
        </button>
        {editingId && (
          <button type="button" className={styles.cancelButton} onClick={resetForm}>
            Cancel
          </button>
        )}
      </form>

      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}

      {goals.length === 0 ? (
        <div className={styles.emptyState}>
          <h3>No goals set yet</h3>
          <p>Add a goal above to start tracking progress toward it.</p>
        </div>
      ) : (
        <div className={styles.list}>
          {goals.map((g) => (
            <div key={g.goal_id} className={styles.row}>
              <div className={styles.rowMain}>
                <div>
                  <div className={styles.goalTitle}>{g.title}</div>
                  <div className={styles.goalDates}>{g.start_date} → {g.end_date}</div>
                </div>
                <div className={styles.typeBadge}>{g.target_value} {g.target_type}</div>
                {goalUpdating === g.goal_id ? (
                  <form
                    className={styles.progressForm}
                    onSubmit={(e) => {
                      e.preventDefault();
                      handleUpdateProgress(g.goal_id, progressInput);
                    }}
                  >
                    <input
                      type="number"
                      value={progressInput}
                      onChange={(e) => setProgressInput(e.target.value)}
                      placeholder="Current progress"
                      autoFocus
                    />
                    <button type="submit" className={styles.actionButton}>Save</button>
                    <button type="button" className={styles.actionButton} onClick={() => setGoalUpdating(null)}>Cancel</button>
                  </form>
                ) : (
                  <button
                    className={styles.actionButton}
                    onClick={() => { setGoalUpdating(g.goal_id); setProgressInput(""); }}
                  >
                    Update progress
                  </button>
                )}
              </div>
              <div className={styles.rowActions}>
                <button className={styles.actionButton} onClick={() => handleEdit(g)}>Edit</button>
                <button
                  className={`${styles.actionButton} ${styles.deleteButton}`}
                  onClick={() => handleDelete(g.goal_id)}
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