"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { getStudent, logout } from "../../lib/auth";
import styles from "./Navbar.module.css";

const LINKS = [
  { href: "/dashboard", label: "Dashboard", icon: "◈" },
  { href: "/subjects", label: "Subjects", icon: "◫" },
  { href: "/topics", label: "Topics", icon: "◎" },
  { href: "/study-sessions", label: "Study sessions", icon: "◷" },
  { href: "/quiz-scores", label: "Quiz scores", icon: "✓" },
  { href: "/goals", label: "Goals", icon: "◆" },
];

const HIDDEN_ON = ["/", "/login", "/register"];

function initials(name) {
  if (!name) return "?";
  return name
    .split(" ")
    .map((part) => part[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [student, setStudent] = useState(null);

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

  return (
    <>
      <nav className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.wordmark}>Field Log</div>
          <div className={styles.tagline}>Study record</div>
        </div>

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
        </ul>

        <div className={styles.userSection}>
          <div className={styles.userInfo}>
            <div className={styles.avatar}>{initials(student?.name)}</div>
            <div className={styles.userMeta}>
              <span className={styles.userName}>{student?.name || "Guest"}</span>
              <span className={styles.userEmail}>{student?.email || ""}</span>
            </div>
          </div>
          <button className={styles.logoutButton} onClick={handleLogout} aria-label="Log out">
            <span className={styles.logoutIcon}>⏻</span>
            Log out
          </button>
        </div>
      </nav>

      <div className={styles.mobileTopBar}>
        <div className={styles.mobileUserInfo}>
          <div className={styles.avatar}>{initials(student?.name)}</div>
          <span className={styles.userName}>{student?.name || "Guest"}</span>
        </div>
        <button className={styles.mobileLogoutButton} onClick={handleLogout} aria-label="Log out">
          ⏻
        </button>
      </div>

      <nav className={styles.mobileTabBar}>
        {LINKS.map((link) => {
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