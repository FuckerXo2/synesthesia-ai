# 🌐 Start Synesthesia Web App

## One Command

```bash
python3 web_app.py
```

Then open your browser to: **http://localhost:5000**

---

## What You Get

A **beautiful web interface** where you:

1. **Type what society you want** (e.g., "Tech startup city")
2. **Set population size** (10-200)
3. **Click GO** 🚀
4. **Watch it live in your browser!**

---

## Features

### Setup Screen
- Clean, modern UI
- Text input for society description
- Quick presets (Tech Startup, Small Town, University)
- Population slider

### Loading Screen
- Real-time progress updates
- Shows what's being generated

### Live Simulation
- **2D Canvas** - Watch agents move in real-time
- **Mental Health Colors**:
  - 🟢 Green = Thriving
  - 🔵 Blue = Stable
  - 🟡 Yellow = Struggling
  - 🔴 Red = Crisis
- **Interactive**:
  - Click agents to see details
  - Drag to pan
  - Scroll to zoom
- **Live Stats** - Population breakdown
- **Controls** - Pause, resume, stop

---

## Requirements

```bash
pip3 install flask flask-socketio python-socketio openai python-dotenv
```

Or:
```bash
pip3 install -r requirements_web.txt
```

---

## How It Works

### Backend (Flask + SocketIO)
- Flask serves the web interface
- SocketIO provides real-time updates
- Simulation runs in background thread
- Updates sent to browser 10 times per second

### Frontend (HTML + Canvas + JavaScript)
- HTML5 Canvas for rendering
- JavaScript handles interaction
- Real-time updates via WebSocket
- Smooth 60 FPS rendering

---

## Example Societies

Try these:
- "Tech startup with burnout culture"
- "Hospital emergency room during pandemic"
- "Wall Street trading floor"
- "Medieval village during harvest"
- "Space station with limited resources"
- "University campus during finals week"

---

## Controls

**In Browser**:
- 🖱️ **Click agent** - See their details
- 🖱️ **Drag** - Pan camera
- 🔍 **Scroll** - Zoom in/out
- ⏸️ **Pause button** - Pause/resume
- ⏹️ **Stop button** - Return to setup

---

## Performance

**Recommended**:
- 50-100 agents: Smooth performance
- 100-200 agents: Good performance
- Keep browser tab active for best FPS

**If slow**:
- Reduce population size
- Close other browser tabs
- Use Chrome/Firefox (better Canvas performance)

---

## Troubleshooting

**"Address already in use"**
- Port 5000 is taken
- Kill other Flask apps or change port in `web_app.py`

**"LLM_API_KEY not found"**
- Make sure `.env` file exists with your NVIDIA API key

**Simulation not updating**
- Check browser console for errors
- Make sure WebSocket connection is active
- Try refreshing the page

**Generation takes forever**
- First generation is slower (LLM creating society)
- Should take 30-60 seconds
- Check your internet connection

---

## Architecture

```
Browser (http://localhost:5000)
    ↓
Flask Web Server
    ↓
SocketIO (WebSocket)
    ↓
Simulation Thread
    ↓
Synesthesia Engine
```

**Real-time updates**:
1. Simulation runs in background thread
2. Updates sent via WebSocket every 100ms
3. Browser receives updates
4. Canvas re-renders at 60 FPS

---

## Deployment

### Local Development
```bash
python3 web_app.py
```

### Production (with Gunicorn)
```bash
gunicorn --worker-class eventlet -w 1 web_app:app
```

### Docker (future)
```bash
docker build -t synesthesia .
docker run -p 5000:5000 synesthesia
```

---

## That's It!

Just run:
```bash
python3 web_app.py
```

Open browser to **http://localhost:5000**

And watch a living world in your browser! 🌍✨
