# Quick Fix for "Analysis Failed" Error

## The Problem
You're seeing "Analysis failed. Please check your files and ensure they have the same columns."

## Possible Causes & Solutions

### 1. **Column Mismatch (Most Common)**
Your CSV files don't have the exact same columns.

**How to check:**
```bash
# Open each CSV and check the header row
# All three files MUST have identical columns (names only, order doesn't matter now)
```

**The fix:**
- Ensure all three CSVs have the **exact same column names**
- Column names are case-insensitive (Age = age)
- Whitespace is trimmed automatically
- **Order doesn't matter** (we auto-reorder now)

### 2. **Backend Not Running / Cold Start**
On free tier, Render spins down after 15 minutes of inactivity.

**The fix:**
- Wait 30-60 seconds for backend to "wake up"
- Try the request again
- Check backend logs in Render dashboard

### 3. **CORS Issues**
Browser blocking requests between frontend and backend.

**The fix:**
- Already fixed in the code (CORS = "*")
- Make sure you deployed latest version
- Check browser console for CORS errors

### 4. **Missing GROQ_API_KEY**
Backend needs this environment variable.

**The fix:**
1. Go to Render dashboard
2. Select your backend service
3. Environment tab
4. Add: `GROQ_API_KEY = your_actual_key`
5. Redeploy

### 5. **Wrong API URL in Frontend**
Frontend trying to connect to localhost instead of deployed backend.

**The fix:**
1. In Render/Vercel dashboard, set environment variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com`
2. Redeploy frontend

## Testing Locally First

Before deploying, test locally:

```bash
# Terminal 1 - Backend
cd model-autopsy-ai
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit http://localhost:3000 and test with sample files.

## Debug Steps

1. **Check backend is running:**
   ```bash
   curl https://your-backend.onrender.com/health
   ```
   Should return `{"status": "healthy", ...}`

2. **Check frontend environment:**
   - Open browser DevTools → Console
   - Look for API URL being used
   - Should show your deployed backend URL

3. **Check backend logs:**
   - Render Dashboard → Your Service → Logs
   - Look for actual error messages

4. **Test with sample files:**
   - Use the files in `samples/` folder
   - These are guaranteed to work

## Still Not Working?

Share the following:
1. Backend logs from Render
2. Browser console errors (F12 → Console)
3. Screenshot of the error
4. Did you set `VITE_API_URL` in frontend?
5. Did you set `GROQ_API_KEY` in backend?
