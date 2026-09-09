import { getToken, logout } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function request(endpoint, options = {}) {
  const token = getToken();
  const isFormData = options.body instanceof FormData;

  const headers = {
    ...(isFormData ? {} : { "Content-Type": "application/json" }),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  let res;
  try {
    res = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
  } catch {
    throw new Error("Can't reach the server. Check your connection and try again.");
  }

  if (res.status === 401) {
    logout();
    if (typeof window !== "undefined") window.location.href = "/login";
    throw new Error("Your session has expired. Please log in again.");
  }

  if (res.status === 429) {
    throw new Error("Too many attempts. Please wait a minute before trying again.");
  }

  if (res.status === 500) {
    throw new Error("Something went wrong on our end. Please try again shortly.");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "Something went wrong. Please try again.");
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  register: (data) =>
    request("/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data) =>
    request("/auth/login", { method: "POST", body: JSON.stringify(data) }),
  verifyOtp: (data) =>
    request("/auth/verify-otp", { method: "POST", body: JSON.stringify(data) }),
  resendOtp: (data) =>
    request("/auth/resend-otp", { method: "POST", body: JSON.stringify(data) }),
  forgotPassword: (data) =>
    request("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  resetPassword: (data) =>
    request("/auth/reset-password", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getMe: () => request("/students/me"),
  uploadProfilePicture: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return request("/students/me/picture", { method: "POST", body: formData });
  },

  getSubjects: () => request("/subjects"),
  createSubject: (data) =>
    request("/subjects", { method: "POST", body: JSON.stringify(data) }),
  updateSubject: (id, data) =>
    request(`/subjects/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteSubject: (id) => request(`/subjects/${id}`, { method: "DELETE" }),

  getTopics: (subjectId) =>
    request(`/topics${subjectId ? `?subject_id=${subjectId}` : ""}`),
  createTopic: (data) =>
    request("/topics", { method: "POST", body: JSON.stringify(data) }),
  updateTopic: (id, data) =>
    request(`/topics/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteTopic: (id) => request(`/topics/${id}`, { method: "DELETE" }),

  getStudySessions: () => request("/study-sessions"),
  createStudySession: (data) =>
    request("/study-sessions", { method: "POST", body: JSON.stringify(data) }),

  getQuizScores: () => request("/quiz-scores"),
  createQuizScore: (data) =>
    request("/quiz-scores", { method: "POST", body: JSON.stringify(data) }),

  getGoals: () => request("/goals"),
  createGoal: (data) =>
    request("/goals", { method: "POST", body: JSON.stringify(data) }),
  updateGoal: (id, data) =>
    request(`/goals/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteGoal: (id) => request(`/goals/${id}`, { method: "DELETE" }),

  updateStudySession: (id, data) =>
    request(`/study-sessions/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteStudySession: (id) =>
    request(`/study-sessions/${id}`, { method: "DELETE" }),
  updateQuizScore: (id, data) =>
    request(`/quiz-scores/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteQuizScore: (id) => request(`/quiz-scores/${id}`, { method: "DELETE" }),
  getDashboard: () => request("/dashboard"),
  getSubjectBreakdown: () => request("/dashboard/subject-breakdown"),
  getProgressOverTime: () => request("/dashboard/progress-over-time"),
  getQuizTrend: () => request("/dashboard/quiz-trend"),
  getGoalProgress: () => request("/dashboard/goal-progress"),
  getStudyStreak: () => request("/dashboard/study-streak"),
  getAlerts: () => request("/dashboard/alerts"),
  getRecommendation: () => request("/recommendations"),
};
