import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Lead-Gen Pipeline Dashboard',
  description: 'Live status of the automated lead-generation pipeline'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
