"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { api } from "../../../lib/api";
import { saveSession } from "../../../lib/auth";
import styles from "./page.module.css";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [needsVerification, setNeedsVerification] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setNeedsVerification(false);
    try {
      const data = await api.login(form);
      saveSession(data);
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
      if (err.message.toLowerCase().includes("verify")) setNeedsVerification(true);
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
              No account? <Link href="/register">Sign up</Link>
            </div>
          </div>

          <h1 className={styles.heading}>Sign in</h1>

          <form onSubmit={handleSubmit}>
            <div className={styles.field}>
              <label>Email</label>
              <input type="email" name="email" value={form.email} onChange={handleChange} required />
            </div>
            <div className={styles.field}>
              <div className={styles.labelRow}>
                <label>Password</label>
                <Link href="/forgot-password" className={styles.inlineLink}>Forgot password?</Link>
              </div>
              <input type="password" name="password" value={form.password} onChange={handleChange} required />
            </div>

            {error && <p className={styles.errorText}>{error}</p>}
            {needsVerification && (
              <p className={styles.switchLink}>
                <Link href={`/verify-otp?email=${encodeURIComponent(form.email)}`}>Verify your email</Link>
              </p>
            )}

            <button type="submit" className={styles.submitButton}>Sign in</button>
          </form>
        </div>

        <div className={styles.illustration}>
          <Image src="/image.png" alt="" width={420} height={420} priority className={styles.illustrationImg} />
        </div>
      </div>
    </div>
  );
}