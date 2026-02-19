import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image Processor",
  description: "Web-based image processing tool",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0a0a0a] text-gray-100 antialiased">{children}</body>
    </html>
  );
}
