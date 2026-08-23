import type { Metadata } from "next";
import { Radio_Canada_Big } from "next/font/google";
import "./globals.css";

const brandFont = Radio_Canada_Big({
  subsets: ["latin"],
  weight: ["500", "700"],
  variable: "--font-brand",
});

export const metadata: Metadata = {
  title: "Spider Console · Cloud Architects",
  description:
    "Cloud Architects GmbH — live view of spider tasks, runs, records, and budget",
  icons: { icon: "/logo.svg" },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={brandFont.variable}>
      <body>{children}</body>
    </html>
  );
}
