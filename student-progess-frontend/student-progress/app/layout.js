import "./globals.css";
import Navbar from "./components/Navbar";

export const metadata = {
  title: "Field Log — Student Progress",
  description: "Track study sessions, quiz scores, and goals.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <Navbar />
          <main className="main-content">{children}</main>
        </div>
      </body>
    </html>
  );
}