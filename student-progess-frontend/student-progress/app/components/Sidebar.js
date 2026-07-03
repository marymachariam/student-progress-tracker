"use client";

import Link from "next/link";
import {
  FaChartLine,
  FaBook,
  FaList,
  FaClock,
  FaClipboardCheck,
  FaBullseye
} from "react-icons/fa";

export default function Sidebar() {
  return (
    <div className="bg-dark text-white vh-100 p-3" style={{ width: "250px" }}>
      <h3 className="mb-4">Student Tracker</h3>

      <ul className="nav flex-column">

        <li className="nav-item mb-3">
          <Link href="/dashboard" className="nav-link text-white">
            <FaChartLine className="me-2" />
            Dashboard
          </Link>
        </li>

        <li className="nav-item mb-3">
          <Link href="/subjects" className="nav-link text-white">
            <FaBook className="me-2" />
            Subjects
          </Link>
        </li>

        <li className="nav-item mb-3">
          <Link href="/topics" className="nav-link text-white">
            <FaList className="me-2" />
            Topics
          </Link>
        </li>

        <li className="nav-item mb-3">
          <Link href="/study-sessions" className="nav-link text-white">
            <FaClock className="me-2" />
            Study Sessions
          </Link>
        </li>

        <li className="nav-item mb-3">
          <Link href="/quiz-scores" className="nav-link text-white">
            <FaClipboardCheck className="me-2" />
            Quiz Scores
          </Link>
        </li>

        <li className="nav-item">
          <Link href="/goals" className="nav-link text-white">
            <FaBullseye className="me-2" />
            Goals
          </Link>
        </li>

      </ul>
    </div>
  );
}