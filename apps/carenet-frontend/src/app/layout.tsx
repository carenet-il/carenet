import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { GoogleAnalytics } from "@next/third-parties/google";
import { GoogleTagManager } from '@next/third-parties/google'

import "./globals.css";
import Head from "next/head";

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
      <Head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/favicon_io/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon_io/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon_io/favicon-16x16.png"
        />
        <link rel="icon" href="/favicon_io/favicon.ico" />
        <link rel="manifest" href="/favicon_io/site.webmanifest" />
      </Head>
      <GoogleAnalytics gaId="G-28BG9RD7VT" />
      <body className={inter.className} dir={"rtl"}>
        {children}
      </body>
      <GoogleTagManager gtmId="GTM-TLBS7L6X" />
    </html>
  );
}
