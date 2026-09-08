"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { api } from "../../../lib/api";
import styles from "../login/page.module.css";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.register(form);
      router.push(`/verify-otp?email=${encodeURIComponent(form.email)}`);
    } catch (err) {
      setError(err.message);
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
          <p className={styles.subtitle}>Start your study record.</p>

          <form onSubmit={handleSubmit}>
            <div className={styles.field}>
              <label>Name</label>
              <input type="text" name="name" value={form.name} onChange={handleChange} required />
            </div>
            <div className={styles.field}>
              <label>Email</label>
              <input type="email" name="email" value={form.email} onChange={handleChange} required />
            </div>
            <div className={styles.field}>
              <label>Password</label>
              <input type="password" name="password" value={form.password} onChange={handleChange} required />
              <span className={styles.hint}>8+ characters, with uppercase, lowercase, and a number.</span>
            </div>

            {error && <p className={styles.errorText}>{error}</p>}
            <button type="submit" className={styles.submitButton}>Create account</button>
          </form>

          <div className={styles.switchLink}>Already have an account? <Link href="/login">Log in</Link></div>
        </div>
      </div>
    </div>
  );
}