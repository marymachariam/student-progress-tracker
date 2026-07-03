"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Navbar.module.css";

const LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/subjects", label: "Subjects" },
  { href: "/topics", label: "Topics" },
  { href: "/study-sessions", label: "Study sessions" },
  { href: "/quiz-scores", label: "Quiz scores" },
  { href: "/goals", label: "Goals" },
];

// pages where the sidebar should NOT show
const HIDDEN_ON = ["/", "/login", "/register"];

export default function Navbar() {
  const pathname = usePathname();

  if (HIDDEN_ON.includes(pathname)) {
    return null;
  }

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
    </nav>
  );
}