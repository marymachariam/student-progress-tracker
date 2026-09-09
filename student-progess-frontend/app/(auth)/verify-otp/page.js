"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Image from "next/image";
import { api } from "../../../lib/api";
import styles from "../login/page.module.css";

export default function VerifyOtpPage() {
  const router = useRouter();
  const params = useSearchParams();
  const email = params.get("email") || "";
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.verifyOtp({ email, code });
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  const handleResend = async () => {
    setError("");
    setMessage("");
    try {
      await api.resendOtp({ email, purpose: "email_verification" });
      setMessage("A new code has been sent.");
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
          </div>

          <h1 className={styles.heading}>Verify email</h1>
          <p className={styles.subtitle}>Enter the code sent to {email}.</p>

          <form onSubmit={handleSubmit}>
            <div className={styles.field}>
              <label>Verification code</label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                maxLength={6}
                required
              />
            </div>

            {error && <p className={styles.errorText}>{error}</p>}
            {message && <p className={styles.switchLink}>{message}</p>}

            <button type="submit" className={styles.submitButton}>Verify</button>
          </form>

          <div className={styles.switchLink}>
            <button onClick={handleResend} className={styles.inlineLink} style={{ background: "none", border: "none", cursor: "pointer" }}>
              Resend code
            </button>
          </div>
        </div>

        <div className={styles.illustration}>
          <Image src="/image.png" alt="" width={420} height={420} priority className={styles.illustrationImg} />
        </div>
      </div>
    </div>
  );
}