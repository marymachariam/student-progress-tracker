"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
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
    <div className={styles.page}>
      <div className={styles.authWrap}>
        <div className={styles.card}>
          <div className={styles.cardTop}>
            <div className={styles.wordmark}>
              <span className={styles.wordmarkIcon}>◈</span>
              Field Log<span className={styles.dot}>.</span>
            </div>
            <div className={styles.topLink}>
              Remembered it? <Link href="/login">Sign in</Link>
            </div>
          </div>

          <h1 className={styles.heading}>Reset password</h1>
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
            {message && <p className={styles.switchLink}>{message}</p>}

            <button type="submit" className={styles.submitButton}>Send reset link</button>
          </form>
        </div>

        <div className={styles.illustration}>
          <Image src="/image.png" alt="" width={420} height={420} priority className={styles.illustrationImg} />
        </div>
      </div>
    </div>
  );
}