"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import styles from "./page.module.css";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch("http://localhost:8000/register_student", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    router.push("/login");
  };

  return (
    <div className={styles.container}>
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
          </div>

          <button type="submit" className={styles.submitButton}>Create account</button>
        </form>

        <div className={styles.switchLink}>
          Already have an account? <Link href="/login">Log in</Link>
        </div>
      </div>
    </div>
  );
}