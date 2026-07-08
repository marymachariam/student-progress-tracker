const STORAGE_KEY = "field_log_student";

export function saveStudent(student) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(student));
}

export function getStudent() {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearStudent() {
  localStorage.removeItem(STORAGE_KEY);
}