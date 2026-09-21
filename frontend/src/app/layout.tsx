import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'APEX-LEGAL-FORENSICS-SUITE — APEX Mega-Dashboard',
  description: 'Autonomous Legal Discovery & Timeline Forensics Suite',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#090d16] text-gray-100 antialiased">
        {children}
      </body>
    </html>
  );
}
