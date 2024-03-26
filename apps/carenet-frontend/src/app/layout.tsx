import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { GoogleAnalytics } from "@next/third-parties/google";
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
          rel="/favicon_io/apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="/favicon_io/icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="/favicon_io/icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="/favicon_io/manifest" href="/site.webmanifest" />
      </Head>
      <GoogleAnalytics gaId="G-28BG9RD7VT" />
      <body className={inter.className} dir={"rtl"}>
        {children}
      </body>
    </html>
  );
}
