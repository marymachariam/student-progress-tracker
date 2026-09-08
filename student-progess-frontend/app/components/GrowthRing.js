import styles from "./GrowthRing.module.css";

export default function GrowthRing({ title, percent, actual, target, onTrack }) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.min(Math.max(percent, 0), 100);
  const offset = circumference - (clamped / 100) * circumference;

  return (
    <div className={styles.wrapper}>
      <svg width="90" height="90" viewBox="0 0 90 90">
        <circle cx="45" cy="45" r={radius} className={styles.ringTrack} />
        <circle
          cx="45" cy="45" r={radius}
          className={styles.ringFill}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
        <text x="45" y="50" textAnchor="middle" className={styles.centerLabel}>
          {Math.round(clamped)}%
        </text>
      </svg>

      <div className={styles.meta}>
        <span className={styles.metaTitle}>{title}</span>
        <span className={styles.metaFigures}>
          <strong>{actual}</strong> / {target}
        </span>
        {typeof onTrack === "boolean" && (
          <span className={`${styles.status} ${onTrack ? styles.statusOnTrack : styles.statusBehind}`}>
            {onTrack ? "On track" : "Behind"}
          </span>
        )}
      </div>
    </div>
  );
}