"use client";

import { useState } from "react";
import Link from "next/link";
import { api } from "../../../lib/api";
import styles from "../login/page.module.css";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      const data = await api.forgotPassword({ email });
      setMessage(data.message);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.wordmark}>Field Log</div>
        <p className={styles.subtitle}>We&apos;ll email you a reset link.</p>

        <form onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {error && <p className={styles.errorText}>{error}</p>}
          {message && <p className={styles.subtitle}>{message}</p>}

          <button type="submit" className={styles.submitButton}>Send reset link</button>
        </form>

        <div className={styles.switchLink}>
          <Link href="/login">Back to login</Link>
        </div>
      </div>
    </div>
  );
}