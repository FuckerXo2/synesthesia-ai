# 🌐 Synesthesia Web App

**"The Sims meets Black Mirror" - Now in Your Browser!**

A living mental health population simulator with AI agents - accessible via web browser.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install flask flask-socketio python-socketio openai python-dotenv
```

### 2. Start Server
```bash
python3 web_app.py
```

### 3. Open Browser
Go to: **http://localhost:5000**

### 4. Use It!
1. Type what society you want (e.g., "Tech startup city")
2. Set population (50-200 recommended)
3. Click **GENERATE & GO** 🚀
4. Watch agents live their lives in real-time!

---

## 📸 What You'll See

### Setup Screen
```
┌─────────────────────────────────────────┐
│           SYNESTHESIA                   │
│   Mental Health Population Simulator    │
│   "The Sims meets Black Mirror"         │
│                                         │
│ What society do you want to simulate?  │
│ [Tech startup city with burnout...]    │
│                                         │
│ Population Size (10-200)                │
│ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━] │
│                                         │
│ Quick presets:                          │
│ [🏢 Tech Startup] [🏘️ Small Town]      │
│ [🎓 University]                         │
│                                         │
│      [🚀 GENERATE & GO]                 │
└─────────────────────────────────────────┘
```

### Live Simulation
```
┌─────────────────────────────────────────┐
│ SYNESTHESIA    12:34 PM    [⏸️][⏹️]     │
├─────────────────────────────────────────┤
│                                    │    │
│  🏢 Office    🏠 Homes    🌳 Park  │ 📊 │
│                                    │    │
│   🟢 Emma walking to office        │ 🟢 │
│   🔵 Alex working at desk          │ 42 │
│   🟡 Sarah stressed in meeting     │    │
│   🔴 Michael in crisis             │ 🔵 │
│                                    │ 38 │
│  Click agent to see details →      │    │
│                                    │ 🟡 │
│                                    │ 15 │
│                                    │    │
│                                    │ 🔴 │
│                                    │ 5  │
└─────────────────────────────────────────┘
```

---

## ✨ Features

### 🎨 Beautiful UI
- Modern, clean design
- Smooth animations
- Responsive layout
- Dark theme (easy on eyes)

### 🧠 LLM-Powered
- Describe any society, AI generates it
- Each agent has unique backstory
- Realistic behavior emerges

### 🎮 Interactive
- **Click agents** - See their full details
- **Drag canvas** - Pan around the world
- **Scroll** - Zoom in/out
- **Pause/Resume** - Control simulation
- **Real-time stats** - Population breakdown

### 🌍 2D Living World
- Agents move through continuous space
- Mental health shown as colors
- Locations (homes, offices, parks, etc.)
- Pathfinding and navigation

### 📊 Live Statistics
- Population mental health breakdown
- Real-time updates
- Individual agent details

---

## 🎯 Example Societies

### Modern
- "Tech startup with burnout culture"
- "Hospital emergency room"
- "Wall Street trading floor"
- "Amazon warehouse"
- "Call center"

### Historical
- "Medieval village during harvest"
- "Victorian factory district"
- "Ancient Roman marketplace"

### Sci-Fi
- "Mars colony with isolation"
- "Space station with limited resources"
- "Cyberpunk megacity slums"

### Educational
- "University during finals week"
- "High school with social pressure"
- "Elementary school playground"

---

## 🛠️ Technical Details

### Stack
- **Backend**: Flask + SocketIO (Python)
- **Frontend**: HTML5 Canvas + JavaScript
- **Real-time**: WebSocket communication
- **AI**: OpenAI API (NVIDIA Build)

### Architecture
```
Browser
  ↓ HTTP
Flask Server
  ↓ WebSocket
Simulation Thread
  ↓
Synesthesia Engine
  ↓
