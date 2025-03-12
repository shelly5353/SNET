'use client';

import React from 'react';
import Link from 'next/link';

export default function PDFEasyEdits() {
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const iframeRef = React.useRef<HTMLIFrameElement>(null);

  const handleIframeLoad = () => {
    setIsLoading(false);
    setError(null);
  };

  const handleIframeError = () => {
    setError('שגיאה בטעינת העורך. אנא נסה שוב מאוחר יותר.');
    setIsLoading(false);
  };

  const retryLoading = () => {
    setIsLoading(true);
    setError(null);
    if (iframeRef.current) {
      iframeRef.current.src = iframeRef.current.src;
    }
  };

  return (
    <div className="w-full min-h-screen bg-white p-4" dir="rtl">
      {/* כותרת וניווט */}
      <div className="max-w-4xl mx-auto mb-8">
        <div className="flex justify-between items-center mb-6">
          <Link 
            href="/" 
            className="text-blue-500 hover:text-blue-700 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            חזרה לדף הבית
          </Link>
          <a 
            href="https://pdf-easy-edits.vercel.app" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            פתח בחלון חדש
          </a>
        </div>
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">עריכת PDF פשוטה</h1>
          <p className="mb-4">העלה קובץ PDF להוספת מספור עמודים, כותרות ועוד</p>
        </div>
      </div>

      {/* עורך מוטמע */}
      <div className="relative max-w-6xl mx-auto h-[800px] border rounded-lg overflow-hidden shadow-lg bg-white">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90 z-10">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p className="mt-4 text-gray-600">טוען את עורך ה-PDF...</p>
            </div>
          </div>
        )}
        
        {error ? (
          <div className="absolute inset-0 flex items-center justify-center bg-white">
            <div className="text-center text-red-600">
              <p>{error}</p>
              <button 
                onClick={retryLoading} 
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                נסה שוב
              </button>
            </div>
          </div>
        ) : (
          <iframe
            ref={iframeRef}
            src="https://pdf-easy-edits.vercel.app"
            className="w-full h-full border-0"
            title="PDF Editor"
            allow="fullscreen"
            loading="lazy"
            onLoad={handleIframeLoad}
            onError={handleIframeError}
            sandbox="allow-same-origin allow-scripts allow-forms allow-downloads allow-popups"
          />
        )}
      </div>
    </div>
  );
} 