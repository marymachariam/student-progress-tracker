"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./page.module.css";
import { api } from "../../lib/api";
import Image from "next/image";
import {
  getStudent,
  isLoggedIn,
  logout,
  updateStoredStudent,
} from "../../lib/auth";

export default function ProfilePage() {
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [form, setForm] = useState({ name: "", email: "" });
  const [statusMessage, setStatusMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [confirmingDeactivate, setConfirmingDeactivate] = useState(false);
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    if (!isLoggedIn()) {
      router.push("/login");
      return;
    }
    loadProfile();
    const savedTheme = localStorage.getItem("theme") || "light";
    setTheme(savedTheme);
    document.documentElement.setAttribute("data-theme", savedTheme);
  }, [router]);

  const loadProfile = () => {
    api
      .getMe()
      .then((data) => {
        setStudent(data);
        setForm({ name: data.name, email: data.email });
      })
      .catch((err) => setStatusMessage(err.message));
  };

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSave = async (e) => {
    e.preventDefault();
    setStatusMessage("");
    try {
      const updated = await api.updateMe(form);
      setStudent(updated);
      updateStoredStudent({ name: updated.name, email: updated.email });
      setStatusMessage("Profile updated");
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handlePictureChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    setStatusMessage("");
    try {
      const updated = await api.uploadProfilePicture(file);
      setStudent(updated);
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [passwordMessage, setPasswordMessage] = useState("");

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordMessage("");
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setPasswordMessage("New password and confirmation don't match");
      return;
    }
    try {
      await api.changePassword(passwordForm);
      setPasswordMessage(
        "Password updated successfully.",
      );
      setPasswordForm({
        current_password: "",
        new_password: "",
        confirm_password: "",
      });
    } catch (err) {
      setPasswordMessage(`Error: ${err.message}`);
    }
  };
  const handleDeactivate = async () => {
    try {
      await api.deactivateAccount();
      logout();
      router.push("/login");
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleDelete = async () => {
    try {
      await api.deleteAccount();
      logout();
      router.push("/login");
    } catch (err) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  if (!student) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <div className={styles.header}>
        <span className={styles.eyebrow}>Account</span>
        <h1>Profile</h1>
      </div>

      <div className={styles.pictureSection}>
        <img
          src={student.profile_picture_url || "/default-avatar.png"}
          alt="Profile"
          className={styles.avatar}
        />
        <label className={styles.uploadLabel}>
          {uploading ? "Uploading..." : "Change photo"}
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handlePictureChange}
            hidden
          />
        </label>
      </div>

      <form onSubmit={handleSave} className={styles.formSection}>
        <label>
          Name
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Email
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </label>
        <button type="submit" className={styles.saveButton}>
          Save changes
        </button>
      </form>

      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}

      <div className={styles.section}>
        <h3>Password</h3>
        <form onSubmit={handlePasswordSubmit} className={styles.passwordForm}>
          <input
            type="password"
            placeholder="Current password"
            value={passwordForm.current_password}
            onChange={(e) =>
              setPasswordForm({
                ...passwordForm,
                current_password: e.target.value,
              })
            }
            required
          />
          <input
            type="password"
            placeholder="New password"
            value={passwordForm.new_password}
            onChange={(e) =>
              setPasswordForm({ ...passwordForm, new_password: e.target.value })
            }
            required
          />
          <input
            type="password"
            placeholder="Confirm new password"
            value={passwordForm.confirm_password}
            onChange={(e) =>
              setPasswordForm({
                ...passwordForm,
                confirm_password: e.target.value,
              })
            }
            required
          />
          <button type="submit" className={styles.actionButton}>
            Update password
          </button>
        </form>
        {passwordMessage && (
          <p className={styles.statusMessage}>{passwordMessage}</p>
        )}
      </div>

      <div className={styles.section}>
        <h3>Theme</h3>
        <div className={styles.themeToggle}>
          <button
            className={
              theme === "light" ? styles.themeActive : styles.themeButton
            }
            onClick={() => handleThemeChange("light")}
          >
            Light
          </button>
          <button
            className={
              theme === "dark" ? styles.themeActive : styles.themeButton
            }
            onClick={() => handleThemeChange("dark")}
          >
            Dark
          </button>
        </div>
      </div>

      <div className={styles.dangerZone}>
        <h3>Danger zone</h3>

        {confirmingDeactivate ? (
          <div className={styles.confirmRow}>
            <span>
              Deactivate your account? You can contact support to reactivate.
            </span>
            <button className={styles.actionButton} onClick={handleDeactivate}>
              Confirm deactivate
            </button>
            <button
              className={styles.actionButton}
              onClick={() => setConfirmingDeactivate(false)}
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            className={styles.actionButton}
            onClick={() => setConfirmingDeactivate(true)}
          >
            Deactivate account
          </button>
        )}

        {confirmingDelete ? (
          <div className={styles.confirmRow}>
            <span>Delete your account permanently? This can't be undone.</span>
            <button
              className={`${styles.actionButton} ${styles.deleteButton}`}
              onClick={handleDelete}
            >
              Confirm delete
            </button>
            <button
              className={styles.actionButton}
              onClick={() => setConfirmingDelete(false)}
            >
              Cancel
            </button>
          </div>
        ) : (
          <button
            className={`${styles.actionButton} ${styles.deleteButton}`}
            onClick={() => setConfirmingDelete(true)}
          >
            Delete account
          </button>
        )}
      </div>
    </div>
  );
}
