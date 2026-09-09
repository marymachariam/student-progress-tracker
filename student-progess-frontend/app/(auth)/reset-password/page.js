"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Image from "next/image";
import { api } from "../../../lib/api";
import styles from "../login/page.module.css";

// 1. This handles the form and the useSearchParams() hook safely inside Suspense
function ResetPasswordForm() {
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

  return (
    <div className={styles.authWrap}>
      <div className={styles.card}>
        <div className={styles.cardTop}>
          <div className={styles.wordmark}>
            <span className={styles.wordmarkIcon}>◈</span>
            Field Log<span className={styles.dot}>.</span>
          </div>
        </div>

        <h1 className={styles.heading}>New password</h1>
        <p className={styles.subtitle}>Choose a new password for your account.</p>

        {!token ? (
          <p className={styles.errorText}>Missing or invalid reset link.</p>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className={styles.field}>
              <label>New password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <span className={styles.hint}>8+ characters, with uppercase, lowercase, and a number.</span>
            </div>

            {error && <p className={styles.errorText}>{error}</p>}

            <button type="submit" className={styles.submitButton}>Reset password</button>
          </form>
        )}
      </div>

      <div className={styles.illustration}>
        <Image src="/image.png" alt="" width={420} height={420} priority className={styles.illustrationImg} />
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className={styles.page}>
      <Suspense fallback={
        <div className={styles.authWrap}>
          <div className={styles.card}>
            <p className={styles.subtitle}>Loading reset options...</p>
          </div>
        </div>
      }>
        <ResetPasswordForm />
      </Suspense>
    </div>
  );
}
