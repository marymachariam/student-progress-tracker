import styles from "./StatCard.module.css";

export default function StatCard({ label, value, subtext }) {
  return (
    <div className={styles.statCard}>
      <span className={styles.label}>{label}</span>
      <span className={styles.value}>{value}</span>
      {subtext && <span className={styles.subtext}>{subtext}</span>}
    </div>
  );
}