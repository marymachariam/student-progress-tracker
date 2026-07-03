const API_URL = "http://localhost:8000";

async function request(endpoint, options = {}) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  register: (data) => request("/register_student", { method: "POST", body: JSON.stringify(data) }),
  login: (data) => request("/login", { method: "POST", body: JSON.stringify(data) }),

  getSubjects: () => request("/subjects"),
  createSubject: (data) => request("/subjects", { method: "POST", body: JSON.stringify(data) }),

  getTopics: () => request("/topics"),
  createTopic: (data) => request("/topics", { method: "POST", body: JSON.stringify(data) }),

  getStudySessions: () => request("/study_sessions"),
  createStudySession: (data) => request("/study_sessions", { method: "POST", body: JSON.stringify(data) }),

  getQuizScores: () => request("/quiz_scores"),
  createQuizScore: (data) => request("/quiz_scores", { method: "POST", body: JSON.stringify(data) }),

  getGoals: () => request("/goals"),
  createGoal: (data) => request("/goals", { method: "POST", body: JSON.stringify(data) }),

  getDashboard: () => request("/dashboard"),
  getSubjectBreakdown: () => request("/dashboard/subject-breakdown"),
  getProgressOverTime: () => request("/dashboard/progress-over-time"),
  getQuizTrend: () => request("/dashboard/quiz-trend"),
  getGoalProgress: () => request("/dashboard/goal-progress"),
  getStudyStreak: () => request("/dashboard/study-streak"),
  getAlerts: () => request("/dashboard/alerts"),
};