import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "NusaQC - Fish Quality Control AI",
  description:
    "AI-Powered visual quality control system for fish processing units.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="id"
      className={`${inter.variable} h-full antialiased`}
    >
      <body className="min-h-screen flex bg-slate-100 overflow-x-hidden antialiased font-sans">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0 min-h-screen bg-slate-100">
          <Topbar />
          <main className="flex-1 flex flex-col overflow-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
