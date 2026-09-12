# Deploying CareerPilot AI Frontend to Vercel

This guide walks you through deploying the **Next.js 14** frontend of CareerPilot AI to [Vercel](https://vercel.com) for production.

---

## Option 1: Deploy via Vercel Dashboard (Recommended & Easiest)

### Step 1: Push Changes to GitHub
Ensure all latest changes are pushed to your GitHub repository:
```bash
git push origin main
```

### Step 2: Import Project in Vercel
1. Go to [vercel.com](https://vercel.com) and log in.
2. Click **"Add New..."** -> **"Project"**.
3. Select your repository: `lalithsagar18/careerpilot-ai`.
4. Click **"Import"**.

### Step 3: Configure Project Settings
In the **Configure Project** screen:

1. **Framework Preset**: Select `Next.js` (automatically detected).
2. **Root Directory**: 
   * Click **Edit** next to Root Directory.
   * Select the `frontend` folder.
   * Click **Continue**.
3. **Build and Output Settings**:
   * Build Command: `next build` (default)
   * Output Directory: `.next` (default)
   * Install Command: `npm install` (default)
4. **Environment Variables**:
   * Add the following environment variable:
     * **Key**: `NEXT_PUBLIC_API_URL`
     * **Value**: Your backend API URL (e.g. `https://your-backend-api.onrender.com/api/v1` or Railway / Fly.io / AWS endpoint)
     * *(For testing without a deployed backend, you can leave it empty or point to your deployed FastAPI instance).*

### Step 4: Click Deploy
Click **"Deploy"**. Vercel will build the Next.js frontend and provide you with a live production URL (e.g. `https://careerpilot-ai.vercel.app`).

---

## Option 2: Deploy via Vercel CLI

If you prefer using the terminal:

1. **Install Vercel CLI globally**:
   ```bash
   npm install -g vercel
   ```

2. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

3. **Deploy to Preview**:
   ```bash
   vercel
   ```
   Follow the interactive prompts:
   - *Set up and deploy?* **Y**
   - *Which scope?* (Select your account)
   - *Link to existing project?* **N**
   - *What's your project's name?* **careerpilot-ai**
   - *In which directory is your code located?* **./**

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## Setting Up Backend & CORS

When your Next.js app is deployed to `https://your-app.vercel.app`, ensure your FastAPI backend allows requests from that origin:

In your backend `.env` (or hosting environment variables on Render/Railway/Heroku):
```env
BACKEND_CORS_ORIGINS=["https://your-app.vercel.app", "http://localhost:3000"]
```
