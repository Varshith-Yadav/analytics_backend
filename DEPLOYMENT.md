# Deployment Guide - Render

This guide will help you deploy the Analytics Backend API to Render.

## Prerequisites

1. A GitHub account with your code repository
2. A Render account (sign up at [render.com](https://render.com))

## Step-by-Step Deployment

### Option 1: Deploy Using render.yml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect Repository to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yml` file

3. **Review and Deploy**
   - Render will show a preview of services to be created
   - Review the configuration
   - Click "Apply" to create the services
   - Render will automatically:
     - Create a PostgreSQL database
     - Create a web service
     - Link the database to the web service via `DATABASE_URL`

4. **Wait for Deployment**
   - Render will build and deploy your application
   - You can monitor the build logs in real-time
   - Once deployed, you'll get a URL like: `https://analytics-backend.onrender.com`

### Option 2: Manual Deployment

#### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `analytics-db`
   - **Database**: `analytics`
   - **User**: `analytics_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (for testing) or Starter/Standard (for production)
4. Click "Create Database"
5. **Copy the Internal Database URL** (you'll need this later)

#### Step 2: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

   **Basic Settings:**
   - **Name**: `analytics-backend`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `.` if needed)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

   **Environment Variables:**
   - Click "Add Environment Variable"
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from Step 1
   - Click "Add"

   **Advanced Settings (Optional):**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes` (deploys on every push)

5. Click "Create Web Service"

#### Step 3: Initialize Database

After deployment, you need to initialize the database tables:

1. Go to your web service in Render Dashboard
2. Click on "Shell" tab
3. Run:
   ```bash
   python -c "from app.core.database import init_db; init_db()"
   ```

   Or if you want to seed sample data:
   ```bash
   python -m app.scripts.seed_data
   ```

## Post-Deployment

### Verify Deployment

1. **Health Check**: Visit `https://your-app.onrender.com/health`
   - Should return: `{"status": "healthy", "service": "analytics-backend"}`

2. **API Documentation**: Visit `https://your-app.onrender.com/docs`
   - Swagger UI should be available

3. **Root Endpoint**: Visit `https://your-app.onrender.com/`
   - Should show API information

### Environment Variables

The following environment variables are available:

- `DATABASE_URL`: Automatically set by Render (PostgreSQL connection string)
- `PORT`: Automatically set by Render (don't override)

### Database Management

**Accessing Database via Shell:**
```bash
# In Render Shell
psql $DATABASE_URL
```

**Backing up Database:**
```bash
pg_dump $DATABASE_URL > backup.sql
```

**Restoring Database:**
```bash
psql $DATABASE_URL < backup.sql
```

## Troubleshooting

### Common Issues

1. **Build Fails - Missing Dependencies**
   - Ensure `requirements.txt` includes all dependencies
   - Check build logs for specific errors

2. **Application Crashes on Start**
   - Check logs in Render Dashboard
   - Verify `DATABASE_URL` is set correctly
   - Ensure database is created and accessible

3. **Database Connection Errors**
   - Verify `DATABASE_URL` environment variable
   - Check if database is in the same region
   - Ensure database is not paused (free tier pauses after inactivity)

4. **Port Issues**
   - Always use `$PORT` environment variable in start command
   - Render assigns ports dynamically

5. **Import Errors**
   - Verify all Python files are in the repository
   - Check that `__init__.py` files exist in all packages

### Viewing Logs

1. Go to your service in Render Dashboard
2. Click on "Logs" tab
3. View real-time logs or download log files

### Restarting Service

1. Go to your service in Render Dashboard
2. Click "Manual Deploy" → "Clear build cache & deploy"

## Production Considerations

### Performance

- **Upgrade Plan**: Free tier has limitations. Consider Starter or Standard for production
- **Database**: Use managed PostgreSQL (not SQLite) for production
- **Caching**: Consider adding Redis for caching (optional)

### Security

- **Environment Variables**: Never commit sensitive data
- **HTTPS**: Render provides HTTPS automatically
- **Database**: Use internal database URLs (not public URLs)

### Monitoring

- **Health Checks**: Configure health check path (`/health`)
- **Alerts**: Set up alerts in Render Dashboard
- **Logs**: Monitor logs regularly

### Scaling

- **Horizontal Scaling**: Available on paid plans
- **Database**: Upgrade database plan for better performance
- **Auto-scaling**: Configure in Render settings

## Cost Estimation

- **Free Tier**: 
  - Web service: Free (spins down after inactivity)
  - Database: Free (limited, pauses after inactivity)
- **Starter Plan**: ~$7/month per service
- **Standard Plan**: ~$25/month per service

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-python)
- [Render PostgreSQL Guide](https://render.com/docs/databases)

## Support

If you encounter issues:
1. Check Render status page
2. Review application logs
3. Check Render community forums
4. Contact Render support

