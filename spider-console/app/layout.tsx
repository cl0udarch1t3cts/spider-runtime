import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Spider Console",
  description: "Live view of spider tasks, runs, records, and budget",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
