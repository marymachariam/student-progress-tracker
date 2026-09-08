const TOKEN_KEY = "access_token";
const STUDENT_KEY = "student";

export function saveSession(loginResponse) {
  const { access_token, ...student } = loginResponse;
  localStorage.setItem(TOKEN_KEY, access_token);
  localStorage.setItem(STUDENT_KEY, JSON.stringify(student));
}

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function getStudent() {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(STUDENT_KEY);
  return raw ? JSON.parse(raw) : null;
}

export function isLoggedIn() {
  return !!getToken();
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(STUDENT_KEY);
}