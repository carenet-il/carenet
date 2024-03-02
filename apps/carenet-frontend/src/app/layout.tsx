import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { GoogleAnalytics } from "@next/third-parties/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CareNet",
  description: "CareNet search",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="he">
      <GoogleAnalytics gaId="G-28BG9RD7VT" />
      <body className={inter.className} dir={"rtl"}>
        {children}
      </body>
    </html>
  );
}
