import Link from "next/link";
import styles from "./page.module.css";

export default function LandingPage() {
  return (
    <div className={styles.page}>
      <span className={styles.eyebrow}>A study record, kept like a field journal</span>
      <h1 className={styles.wordmark}>Marys Students Log</h1>
      <p className={styles.tagline}>
        Track study sessions, quiz scores, and goals in one place. Log in or
        create an account to open your dashboard.
      </p>

      <div className={styles.ctaRow}>
        <Link href="/login" className={styles.secondaryButton}>Log in</Link>
        <Link href="/register" className={styles.primaryButton}>Create an account</Link>
      </div>
    </div>
  );
}