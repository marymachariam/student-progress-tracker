import Link from "next/link";
import styles from "./page.module.css";

const FEATURES = [
  {
    icon: "◈",
    title: "Track everything in one place",
    description: "Subjects, topics, study sessions, and quiz scores logged and organized as you go.",
  },
  {
    icon: "◆",
    title: "Set goals that predict themselves",
    description: "Set an hours-based goal and see, in real time, whether your current pace will actually hit it.",
  },
  {
    icon: "✦",
    title: "AI-powered recommendations",
    description: "Get a personalized suggestion on what to review next, based on your weakest topics and recent activity.",
  },
  {
    icon: "◷",
    title: "Weekly progress digest",
    description: "A summary emailed every week hours studied, quiz trends, and goals falling behind.",
  },
];

export default function LandingPage() {
  return (
    <div className={styles.landing}>
      <div className={styles.hero}>
        <span className={styles.eyebrow}>A study record, kept like a field journal</span>
        <h1 className={styles.heroTitle}>Marys Students Log</h1>
        <p className={styles.heroSubtitle}>
          Track study sessions, quiz scores, and goals in one place.
          Log in or create an account to open your dashboard.
        </p>
        <div className={styles.heroActions}>
          <Link href="/login" className={styles.secondaryButton}>Log in</Link>
          <Link href="/register" className={styles.primaryButton}>Create an account</Link>
        </div>
      </div>

      <div className={styles.featureGrid}>
        {FEATURES.map((feature) => (
          <div key={feature.title} className={styles.featureCard}>
            <div className={styles.featureIcon}>{feature.icon}</div>
            <h3 className={styles.featureTitle}>{feature.title}</h3>
            <p className={styles.featureDescription}>{feature.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}