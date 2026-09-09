export default function GoalProgressBar({ goal }) {
  const percent = Math.min(goal.percent_complete, 100);

  return (
    <div className="goal-card">
      <div className="goal-header">
        <span>{goal.title}</span>
        <span>{goal.percent_complete}%</span>
      </div>
      <div className="goal-bar-bg">
        <div className="goal-bar-fill" style={{ width: `${percent}%` }} />
      </div>
      <p className="goal-sub">
        {goal.actual_progress} / {goal.target_value} hrs — ends {goal.end_date}
      </p>
    </div>
  );
}