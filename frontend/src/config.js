// API Configuration
// Automatically detects environment and uses correct backend URL

const getApiUrl = () => {
  // 1. If VITE_API_URL is set (production deployment), use it
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // 2. If running in development (localhost), use proxy
  if (import.meta.env.DEV) {
    return '/api';
  }
  
  // 3. If deployed but VITE_API_URL not set, try to detect backend
  // This is a fallback - you should always set VITE_API_URL in production!
  const hostname = window.location.hostname;
  
  // If frontend is on Vercel/Netlify, guess the backend URL
  if (hostname.includes('vercel.app') || hostname.includes('netlify.app')) {
    console.warn('⚠️ VITE_API_URL not set! Using fallback. Please set it in deployment settings.');
    // You need to replace this with your actual backend URL
    return 'https://YOUR-BACKEND-URL.onrender.com';
  }
  
  // Default fallback
  return '/api';
};

export const API_URL = getApiUrl();

// Log the API URL in development for debugging
if (import.meta.env.DEV) {
  console.log('🔗 API URL:', API_URL);
}
