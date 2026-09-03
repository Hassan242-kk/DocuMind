import type { Metadata } from "next";
import "./globals.css";


export const metadata: Metadata = {
  title: "DocuMind",
  description:
    "Intelligent Document Processing and AI Assistant",
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  return (
    <html lang="en">

      <body>
        {children}
      </body>

    </html>
  );
}