"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import { isLoggedIn } from "../../lib/auth";

export default function RecommendationsPage() {
  const router = useRouter();
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [speaking, setSpeaking] = useState(false);
  const utteranceRef = useRef(null);

  const load = () => {
    setLoading(true);
    setError("");
    api
      .getRecommendation()
      .then(setRecommendation)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    load();
    return () => {
      window.speechSynthesis?.cancel();
    };
  }, [router]);

  const handleListen = () => {
    if (!recommendation?.recommendation) return;

    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(
      recommendation.recommendation,
    );
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    utteranceRef.current = utterance;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  };

  const weakest = recommendation?.based_on?.weakest_topic;
  const alerts = recommendation?.based_on?.alerts || [];

  return (
    <div>
      <div className={styles.header}>
        <span className={styles.eyebrow}>Powered by AI</span>
        <h1>Recommendations</h1>
      </div>

      {loading && (
        <p className={styles.loadingText}>Analyzing your progress…</p>
      )}
      {error && <p className={styles.errorText}>{error}</p>}

      {recommendation && !loading && (
        <>
          <div className={styles.recCard}>
            <div className={styles.recTop}>
              <span className={styles.sourceBadge}>
                {recommendation.source === "ai" && "✦ AI-generated"}
                {recommendation.source === "cached" &&
                  "↻ Last AI response (temporarily unavailable)"}
                {recommendation.source === "fallback" &&
                  "◈ Basic tip (AI unavailable)"}
              </span>
              <button
                className={`${styles.listenButton} ${speaking ? styles.listenButtonActive : ""}`}
                onClick={handleListen}
              >
                {speaking ? "■ Stop" : "▶ Listen"}
              </button>
            </div>
            <p className={styles.recText}>{recommendation.recommendation}</p>
          </div>

          {(weakest || alerts.length > 0) && (
            <div className={styles.basisSection}>
              <h2 className={styles.basisTitle}>Based on</h2>
              <div className={styles.basisGrid}>
                {weakest && (
                  <div className={styles.basisCard}>
                    <span className={styles.basisLabel}>Weakest topic</span>
                    <span className={styles.basisValue}>{weakest.topic}</span>
                    <span className={styles.basisMeta}>
                      {weakest.average_score_percent}% average
                    </span>
                  </div>
                )}
                {alerts.slice(0, 3).map((a, i) => (
                  <div key={i} className={styles.basisCard}>
                    <span className={styles.basisLabel}>Alert</span>
                    <span className={styles.basisValue}>
                      {a.type === "goal_behind_schedule" && a.goal}
                      {a.type === "subject_inactive" && a.subject}
                      {a.type === "no_sessions_logged" && a.subject}
                    </span>
                    <span className={styles.basisMeta}>
                      {a.type === "goal_behind_schedule" &&
                        "Falling behind schedule"}
                      {a.type === "subject_inactive" &&
                        `Inactive ${a.days_since_last_session} days`}
                      {a.type === "no_sessions_logged" &&
                        "No sessions logged yet"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button className={styles.refreshButton} onClick={load}>
            ↻ Get a new recommendation
          </button>
        </>
      )}
    </div>
  );
}
