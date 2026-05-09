# 🎯 AMD HACKATHON SUBMISSION CHECKLIST

## ⏰ DEADLINE: 5 DAYS LEFT

---

## 📋 PRE-DEPLOYMENT

- [x] ✅ Build complete mental health simulator
- [x] ✅ Event injection system working
- [x] ✅ Conversation bubbles implemented
- [x] ✅ Black Mirror clinical UI
- [x] ✅ Oracle AI with AMD integration
- [x] ✅ Git repository initialized
- [x] ✅ All files committed
- [ ] ⏳ AMD API credentials added to `.env`

---

## 🚀 DEPLOYMENT (DO NOW)

### Step 1: GitHub
- [ ] Create GitHub repo: https://github.com/new
  - Name: `synesthesia-ai`
  - Visibility: **PUBLIC** (required)
  - Don't initialize with README
- [ ] Add remote: `git remote add origin https://github.com/YOUR_USERNAME/synesthesia-ai.git`
- [ ] Push code: `git push -u origin main`

### Step 2: Railway
- [ ] Sign up: https://railway.app
- [ ] Create new project
- [ ] Deploy from GitHub repo
- [ ] Add environment variables:
  - `LLM_API_KEY` (NVIDIA)
  - `LLM_BASE_URL` (NVIDIA)
  - `AMD_API_KEY` (your AMD key)
  - `AMD_BASE_URL` (your AMD endpoint)
  - `PORT=5001`
- [ ] Wait for deployment (5-10 min)
- [ ] Get Railway URL

### Step 3: Test Deployment
- [ ] Open Railway URL
- [ ] Create simulation (100 agents)
- [ ] Watch agents move
- [ ] Inject event
- [ ] Query Oracle AI
- [ ] Check browser console for "Powered by AMD"
- [ ] No errors

---

## 📝 HACKATHON SUBMISSION

### Required Field: "Open Source / Technical Walkthrough Link"

**Primary Link (Railway):**
```
https://synesthesia-production-xxxx.up.railway.app
```

**Secondary Link (GitHub):**
```
https://github.com/YOUR_USERNAME/synesthesia-ai
```

### What Judges Will See:
1. ✅ Live working demo
2. ✅ AI-generated societies
3. ✅ Real-time simulation
4. ✅ Event injection
5. ✅ Oracle AI (AMD-powered)
6. ✅ Conversation system
7. ✅ Black Mirror UI

---

## 🔴 AMD INTEGRATION PROOF

**Where AMD is Used:**
- Oracle AI (real-time population analytics)
- Most compute-intensive feature
- User-facing (judges will use it)
- 2-5 second response time

**How to Verify:**
1. Open browser console
2. Query Oracle: "Who is most stressed?"
3. Look for: `"provider": "AMD"`
4. Check for "Powered by AMD" badge in UI

---

## 📊 DEMO SCENARIOS (For Judges)

### Scenario 1: School Stress
```
Society: "High school during finals week"
Population: 100
Event: "Finals cancelled - snow day"
Query: "Who was most stressed before the event?"
```

### Scenario 2: Workplace Burnout
```
Society: "Tech startup with tight deadlines"
Population: 150
Event: "New policy: 4-day work week"
Query: "How did mental health change?"
```

### Scenario 3: Hospital Crisis
```
Society: "Hospital emergency room"
Population: 100
Event: "Mass casualty event - multiple patients"
Query: "Which staff members are in crisis?"
```

---

## ⚠️ COMMON ISSUES

### Issue: "Application failed to respond"
**Fix:** Check Railway logs, verify env variables

### Issue: "Society generation timeout"
**Fix:** Normal on first load (cold start), try again

### Issue: "Oracle AI not using AMD"
**Fix:** Verify AMD_API_KEY and AMD_BASE_URL are correct

### Issue: "Module not found"
**Fix:** Railway should auto-install from requirements_deploy.txt

---

## 🎥 OPTIONAL: Video Walkthrough

If you have time (not required):
1. Record 2-3 minute demo
2. Show society generation
3. Show event injection
4. Show Oracle AI
5. Upload to YouTube
6. Add link to README

---

## 📈 SUBMISSION STRATEGY

### What Makes This Stand Out:
1. **Real-time simulation** (not turn-based)
2. **10,000 agents** (scalable, demo with 100-200)
3. **AI-generated societies** (any scenario)
4. **Event injection** (interactive)
5. **Oracle AI** (AMD-powered insights)
6. **Visual polish** (Black Mirror aesthetic)
7. **Complete system** (not just a prototype)

### AMD Integration Highlights:
- Oracle AI runs on AMD
- Real-time analytics
- User-facing feature
- Showcases AMD compute power

---

## ⏱️ TIME ESTIMATE

- GitHub setup: **2 minutes**
- Railway deployment: **5 minutes**
- Testing: **5 minutes**
- Submission: **2 minutes**

**Total: ~15 minutes**

---

## 🚨 DO THIS NOW

1. Run: `./deploy.sh`
2. Follow instructions
3. Deploy to Railway
4. Test deployment
5. Submit to hackathon

**You have 5 days. Deploy today!**

---

## 📞 HELP

If stuck:
- Check: `DEPLOYMENT_STEPS.md`
- Check: `DEPLOY.md`
- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## ✨ FINAL CHECKLIST

Before submitting:
- [ ] Railway URL works
- [ ] Can create simulation
- [ ] Agents move smoothly
- [ ] Event injection works
- [ ] Oracle AI responds
- [ ] AMD badge visible
- [ ] No console errors
- [ ] GitHub repo is public
- [ ] README has links
- [ ] Submitted to hackathon

---

**YOU GOT THIS! 🚀**

Built in 1 week. 5,000+ lines of code. Real-time mental health simulation at scale.

**Now deploy and win!** 🏆
