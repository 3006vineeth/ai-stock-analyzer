import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Stock Analyzer - Indian Stock Market Analysis",
  description: "AI-powered stock analysis platform for Indian stock market",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}
