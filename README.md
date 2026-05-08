# SYNESTHESIA

**Mental Health Population Simulator**  
*"The Sims meets Black Mirror"*

A living, breathing simulation of 10,000 AI agents where you can see mental health spread through populations like weather patterns.

🔴 **Powered by AMD** for real-time population analytics

---

## 🎯 What Is This?

Synesthesia is a real-time mental health population simulator that lets you:

- **Generate any society** - Describe it, AI builds it (schools, hospitals, startups, space stations)
- **Watch 10,000 agents live** - Each with their own mental health, relationships, and daily lives
- **Inject events** - "Elections happening", "Economic crisis", "4-day work week" - watch mental health react
- **Query with AI** - Ask "Who's most at risk?" and get instant insights powered by AMD
- **See mental health like weather** - Green = thriving, Red = crisis, visualized in real-time

Built for the **AMD Hackathon 2024**.

---

## 🎬 Demo

**Live Demo:** [https://synesthesia.up.railway.app](https://synesthesia.up.railway.app) *(deploying now)*

**Video Walkthrough:** *(coming soon)*

---

## ✨ Key Features

### 1. **AI-Generated Societies**
Describe any society and LLM generates the complete structure:
- Roles (students, teachers, doctors, engineers)
- Locations (classrooms, hospitals, offices)
- Daily rhythms (when things happen)
- Stressors and support systems

### 2. **Real-Time Simulation**
- 10,000 agents living continuously (not turn-based)
- Each agent moves through 2D space
- Mental health changes in real-time
- Conversations happen automatically

### 3. **Event Injection**
Inject events and watch the population react:
```
"Finals week - extreme stress" → Stress spikes
"Snow day - classes cancelled" → Stress drops
"New policy: 4-day work week" → Wellbeing increases
```

### 4. **Oracle AI (Powered by AMD)**
Ask natural language questions:
- "Who is most at risk right now?"
- "Why are teachers so stressed?"
- "What interventions would help?"
- "How are mental health percentages changing?"

The AI analyzes the entire population and gives you insights in 2-5 seconds.

### 5. **2D Visualization**
- See agents moving through space
- Mental health shown as colors
- Conversation bubbles when agents talk
- Mini-map for navigation
- Click agents to see details

---

## 🏗️ Tech Stack

### Backend
- **Python 3.11+**
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time updates
- **OpenAI SDK** - LLM integration

### Frontend
- **HTML5 Canvas** - 2D rendering
- **JavaScript** - Real-time updates
- **Socket.IO** - WebSocket communication

### AI/LLM
- **NVIDIA Build API** - Society generation, identities, conversations
- **AMD Inference** - Oracle AI (real-time analytics)
- **Models**: Qwen 3.5 122B, Llama 3.3 70B, Mistral Large

### Algorithms
- **A* Pathfinding** - Agent movement
- **Spatial Grid** - Collision detection
- **Rule-Based AI** - Action selection

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/synesthesia.git
cd synesthesia
```

### 2. Install dependencies
```bash
pip install -r requirements_deploy.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run the app
```bash
python3 web_app.py
```

### 5. Open browser
```
http://localhost:5001
```

---

## 🔑 Environment Variables

```bash
# NVIDIA Build API (for society generation)
LLM_API_KEY=your_nvidia_api_key
LLM_BASE_URL=https://integrate.api.nvidia.com/v1

# AMD API (for Oracle AI)
AMD_API_KEY=your_amd_api_key
AMD_BASE_URL=your_amd_endpoint
```

Get API keys:
- **NVIDIA**: https://build.nvidia.com/
- **AMD**: *(your AMD dashboard)*

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         WEB APPLICATION                 │
│  (Flask + SocketIO + HTML5 Canvas)      │
└─────────────────────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
┌──────────────┐      ┌──────────────────┐
│ VISUALIZATION│      │   ORACLE AI      │
│  (2D Canvas) │      │ (AMD-Powered)    │
└──────────────┘      └──────────────────┘
    │                           │
    └─────────────┬─────────────┘
                  ▼
    ┌─────────────────────────┐
    │  SIMULATION ENGINE      │
    │  (Real-Time)            │
    └─────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
┌──────────┐          ┌──────────────┐
│  AGENTS  │          │    WORLD     │
│ (10,000) │          │ (2D Space)   │
└──────────┘          └──────────────┘
```

---

## 🎮 How to Use

### Create a Simulation
1. Enter society description: "High school during finals week"
2. Set population: 100 agents
3. Click "GENERATE & GO"

### Inject Events
1. Type event: "Economic crisis - layoffs announced"
2. Click "⚡ Inject Event"
3. Watch stress levels spike

### Query Oracle AI
1. Click quick query: "Most at Risk"
2. Or type custom: "Why are students struggling?"
3. Get instant insights

### Explore
- **Click agents** to see details
- **Scroll** to zoom
- **Drag** to pan
- **Watch** conversations appear

---

## 🔴 AMD Integration

The **Oracle AI** runs on AMD hardware for real-time population analytics.

**Why AMD for Oracle AI?**
- Most compute-intensive feature
- User-facing (judges will use it)
- Real-time analysis of 10,000 agents
- 2-5 second response time

**Models Used:**
- Primary: Llama 3.3 70B on AMD
- Fallback: NVIDIA models if AMD unavailable

---

## 📈 What You Can Simulate

### Educational
- High school during finals
- University campus
- Online learning platform

### Healthcare
- Hospital emergency room
- Mental health clinic
- Nursing home

### Corporate
- Tech startup with burnout
- Corporate office
- Remote work company

### Extreme
- Space station isolation
- Prison population
- Disaster scenario

---

## 🎯 Use Cases

### 1. Policy Planning
Test interventions before deploying:
- "What if we reduce work hours by 20%?"
- "What if we add 2 counselors?"

### 2. Research
Study population-level mental health dynamics:
- How does stress spread?
- What factors protect mental health?

### 3. Training
Teach mental health professionals:
- Identify at-risk populations
- Practice intervention strategies

### 4. Prevention
Early warning system:
- Detect crisis patterns
- Identify vulnerable groups

---

## 🛠️ Development

### Project Structure
```
synesthesia/
├── web_app.py              # Flask backend
├── templates/
│   └── index.html          # Frontend
├── static/
│   ├── css/style.css       # Styling
│   └── js/app.js           # Canvas rendering
├── synesthesia/
│   ├── agent/              # Agent system
│   ├── world/              # World & locations
│   ├── simulation/         # Simulation engine
│   └── llm/                # LLM integrations
└── requirements_deploy.txt # Dependencies
```

### Key Files
- `web_app.py` - Main Flask app with SocketIO
- `synesthesia/llm/oracle_ai.py` - AMD-powered Oracle
- `synesthesia/world/society_orchestrator.py` - LLM society generation
- `synesthesia/simulation/realtime_engine.py` - Real-time simulation

---

## 🚢 Deployment

### Railway (Recommended)
1. Push to GitHub
2. Connect Railway to repo
3. Add environment variables
4. Deploy

### Render
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements_deploy.txt`
4. Start command: `gunicorn --worker-class eventlet -w 1 web_app:app`

### Fly.io
```bash
fly launch
fly secrets set LLM_API_KEY=your_key
fly deploy
```

---

## 🎨 UI Design

**Black Mirror + Clinical** aesthetic:
- Cold, sterile blues (#58a6ff)
- Monospace fonts (Courier New)
- Sharp edges, no rounded corners
- Glowing elements
- Crosshair cursor
- Dystopian but professional

---

## 🤝 Contributing

This is a hackathon project, but contributions welcome!

1. Fork the repo
2. Create feature branch
3. Make changes
4. Submit PR

---

## 📝 License

MIT License - See LICENSE file

---

## 🏆 Built For

**AMD Hackathon 2024**

**Team:** *(your name)*  
**Built in:** 1 week  
**Lines of Code:** ~5,000

---

## 🙏 Acknowledgments

- **AMD** - For compute credits and API access
- **NVIDIA** - For Build API (society generation)
- **OpenAI** - For SDK and API design

---

## 📧 Contact

- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Email:** your.email@example.com
- **Demo:** [synesthesia.up.railway.app](https://synesthesia.up.railway.app)

---

**See mental health at scale. Built with AMD.** 🔴
