# Synesthesia 🧠

**A living, breathing world of AI agents with realistic mental health dynamics**

Synesthesia is a mental health population simulator that creates a society of AI agents who live their daily lives, experience stress, form relationships, and navigate mental health challenges - just like real people.

## What We Built (So Far)

### ✅ Core Components (COMPLETE)

1. **Database Layer** - Full SQLite schema with ORM
   - Agents, mental health states, actions, connections, events
   - Optimized for 10k+ agents
   - Time-series mental health tracking

2. **Agent System** - Realistic AI people
   - Demographics (age, role, family status)
   - Personality traits
   - Mental health states (anxiety, depression, stress, wellbeing)
   - Daily schedules (work, sleep, free time)
   - Social connections

3. **Action System** - 50+ daily life actions
   - Morning routine, work, social, self-care
   - Mental health care (therapy, medication, support groups)
   - Negative coping (isolation, substance use)
   - Each action has mental health effects

4. **Simulation Engine** - The world runs here
   - Time progression (hourly rounds)
   - Parallel agent processing
   - Population statistics tracking
   - Crisis intervention system

5. **Population Generator** - LLM-powered society creation
   - Describe any society in natural language
   - LLM generates demographics, stressors, baselines
   - Creates thousands of unique agents

### 🚧 In Progress

6. **LLM Integration** - Smart agent decisions
7. **Mental Health Tracker** - Analytics and trends
8. **Oracle AI** - Query the simulation
9. **Interview System** - Talk to agents
10. **Visualization** - Dashboard (optional)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your NVIDIA Build API key
```

### 3. Run a Simulation

```bash
python run_simulation.py
```

You'll be prompted to:
- Describe the society you want to simulate
- Set population size
- Set simulation duration

Example:
```
Describe the society: Tech startup city, 5000 people, burnout culture, high stress
Population size: 5000
Simulation hours: 72
```

The simulation will:
1. Generate society configuration with LLM
2. Create 5000 unique agents
3. Run 72 hours of simulated life
4. Track mental health changes
5. Save everything to database

## Architecture

```
synesthesia/
├── agent/          # Agent system
│   ├── agent.py    # Agent class
│   └── state.py    # Mental health state
├── actions/        # Action system
│   ├── types.py    # Action definitions
│   └── executor.py # Action execution
├── simulation/     # Simulation engine
│   └── engine.py   # Main simulation loop
├── database/       # Database layer
│   ├── schema.py   # Database schema
│   └── models.py   # ORM and queries
├── analytics/      # Analytics (TODO)
├── llm/           # LLM integration (TODO)
├── oracle/        # Oracle AI (TODO)
└── interview/     # Interview system (TODO)
```

## How It Works

### 1. Society Generation

User describes society → LLM generates:
- Demographics (students, workers, parents, etc.)
- Age distributions
- Stressors (academic pressure, work stress, etc.)
- Mental health baselines
- Cultural factors (stigma, help-seeking)

### 2. Agent Creation

For each demographic, generate agents with:
- Unique name, age, personality
- Mental health state (within baseline ranges)
- Daily schedule (work/sleep/active hours)
- Social connections
- Coping mechanisms

### 3. Simulation Loop

For each hour:
1. Determine which agents are awake
2. Each agent chooses an action (rule-based or LLM)
3. Execute action and apply mental health effects
4. Apply random life events
5. Track population statistics
6. Detect crises and intervene

### 4. Mental Health Dynamics

Agents' mental health changes based on:
- **Actions taken** (exercise helps, isolation hurts)
- **Life events** (good sleep, work stress, conflicts)
- **Time decay** (natural recovery/regression to mean)
- **Social connections** (support from friends/family)

## Example Output

```
🌍 Simulation Engine Initialized
   Simulation ID: abc-123
   Population: 5,000 agents
   Duration: 72 hours (72 rounds)
   Time scale: 60 minutes per round

📊 Initial Population State:
   Total: 5,000
   In Crisis: 250 (5.0%)
   Thriving: 1,000 (20.0%)
   Avg Anxiety: 0.45
   Avg Depression: 0.32
   Avg Stress: 0.52

[Day 1, 08:00] Round 1/72 (1.4%) - 4,200 agents active - Crisis: 250
[Day 1, 09:00] Round 2/72 (2.8%) - 4,500 agents active - Crisis: 248
...
[Day 3, 23:00] Round 72/72 (100.0%) - 1,200 agents active - Crisis: 312

✅ SIMULATION COMPLETE
Total actions: 324,000
Crisis interventions: 45
Therapy sessions: 1,234
Social interactions: 45,678
```

## Database Schema

All data is stored in SQLite:

- **agents** - Agent profiles
- **mental_health_states** - Time-series mental health data
- **actions** - Every action taken
- **connections** - Social relationships
- **life_events** - Random events
- **interviews** - Conversations with agents
- **population_stats** - Aggregated statistics

Query the database to:
- Track individual agent journeys
- Analyze population trends
- Identify risk factors
- Measure intervention effectiveness

## What Makes This Special

1. **Realistic Mental Health** - Not just random numbers, actual psychological dynamics
2. **Population Scale** - Simulate entire communities (1k-10k agents)
3. **Emergent Behavior** - Complex patterns emerge from simple rules
4. **Data-Driven** - Everything tracked in database for analysis
5. **LLM-Powered** - Intelligent agent decisions and society generation

## Use Cases

- **Research** - Study mental health interventions at scale
- **Education** - Teach about mental health dynamics
- **Policy** - Test mental health policies before implementation
- **Awareness** - Visualize mental health as a population phenomenon
- **Gaming** - "The Sims meets mental health"

## Roadmap

### Phase 1: Core (DONE ✅)
- [x] Database layer
- [x] Agent system
- [x] Action system
- [x] Simulation engine
- [x] Population generator

### Phase 2: Intelligence (IN PROGRESS 🚧)
- [ ] LLM integration for agent decisions
- [ ] Mental health analytics
- [ ] Oracle AI query system
- [ ] Interview system

### Phase 3: Visualization (FUTURE 🔮)
- [ ] Web dashboard
- [ ] Real-time updates
- [ ] Mental health heatmaps
- [ ] Agent timeline viewer

## Contributing

This is a hackathon project built in record time by AI + human collaboration.

Built with ❤️ for the AMD AI Hackathon

## License

MIT License - Do whatever you want with it!

---

**Note:** This is a simulation for educational/research purposes. Not a substitute for real mental health care. If you or someone you know is in crisis, please contact:
- 988 Suicide & Crisis Lifeline (US)
- Emergency services (911)
