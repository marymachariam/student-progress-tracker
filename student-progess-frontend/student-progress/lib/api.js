import { getStudent } from "./auth";

const API_URL = "http://localhost:8000";

async function request(endpoint, options = {}) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function studentId() {
  const student = getStudent();
  if (!student) throw new Error("No student logged in");
  return student.student_id;
}

export const api = {
  register: (data) => request("/register_student", { method: "POST", body: JSON.stringify(data) }),
  login: (data) => request("/login", { method: "POST", body: JSON.stringify(data) }),

  getSubjects: () => request(`/subjects?student_id=${studentId()}`),
  createSubject: (data) => request("/subjects", { method: "POST", body: JSON.stringify(data) }),

  getTopics: () => request(`/topics?student_id=${studentId()}`),
  createTopic: (data) => request("/topics", { method: "POST", body: JSON.stringify(data) }),

  getStudySessions: () => request(`/study_sessions?student_id=${studentId()}`),
  createStudySession: (data) => request("/study_sessions", { method: "POST", body: JSON.stringify(data) }),

  getQuizScores: () => request(`/quiz_scores?student_id=${studentId()}`),
  createQuizScore: (data) => request("/quiz_scores", { method: "POST", body: JSON.stringify(data) }),

  getGoals: () => request(`/goals?student_id=${studentId()}`),
  createGoal: (data) => request("/goals", { method: "POST", body: JSON.stringify(data) }),

  getDashboard: () => request(`/dashboard?student_id=${studentId()}`),
  getSubjectBreakdown: () => request(`/dashboard/subject-breakdown?student_id=${studentId()}`),
  getProgressOverTime: () => request(`/dashboard/progress-over-time?student_id=${studentId()}`),
  getQuizTrend: () => request(`/dashboard/quiz-trend?student_id=${studentId()}`),
  getGoalProgress: () => request(`/dashboard/goal-progress?student_id=${studentId()}`),
  getStudyStreak: () => request(`/dashboard/study-streak?student_id=${studentId()}`),
  getAlerts: () => request(`/dashboard/alerts?student_id=${studentId()}`),
};