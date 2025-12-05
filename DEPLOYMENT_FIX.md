# Fix for Render Deployment Error

## Problem
Render is trying to use Poetry instead of pip, causing the error:
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

## Solution

### Option 1: Manual Deployment (Recommended for now)

Instead of using Blueprint (render.yml), deploy manually:

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → New + → PostgreSQL
   - Name: `analytics-db`
   - Plan: Free
   - Create and copy the **Internal Database URL**

2. **Create Web Service:**
   - Go to Render Dashboard → New + → Web Service
   - Connect your GitHub repo
   - Settings:
     - **Name**: `analytics-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Environment Variable**: 
       - Key: `DATABASE_URL`
       - Value: (paste Internal Database URL from step 1)
   - Click "Create Web Service"

3. **Initialize Database:**
   - After deployment, go to Shell tab
   - Run: `python -c "from app.core.database import init_db; init_db()"`

### Option 2: Fix Blueprint Deployment

If you want to use Blueprint, you need to:

1. **Commit all changes:**
   ```bash
   git add requirements.txt render.yml
   git commit -m "Fix Render deployment configuration"
   git push origin main
   ```

2. **In Render Dashboard:**
   - Delete the existing Blueprint/service
   - Create new Blueprint
   - Make sure to select "Python" not "Poetry" when it asks

3. **Or manually override in service settings:**
   - After Blueprint creates services
   - Go to Web Service → Settings
   - Change "Build Command" to: `pip install --upgrade pip && pip install -r requirements.txt`
   - Save and redeploy

## Why This Happens

Render auto-detects build systems. If it sees certain files or patterns, it might try Poetry. The `render.yml` should override this, but sometimes manual configuration is needed.

## Verify Requirements.txt is Committed

Run this to verify:
```bash
git ls-files requirements.txt
```

If it shows `requirements.txt`, it's committed. If not:
```bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

