from sqlalchemy.orm import Session

from app.models.student import Student
from app.services.analytics import (
    get_dashboard_summary, get_quiz_trend, get_goal_progress, get_alerts,
)


def build_digest_text(db: Session, student: Student) -> str:
    summary = get_dashboard_summary(db, student.student_id)
    goals = get_goal_progress(db, student.student_id)
    alerts = get_alerts(db, student.student_id)

    lines = [
        f"This week you studied {summary['total_hours_studied']} hours total, "
        f"averaging {summary['average_quiz_score_percent']}% on quizzes.",
        f"Top subject: {summary['top_subject']}. "
        f"Active goals: {summary['active_goals']}, completed: {summary['completed_goals']}.",
    ]
    if goals:
        top_goal = goals[0]
        lines.append(f"Goal progress on \"{top_goal['title']}\": {top_goal['percent_complete']}% complete.")
    if alerts:
        first = alerts[0]
        if first["type"] == "goal_behind_schedule":
            lines.append(f"Heads up: \"{first['goal']}\" is falling behind schedule.")
        elif first["type"] == "subject_inactive":
            lines.append(f"You haven't touched {first['subject']} in {first['days_since_last_session']} days.")

    return " ".join(lines)


def build_digest_html(db: Session, student: Student) -> str:
    summary = get_dashboard_summary(db, student.student_id)
    goals = get_goal_progress(db, student.student_id)
    alerts = get_alerts(db, student.student_id)

    stat_cards = f"""
      <tr>
        <td style="padding:12px 8px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F7F3;border-radius:8px;border:1px solid #C9D2C4;">
            <tr>
              <td style="padding:16px;text-align:center;">
                <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#3F6B4F;font-family:Arial,sans-serif;">Hours Studied</div>
                <div style="font-size:24px;font-weight:700;color:#16241B;font-family:Georgia,serif;margin-top:4px;">{summary['total_hours_studied']}</div>
              </td>
              <td style="padding:16px;text-align:center;">
                <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#3F6B4F;font-family:Arial,sans-serif;">Avg Quiz Score</div>
                <div style="font-size:24px;font-weight:700;color:#16241B;font-family:Georgia,serif;margin-top:4px;">{summary['average_quiz_score_percent']}%</div>
              </td>
              <td style="padding:16px;text-align:center;">
                <div style="font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:#3F6B4F;font-family:Arial,sans-serif;">Top Subject</div>
                <div style="font-size:20px;font-weight:700;color:#16241B;font-family:Georgia,serif;margin-top:4px;">{summary['top_subject']}</div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    """

    goal_rows = ""
    for g in goals[:3]:
        pct = min(g["percent_complete"], 100)
        goal_rows += f"""
          <tr>
            <td style="padding:10px 8px;">
              <div style="font-size:14px;font-weight:600;color:#16241B;font-family:Arial,sans-serif;margin-bottom:6px;">
                {g['title']} — {g['percent_complete']}%
              </div>
              <table width="100%" cellpadding="0" cellspacing="0" style="background:#E4E9E1;border-radius:6px;overflow:hidden;">
                <tr>
                  <td width="{pct}%" style="background:#3F6B4F;height:8px;font-size:0;line-height:0;">&nbsp;</td>
                  <td style="height:8px;font-size:0;line-height:0;">&nbsp;</td>
                </tr>
              </table>
            </td>
          </tr>
        """

    alert_rows = ""
    for a in alerts[:3]:
        if a["type"] == "goal_behind_schedule":
            text = f"\"{a['goal']}\" is falling behind schedule."
        elif a["type"] == "subject_inactive":
            text = f"No sessions logged for {a['subject']} in {a['days_since_last_session']} days."
        else:
            text = f"No sessions logged yet for {a['subject']}."
        alert_rows += f"""
          <tr>
            <td style="padding:8px;border-left:3px solid #B5533C;background:#F2DAD3;border-radius:4px;font-size:13px;color:#16241B;font-family:Arial,sans-serif;">
              {text}
            </td>
          </tr>
          <tr><td style="height:8px;"></td></tr>
        """

    return f"""
    <html>
    <body style="margin:0;padding:0;background:#EEF1EC;font-family:Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#EEF1EC;padding:32px 0;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0" style="background:#FFFFFF;border-radius:12px;overflow:hidden;border:1px solid #C9D2C4;">
              <tr>
                <td style="background:#3F6B4F;padding:24px 32px;">
                  <div style="color:#FFFFFF;font-family:Georgia,serif;font-size:20px;font-weight:700;">Field Log</div>
                  <div style="color:#DDEDD9;font-size:12px;letter-spacing:0.06em;text-transform:uppercase;margin-top:2px;">Weekly Study Summary</div>
                </td>
              </tr>
              <tr>
                <td style="padding:24px 32px 8px 32px;">
                  <div style="font-size:15px;color:#16241B;font-family:Arial,sans-serif;">Hi {student.name},</div>
                  <div style="font-size:14px;color:#4B5A50;font-family:Arial,sans-serif;margin-top:4px;">Here's how your week went.</div>
                </td>
              </tr>
              <tr><td style="padding:0 24px;">
                <table width="100%" cellpadding="0" cellspacing="0">{stat_cards}</table>
              </td></tr>
              {"<tr><td style='padding:16px 32px 0 32px;font-size:14px;font-weight:700;color:#16241B;font-family:Arial,sans-serif;'>Goal Progress</td></tr>" if goals else ""}
              <tr><td style="padding:0 32px;">
                <table width="100%" cellpadding="0" cellspacing="0">{goal_rows}</table>
              </td></tr>
              {"<tr><td style='padding:16px 32px 0 32px;font-size:14px;font-weight:700;color:#16241B;font-family:Arial,sans-serif;'>Alerts</td></tr>" if alerts else ""}
              <tr><td style="padding:8px 32px 24px 32px;">
                <table width="100%" cellpadding="0" cellspacing="0">{alert_rows}</table>
              </td></tr>
              <tr>
                <td style="padding:20px 32px;background:#F5F7F3;border-top:1px solid #C9D2C4;">
                  <div style="font-size:13px;color:#4B5A50;font-family:Arial,sans-serif;">Keep up the momentum!</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


async def send_weekly_digests(db: Session) -> int:
    from app.core.mail import send_digest_email

    students = db.query(Student).filter(Student.is_verified == True).all()
    sent = 0
    for student in students:
        text = build_digest_text(db, student)
        html = build_digest_html(db, student)
        await send_digest_email(student.email, student.name, text, html)
        sent += 1
    return sent