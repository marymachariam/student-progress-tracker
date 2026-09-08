"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { api } from "../../../lib/api";
import styles from "../login/page.module.css";

export default function ResetPasswordPage() {
  const router = useRouter();
  const params = useSearchParams();
  const token = params.get("token") || "";
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.resetPassword({ token, new_password: newPassword });
      router.push("/login");
    } catch (err) {
      setError(err.message);
    }
  };

  if (!token) {
    return (
      <div className={styles.container}>
        <div className={styles.card}>
          <p className={styles.errorText}>Missing or invalid reset link.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.wordmark}>Field Log</div>
        <p className={styles.subtitle}>Choose a new password.</p>

        <form onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label>New password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className={styles.errorText}>{error}</p>}

          <button type="submit" className={styles.submitButton}>Reset password</button>
        </form>
      </div>
    </div>
  );
}