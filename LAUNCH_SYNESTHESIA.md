# 🚀 Launch Synesthesia

## One Command to Rule Them All

```bash
python3 synesthesia_launcher.py
```

That's it! 🎉

---

## What Happens

### 1. Setup Screen Opens
A GUI window appears where you:
- **Type what society you want** (e.g., "Tech startup city", "Medieval village", "Space station")
- **Set population size** (recommended: 50-200 for smooth performance)
- **Click GO** 🚀

### 2. Generation Phase (30-60 seconds)
The system:
- 🧠 Generates society structure using LLM
- 🌍 Creates spatial world with locations
- 👥 Creates population with unique identities
- 🗺️ Sets up pathfinding and movement

### 3. Live Simulation Starts
You see:
- **2D world** with agents moving around
- **Mental health colors**: 🟢 Thriving, 🔵 Stable, 🟡 Struggling, 🔴 Crisis
- **Real-time movement** - agents walk between locations
- **Interactive controls** - click, pan, zoom

---

## Quick Presets

Click these for instant societies:
- **Tech Startup** - Burnout culture, high stress
- **Small Town** - Tight-knit community, lower stress
- **University** - Finals week stress, social dynamics

---

## Controls (Once Running)

### Camera
- **WASD** or **Arrow Keys**: Move camera
- **Mouse Wheel**: Zoom in/out
- **Middle Mouse + Drag**: Pan camera

### Interaction
- **Left Click**: Select agent (see their details)
- **SPACE**: Pause/Resume
- **L**: Toggle labels
- **P**: Toggle paths
- **ESC**: Quit

---

## Requirements

Make sure you have:
```bash
# Install dependencies
pip3 install pygame openai python-dotenv

# Set up .env file with your NVIDIA API key
LLM_API_KEY=nvapi-YOUR_KEY_HERE
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-122b-a10b
```

---

## Example Societies to Try

**Modern**:
- "Tech startup in Silicon Valley"
- "Hospital emergency room"
- "Wall Street trading floor"
- "Amazon warehouse"

**Historical**:
- "Medieval village during harvest season"
- "Victorian London factory district"
- "Ancient Roman marketplace"

**Sci-Fi**:
- "Mars colony struggling with isolation"
- "Space station with limited resources"
- "Cyberpunk megacity slums"

**Fantasy**:
- "Wizard academy during exam week"
- "Adventurer's guild in fantasy city"
- "Dwarven mining community"

---

## Performance Tips

**For smooth performance**:
- Start with 50-100 agents
- Increase to 200 if your computer handles it well
- 500+ agents may slow down (but looks amazing!)

**If it's slow**:
- Reduce population size
- Press **P** to hide paths
- Press **L** to hide labels
- Zoom out to see less detail

---

## What You'll See

```
Setup Screen:
┌─────────────────────────────────────┐
│         SYNESTHESIA                 │
│  Mental Health Population Simulator │
│                                     │
│ What society do you want?           │
│ [Tech startup city with burnout...] │
│                                     │
│ Population: [100]                   │
│                                     │
│ [Tech Startup] [Small Town] [Univ] │
│                                     │
│        [🚀 GENERATE & GO]           │
└─────────────────────────────────────┘

↓ Click GO ↓

Live Simulation:
┌─────────────────────────────────────┐
│ 🏢 Office    🏠 Homes    🌳 Park    │
│                                     │
│  🟢 Emma walking to office          │
│  🔵 Alex working at desk            │
│  🟡 Sarah stressed in meeting       │
│  🔴 Michael in crisis, needs help   │
│                                     │
│ Click any agent to see details →   │
└─────────────────────────────────────┘
```

---

## Troubleshooting

**"LLM_API_KEY not found"**
- Make sure `.env` file exists
- Add your NVIDIA API key

**"pygame not found"**
```bash
pip3 install pygame
```

**Window doesn't open**
- Make sure you're not in a headless environment
- Try running on your local machine (not remote server)

**Generation takes forever**
- First time is slower (LLM generating society)
- Should take 30-60 seconds
- Check your internet connection

**Agents not moving**
- They should automatically pick destinations
- Check console for errors
- Try reducing population size

---

## That's It!

Just run:
```bash
python3 synesthesia_launcher.py
```

And watch a living world come to life! 🌍✨
