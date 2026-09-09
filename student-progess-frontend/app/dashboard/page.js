"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import StatCard from "../components/StatCard";
import GrowthRing from "../components/GrowthRing";
import { getStudent, isLoggedIn } from "../../lib/auth";
import { api } from "../../lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [stats, setStats] = useState(null);
  const [goals, setGoals] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    setStudent(getStudent());
  }, [router]);

  useEffect(() => {
    if (!student) return;

    api.getDashboard().then(setStats).catch(() => {});
    api.getGoalProgress().then((data) => setGoals(data || [])).catch(() => {});
    api.getAlerts().then((data) => setAlerts(data || [])).catch(() => {});
  }, [student]);

  return (
    <div>
      <div className={styles.header}>
        <span className={styles.eyebrow}>Overview</span>
        <h1>Dashboard</h1>
      </div>

      {stats && (
        <div className={styles.statGrid}>
          <StatCard label="Hours studied" value={stats.total_hours_studied} />
          <StatCard label="Avg quiz score" value={`${stats.average_quiz_score_percent}%`} />
          <StatCard label="Active goals" value={stats.active_goals} />
          <StatCard label="Completed goals" value={stats.completed_goals} />
          <StatCard label="Top subject" value={stats.top_subject} />
        </div>
      )}

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>Goal progress</h2>
        <div className={styles.goalGrid}>
          {goals.map((g) => (
            <div key={g.goal_id} className={styles.goalCard}>
              <GrowthRing
                title={g.title}
                percent={g.percent_complete}
                actual={g.actual_progress}
                target={g.target_value}
              />
            </div>
          ))}
          {goals.length === 0 && <p>No active goals yet.</p>}
        </div>
      </div>

      {alerts.length > 0 && (
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>Alerts</h2>
          <div className={styles.alertList}>
            {alerts.map((a, i) => (
              <div key={i} className={styles.alertItem}>
                {a.type === "goal_behind_schedule" &&
                  `"${a.goal}" is behind — expected ${a.expected_by_now} by now, at ${a.actual}.`}
                {a.type === "subject_inactive" &&
                  `No sessions logged for ${a.subject} in ${a.days_since_last_session} days.`}
                {a.type === "no_sessions_logged" &&
                  `No sessions logged yet for ${a.subject}.`}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}