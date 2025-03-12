import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SNET - כלים דיגיטליים מתקדמים',
  description: 'פלטפורמה לכלים דיגיטליים מתקדמים, כולל עריכת PDF פשוטה',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="he" dir="rtl">
      <body className={inter.className}>{children}</body>
    </html>
  );
} 