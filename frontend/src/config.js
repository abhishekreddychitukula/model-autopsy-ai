// API Configuration
// Automatically detects environment and uses correct backend URL

const getApiUrl = () => {
  // 1. Check for VITE_API_BASE_URL or VITE_API_URL (supports both naming conventions)
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // 2. If running in development (localhost), use proxy
  if (import.meta.env.DEV) {
    return '/api';
  }
  
  // 3. If deployed but no env var set, try to detect backend
  // This is a fallback - you should always set VITE_API_BASE_URL in production!
  const hostname = window.location.hostname;
  
  // If frontend is on Vercel/Netlify, guess the backend URL
  if (hostname.includes('vercel.app') || hostname.includes('netlify.app')) {
    console.warn('⚠️ VITE_API_BASE_URL not set! Using fallback. Please set it in deployment settings.');
    // You need to replace this with your actual backend URL
    return 'https://YOUR-BACKEND-URL.onrender.com';
  }
  
  // Default fallback
  return '/api';
};

export const API_URL = getApiUrl();

// Log the API URL for debugging
console.log('🔗 API Base URL:', API_URL);
