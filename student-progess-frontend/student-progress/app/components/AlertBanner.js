export default function AlertBanner({ alerts }) {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="alerts-container">
      {alerts.map((alert, i) => (
        <div key={i} className="alert-item">
          {alert.type === "goal_behind_schedule" &&
            ` "${alert.goal}" is behind schedule — expected ${alert.expected_by_now}h, you're at ${alert.actual}h.`}
          {alert.type === "subject_inactive" &&
            ` You haven't studied ${alert.subject} in ${alert.days_since_last_session} days.`}
          {alert.type === "no_sessions_logged" &&
            ` No sessions logged yet for ${alert.subject}.`}
        </div>
      ))}
    </div>
  );
}