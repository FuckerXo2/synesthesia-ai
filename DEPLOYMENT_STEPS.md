# 🚀 DEPLOYMENT STEPS - DO THIS NOW

## ✅ Step 1: Git is Ready (DONE)
- ✅ Git initialized
- ✅ All files committed

## 📦 Step 2: Push to GitHub

### Create GitHub Repo:
1. Go to https://github.com/new
2. Repository name: `synesthesia-ai`
3. Description: "Mental Health Population Simulator - AMD Hackathon"
4. **Make it PUBLIC** (required for hackathon)
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### Push Your Code:
```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/synesthesia-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🚂 Step 3: Deploy to Railway

### Create Railway Account:
1. Go to https://railway.app
2. Sign up with GitHub (easiest)
3. Verify email

### Deploy:
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `synesthesia-ai` repo
4. Railway will auto-detect Python

### Add Environment Variables:
In Railway dashboard → Variables tab, add:

```
LLM_API_KEY=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
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-122b-a10b
AMD_API_KEY=your_amd_api_key_here
AMD_BASE_URL=your_amd_base_url_here
PORT=5001
```

**IMPORTANT:** Replace `AMD_API_KEY` and `AMD_BASE_URL` with your actual AMD credentials!

### Get Your URL:
- Railway will give you a URL like: `https://synesthesia-production-xxxx.up.railway.app`
- **THIS IS YOUR HACKATHON SUBMISSION LINK!**

## 📝 Step 4: Submit to Hackathon

**Submission Field:** "Open Source / Technical Walkthrough Link"

**What to submit:**
```
https://synesthesia-production-xxxx.up.railway.app
```

**Also include GitHub link:**
```
https://github.com/YOUR_USERNAME/synesthesia-ai
```

## 🎥 Step 5: Test Your Deployment

1. Open your Railway URL
2. Create a simulation: "High school during finals week"
3. Population: 100
4. Click "GENERATE & GO"
5. Watch agents move
6. Inject event: "Snow day - classes cancelled"
7. Query Oracle: "Who is most stressed?"

**If everything works, you're ready to submit!**

## ⚠️ Troubleshooting

### "Application failed to respond"
- Check Railway logs
- Verify all env variables are set
- Make sure PORT=5001 is set

### "Module not found"
- Railway should auto-install from `requirements_deploy.txt`
- Check build logs

### "Society generation timeout"
- This is normal on first load (cold start)
- Try again, it should work

### "Oracle AI not using AMD"
- Check AMD_API_KEY and AMD_BASE_URL are correct
- Look for "✅ AMD client initialized" in logs
- If not set, Oracle will use NVIDIA (still works)

## 📊 What Judges Will See

1. **Landing page** - Black Mirror clinical UI
2. **Society generation** - AI creates the world
3. **Live simulation** - Agents moving, mental health changing
4. **Event injection** - Real-time impact on population
5. **Oracle AI** - Powered by AMD, instant insights
6. **Conversations** - Speech bubbles between agents

## 🎯 Hackathon Submission Checklist

- [ ] GitHub repo is PUBLIC
- [ ] Railway deployment is live
- [ ] Can create simulation
- [ ] Agents appear and move
- [ ] Event injection works
- [ ] Oracle AI responds (check if AMD is used)
- [ ] No console errors
- [ ] Submitted Railway URL to hackathon

## 💡 Tips

1. **Test before submitting** - Make sure everything works
2. **Check AMD usage** - Open browser console, look for "Powered by AMD"
3. **Keep it simple** - Use 100-200 agents for demo (not 10,000)
4. **Have backup** - If Railway fails, try Render or Fly.io

---

**Time Estimate:**
- GitHub push: 2 minutes
- Railway setup: 5 minutes
- Testing: 5 minutes
- **Total: ~15 minutes**

**You have 5 days until deadline. Deploy NOW!** 🚀
