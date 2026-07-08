"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { getStudent, clearStudent } from "../../lib/auth";
import styles from "./Navbar.module.css";

const LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/subjects", label: "Subjects" },
  { href: "/topics", label: "Topics" },
  { href: "/study-sessions", label: "Study sessions" },
  { href: "/quiz-scores", label: "Quiz scores" },
  { href: "/goals", label: "Goals" },
];

const HIDDEN_ON = ["/", "/login", "/register"];

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
    clearStudent();
    router.push("/");
  };

  return (
    <nav className={styles.sidebar}>
      <div className={styles.wordmark}>Field Log</div>
      <ul className={styles.navList}>
        {LINKS.map((link, i) => {
          const isActive = pathname?.startsWith(link.href);
          return (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`${styles.navLink} ${isActive ? styles.navLinkActive : ""}`}
              >
                <span className={styles.tabIndex}>{String(i + 1).padStart(2, "0")}</span>
                {link.label}
              </Link>
            </li>
          );
        })}
      </ul>

      <div className={styles.userSection}>
        <span className={styles.userName}>{student?.name || "Guest"}</span>
        <button className={styles.logoutButton} onClick={handleLogout}>Log out</button>
      </div>
    </nav>
  );
}