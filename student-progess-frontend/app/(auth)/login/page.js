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
    <div className={styles.split}>
      <div className={styles.imageSide}>
        <Image src="/image.png" alt="" fill priority className={styles.image} />
        <div className={styles.imageOverlay} />
      </div>

      <div className={styles.formSide}>
        <div className={styles.card}>
          <div className={styles.wordmark}>Field Log</div>
          <p className={styles.subtitle}>Log in to your study record.</p>

          <form onSubmit={handleSubmit}>
            <div className={styles.field}>
              <label>Email</label>
              <input type="email" name="email" value={form.email} onChange={handleChange} required />
            </div>
            <div className={styles.field}>
              <label>Password</label>
              <input type="password" name="password" value={form.password} onChange={handleChange} required />
            </div>

            {error && <p className={styles.errorText}>{error}</p>}
            {needsVerification && (
              <p className={styles.switchLink}>
                <Link href={`/verify-otp?email=${encodeURIComponent(form.email)}`}>Verify your email</Link>
              </p>
            )}

            <button type="submit" className={styles.submitButton}>Log in</button>
          </form>

          <div className={styles.switchLink}>No account? <Link href="/register">Register</Link></div>
          <div className={styles.switchLink}><Link href="/forgot-password">Forgot password?</Link></div>
        </div>
      </div>
    </div>
  );
}