# 🚀 Deployment Guide

## Railway Deployment (Recommended)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Synesthesia"

# Create GitHub repo (on github.com)
# Then connect and push:
git remote add origin https://github.com/yourusername/synesthesia.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `synesthesia` repo
5. Railway will auto-detect Python and deploy

### Step 3: Add Environment Variables

In Railway dashboard:
1. Go to your project
2. Click "Variables"
3. Add these:

```
LLM_API_KEY=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
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-122b-a10b
AMD_API_KEY=your_amd_key_here
AMD_BASE_URL=your_amd_endpoint_here
```

### Step 4: Get Your URL

Railway will give you a URL like:
```
https://synesthesia-production-xxxx.up.railway.app
```

**This is the link you submit to the hackathon!**

---

## Render Deployment (Alternative)

### Step 1: Push to GitHub (same as above)

### Step 2: Create Render Service

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name:** synesthesia
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements_deploy.txt`
   - **Start Command:** `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT web_app:app`

### Step 3: Add Environment Variables

Same as Railway, add all env vars.

### Step 4: Deploy

Click "Create Web Service" and wait 5-10 minutes.

---

## Fly.io Deployment (Advanced)

### Step 1: Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Launch

```bash
fly auth login
fly launch
```

### Step 3: Add Secrets

```bash
fly secrets set LLM_API_KEY=your_key
fly secrets set LLM_BASE_URL=https://integrate.api.nvidia.com/v1
fly secrets set AMD_API_KEY=your_amd_key
fly secrets set AMD_BASE_URL=your_amd_endpoint
```

### Step 4: Deploy

```bash
fly deploy
```

---

## Troubleshooting

### "Application failed to respond"
- Check logs: `railway logs` or Render dashboard
- Verify PORT env variable is being used
- Check if all dependencies installed

### "Module not found"
- Make sure `requirements_deploy.txt` has all dependencies
- Redeploy after fixing

### "WebSocket connection failed"
- Railway/Render support WebSockets by default
- Check if `flask-socketio` is installed
- Verify `eventlet` worker is being used

### "API timeout"
- NVIDIA API can be slow
- Increase timeout in code
- Use fallback models

---

## Performance Tips

### For Railway/Render Free Tier:

1. **Limit population to 200 agents** (not 10,000)
   - Free tier has limited RAM
   - 200 agents runs smoothly

2. **Use environment variable:**
   ```
   MAX_POPULATION=200
   ```

3. **Cold starts:**
   - First load takes 30-60 seconds
   - Subsequent loads are fast

4. **Keep it alive:**
   - Free tier sleeps after 15 min inactivity
   - Use UptimeRobot to ping every 5 min

---

## What to Submit

**For Hackathon Submission:**

1. **Primary Link:** Railway/Render URL
   ```
   https://synesthesia-production.up.railway.app
   ```

2. **GitHub Link:** (secondary)
   ```
   https://github.com/yourusername/synesthesia
   ```

3. **In README:** Add both links at top

---

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Can create simulation
- [ ] Agents appear and move
- [ ] Event injection works
- [ ] Oracle AI responds
- [ ] No console errors
- [ ] Mobile responsive (bonus)

---

## Cost Estimate

### Railway Free Tier:
- $5 credit/month
- ~500 hours runtime
- **Cost: FREE** (for hackathon)

### Render Free Tier:
- 750 hours/month
- Sleeps after 15 min
- **Cost: FREE**

### Fly.io Free Tier:
- 3 shared VMs
- 160GB bandwidth
- **Cost: FREE**

**All options are free for hackathon!**

---

## Need Help?

Check logs:
```bash
# Railway
railway logs

# Render
# Check dashboard → Logs tab

# Fly.io
fly logs
```

Common issues:
1. Missing env vars → Add in dashboard
2. Wrong Python version → Specify in `runtime.txt`
3. Port binding → Use `$PORT` env variable

---

**You're ready to deploy!** 🚀
