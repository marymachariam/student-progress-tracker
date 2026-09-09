"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { getStudent, logout, updateStoredStudent } from "../../lib/auth";
import { api } from "../../lib/api";
import styles from "./Navbar.module.css";

const LINKS = [
  { href: "/dashboard", label: "Dashboard", icon: "◈" },
  { href: "/subjects", label: "Subjects", icon: "◫" },
  { href: "/topics", label: "Topics", icon: "◎" },
  { href: "/study-sessions", label: "Study sessions", icon: "◷" },
  { href: "/quiz-scores", label: "Quiz scores", icon: "✓" },
  { href: "/goals", label: "Goals", icon: "◆" },
  { href: "/recommendations", label: "AI recommendations", icon: "✦" },
];

const HIDDEN_ON = ["/", "/login", "/register"];

function initials(name) {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).slice(0, 2).join("").toUpperCase();
}

function Avatar({ student, size = 44, onClick, uploading }) {
  return (
    <div
      className={styles.avatarWrap}
      style={{ width: size, height: size, cursor: onClick ? "pointer" : "default" }}
      onClick={onClick}
      title={onClick ? "Change profile picture" : undefined}
    >
      {student?.profile_picture_url ? (
        <Image
          src={student.profile_picture_url}
          alt={student.name || "Profile"}
          fill
          className={styles.avatarImg}
        />
      ) : (
        <div className={styles.avatar}>{initials(student?.name)}</div>
      )}
      {onClick && <div className={styles.avatarOverlay}>{uploading ? "…" : "✎"}</div>}
    </div>
  );
}

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [student, setStudent] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const fileInputRef = useRef(null);

  useEffect(() => {
    setStudent(getStudent());
  }, []);

  if (HIDDEN_ON.includes(pathname)) {
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadError("");
    setUploading(true);
    try {
      const updatedStudent = await api.uploadProfilePicture(file);
      const merged = updateStoredStudent({ profile_picture_url: updatedStudent.profile_picture_url });
      setStudent(merged);
    } catch (err) {
      setUploadError(err.message);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  return (
    <>
      <nav className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.wordmark}>Field Log</div>
          <div className={styles.tagline}>Study record</div>
        </div>

        <div className={styles.profileCard}>
          <Avatar student={student} size={48} onClick={handleAvatarClick} uploading={uploading} />
          <div className={styles.userMeta}>
            <span className={styles.userName}>{student?.name || "Guest"}</span>
            <span className={styles.userEmail}>{student?.email || ""}</span>
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleFileChange}
            className={styles.hiddenInput}
            style={{ display: "none" }}
          />
        </div>
        {uploadError && <p className={styles.uploadError}>{uploadError}</p>}

        <ul className={styles.navList}>
          {LINKS.map((link, i) => {
            const isActive = pathname?.startsWith(link.href);
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`${styles.navLink} ${isActive ? styles.navLinkActive : ""}`}
                >
                  <span className={styles.navIcon}>{link.icon}</span>
                  <span className={styles.navLabel}>{link.label}</span>
                  <span className={styles.tabIndex}>{String(i + 1).padStart(2, "0")}</span>
                </Link>
              </li>
            );
          })}
          <li>
            <button className={styles.logoutRow} onClick={handleLogout}>
              <span className={styles.navIcon}>⏻</span>
              <span className={styles.navLabel}>Log out</span>
            </button>
          </li>
        </ul>
      </nav>

      <div className={styles.mobileTopBar}>
        <div className={styles.mobileUserInfo}>
          <Avatar student={student} size={32} onClick={handleAvatarClick} uploading={uploading} />
          <span className={styles.userName}>{student?.name || "Guest"}</span>
        </div>
        <button className={styles.mobileLogoutButton} onClick={handleLogout} aria-label="Log out">
          ⏻
        </button>
      </div>

      <nav className={styles.mobileTabBar}>
        {LINKS.slice(0, 5).map((link) => {
          const isActive = pathname?.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`${styles.mobileTab} ${isActive ? styles.mobileTabActive : ""}`}
            >
              <span className={styles.mobileTabIcon}>{link.icon}</span>
              <span className={styles.mobileTabLabel}>{link.label.split(" ")[0]}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}