import { getToken, logout } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function request(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

  if (res.status === 401) {
    logout();
    if (typeof window !== "undefined") window.location.href = "/login";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `API error: ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  register: (data) => request("/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data) => request("/auth/login", { method: "POST", body: JSON.stringify(data) }),
  verifyOtp: (data) => request("/auth/verify-otp", { method: "POST", body: JSON.stringify(data) }),
  resendOtp: (data) => request("/auth/resend-otp", { method: "POST", body: JSON.stringify(data) }),
  forgotPassword: (data) => request("/auth/forgot-password", { method: "POST", body: JSON.stringify(data) }),
  resetPassword: (data) => request("/auth/reset-password", { method: "POST", body: JSON.stringify(data) }),

  getMe: () => request("/students/me"),

  getSubjects: () => request("/subjects"),
  createSubject: (data) => request("/subjects", { method: "POST", body: JSON.stringify(data) }),

  getTopics: (subjectId) => request(`/topics${subjectId ? `?subject_id=${subjectId}` : ""}`),
  createTopic: (data) => request("/topics", { method: "POST", body: JSON.stringify(data) }),

  getStudySessions: () => request("/study-sessions"),
  createStudySession: (data) => request("/study-sessions", { method: "POST", body: JSON.stringify(data) }),

  getQuizScores: () => request("/quiz-scores"),
  createQuizScore: (data) => request("/quiz-scores", { method: "POST", body: JSON.stringify(data) }),

  getGoals: () => request("/goals"),
  createGoal: (data) => request("/goals", { method: "POST", body: JSON.stringify(data) }),

  getDashboard: () => request("/dashboard"),
  getSubjectBreakdown: () => request("/dashboard/subject-breakdown"),
  getProgressOverTime: () => request("/dashboard/progress-over-time"),
  getQuizTrend: () => request("/dashboard/quiz-trend"),
  getGoalProgress: () => request("/dashboard/goal-progress"),
  getStudyStreak: () => request("/dashboard/study-streak"),
  getAlerts: () => request("/dashboard/alerts"),
  getRecommendation: () => request("/recommendations"),
};