LLM (NVIDIA API)
```

### Performance
- **Backend**: 10 updates/second
- **Frontend**: 60 FPS rendering
- **Latency**: <100ms update delay
- **Capacity**: 200 agents smoothly

---

## 🎮 Controls

### Mouse
- **Left Click**: Select agent
- **Left Drag**: Pan camera
- **Scroll Wheel**: Zoom in/out

### Buttons
- **⏸️ Pause**: Pause/resume simulation
- **⏹️ Stop**: Stop and return to setup

### Keyboard (future)
- **Space**: Pause/resume
- **R**: Reset camera
- **+/-**: Zoom

---

## 📦 Files

### Web App
- `web_app.py` - Flask backend server
- `templates/index.html` - Main HTML page
- `static/css/style.css` - Styling
- `static/js/app.js` - Frontend JavaScript

### Documentation
- `WEB_APP_README.md` - This file
- `START_WEB_APP.md` - Quick start guide

### Requirements
- `requirements_web.txt` - Python dependencies

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
LLM_API_KEY=nvapi-YOUR_KEY_HERE
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-122b-a10b
```

### Server Settings (web_app.py)
```python
# Port
port = 5000

# Host (0.0.0.0 = accessible from network)
host = '0.0.0.0'

# Debug mode
debug = True
```

---

## 🚀 Deployment

### Local Development
```bash
python3 web_app.py
```
Access at: http://localhost:5000

### Production (Gunicorn)
```bash
pip3 install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 web_app:app
```

### Docker (future)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements_web.txt
CMD ["python", "web_app.py"]
```

---

## 🐛 Troubleshooting

### "Address already in use"
**Problem**: Port 5000 is taken
**Solution**: 
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in web_app.py
```

### "LLM_API_KEY not found"
**Problem**: Missing API key
**Solution**: Create `.env` file with your NVIDIA API key

### Simulation not updating
**Problem**: WebSocket connection lost
**Solution**: 
- Refresh browser
- Check browser console for errors
- Restart server

### Slow performance
**Problem**: Too many agents or slow computer
**Solution**:
- Reduce population to 50-100
- Close other browser tabs
- Use Chrome/Firefox (better Canvas performance)

### Generation takes forever
**Problem**: LLM is slow or rate limited
**Solution**:
- Wait 30-60 seconds (first generation is slower)
- Check internet connection
- Verify API key is valid

---

## 🎓 How It Works

### 1. User Input
User describes society and sets population

### 2. Generation (30-60s)
- LLM generates society structure
- Creates locations (homes, offices, etc.)
- Creates agents with unique identities
- Sets up spatial world

### 3. Simulation Loop
```python
while running:
    # Update agents (movement, actions)
    update_simulation()
    
    # Send state to browser via WebSocket
    emit('simulation_update', state)
    
    # Wait 100ms (10 FPS)
    sleep(0.1)
```

### 4. Browser Rendering
```javascript
// Receive updates via WebSocket
socket.on('simulation_update', (state) => {
    // Update UI
    updateStats(state.stats);
    
    // Render canvas (60 FPS)
    render(state.agents, state.locations);
});
```

---

## 🌟 What Makes This Special

### 1. **Web-Based**
- No installation needed (just browser)
- Works on any device
- Easy to share (just send URL)

### 2. **Real-Time**
- Live updates via WebSocket
- Smooth 60 FPS rendering
- Instant interaction

### 3. **Beautiful UI**
- Modern design
- Intuitive controls
- Responsive layout

### 4. **Powerful Backend**
- LLM-powered generation
- Deep psychological simulation
- Emergent behavior

---

## 📈 Roadmap

### Phase 1 ✅
- Basic web interface
- Real-time visualization
- Agent movement
- Mental health colors

### Phase 2 🚧
- Conversations (speech bubbles)
- Relationship visualization
- Memory timeline
- Agent interviews

### Phase 3 📋
- Multi-user support
- Save/load simulations
- Export data (CSV, JSON)
- Analytics dashboard

### Phase 4 📋
- Mobile app
- VR/AR support
- AI-powered insights
- Predictive analytics

---

## 🤝 Contributing

Want to improve Synesthesia?

1. Fork the repo
2. Create feature branch
3. Make changes
4. Submit pull request

---

## 📄 License

MIT License - Use freely!

---

## 🎉 That's It!

Just run:
```bash
python3 web_app.py
```

Open browser to **http://localhost:5000**

And watch a living world in your browser! 🌍✨

---

**Built for AMD Hackathon 2024**
**"The Sims meets Black Mirror"**
