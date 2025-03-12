'use client';

import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="w-full min-h-screen bg-white p-4" dir="rtl">
      <div className="max-w-4xl mx-auto mb-8 text-center">
        <h1 className="text-3xl font-bold mb-4">ברוכים הבאים ל-SNET</h1>
        <p className="mb-6">הפלטפורמה המובילה לכלים דיגיטליים מתקדמים</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-3">עריכת PDF פשוטה</h2>
            <p className="text-gray-600 mb-4">הוסף מספור עמודים, כותרות וערוך קבצי PDF בקלות</p>
            <div className="flex flex-col space-y-3">
              <Link 
                href="/pdf-easy-edits" 
                className="inline-block bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
              >
                השתמש באפליקציה באתר
              </Link>
              <a 
                href="https://pdf-easy-edits.vercel.app" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-block bg-gray-100 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                פתח את האפליקציה בחלון חדש
              </a>
            </div>
          </div>
          
          {/* ניתן להוסיף כאן כרטיסיות נוספות לשירותים אחרים */}
        </div>
      </div>
    </main>
  );
} 