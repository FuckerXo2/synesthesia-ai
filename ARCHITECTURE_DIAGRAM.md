# Synesthesia Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SYNESTHESIA SYSTEM                           │
│                  "The Sims meets Black Mirror"                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐    ┌──────────────────────┐             │
│  │  2D Visualization    │    │   Oracle AI          │             │
│  │  (Pygame)            │    │   (Query System)     │             │
│  │                      │    │                      │             │
│  │  • 60 FPS rendering  │    │  • "Show crisis"     │             │
│  │  • Mental health     │    │  • "Who's isolated?" │             │
│  │    colors            │    │  • Interview agents  │             │
│  │  • Click agents      │    │                      │             │
│  │  • Pan/zoom camera   │    │                      │             │
│  └──────────────────────┘    └──────────────────────┘             │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SIMULATION ENGINE LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Real-Time Simulation Engine                                 │  │
│  │  • Continuous time (not turn-based)                          │  │
│  │  • 10-30 FPS updates                                         │  │
│  │  • Time scale: 1 real sec = 60 sim secs                     │  │
│  │  • Proximity-based interactions                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Society Orchestrator (LLM-Powered)                          │  │
│  │  • Generates society structures from user description        │  │
│  │  • Creates roles, events, stressors, support systems         │  │
│  │  • Orchestrates emergent events                              │  │
│  │  • No hardcoded templates                                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        SPATIAL WORLD LAYER                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Spatial World (2D Continuous Space)                         │  │
│  │  • 1000m x 1000m world                                       │  │
│  │  • Spatial grid (50m cells) for fast queries                │  │
│  │  • Locations with boundaries                                │  │
│  │  • Agents with position & velocity                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Movement System                                             │  │
│  │  • A* pathfinding (2m grid resolution)                      │  │
│  │  • Obstacle avoidance                                        │  │
│  │  • Path simplification                                       │  │
│  │  • Smooth velocity-based movement                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Agent (5,000-10,000 agents)                                 │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │   Identity     │  │ Mental Health  │  │ Relationships  │ │  │
│  │  │                │  │                │  │                │ │  │
│  │  │ • Backstory    │  │ • Anxiety      │  │ • Family       │ │  │
│  │  │ • Values       │  │ • Depression   │  │ • Friends      │ │  │
│  │  │ • Fears        │  │ • Stress       │  │ • Coworkers    │ │  │
│  │  │ • Goals        │  │ • Wellbeing    │  │ • Quality      │ │  │
│  │  │ • Quirks       │  │ • Category     │  │ • History      │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  │                                                              │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │    Memory      │  │    Actions     │  │   Position     │ │  │
│  │  │                │  │                │  │                │ │  │
│  │  │ • Recent       │  │ • Work         │  │ • (x, y)       │ │  │
│  │  │ • Trauma       │  │ • Sleep        │  │ • Velocity     │ │  │
│  │  │ • Positive     │  │ • Socialize    │  │ • Path         │ │  │
│  │  │ • By person    │  │ • Exercise     │  │ • Speed        │ │  │
│  │  │ • Resilience   │  │ • 50+ types    │  │                │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        LLM INTELLIGENCE LAYER                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  LLM Services (NVIDIA Build API)                             │  │
│  │                                                              │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │  Population    │  │   Identity     │  │ Conversation   │ │  │
│  │  │  Generator     │  │   Generator    │  │  Generator     │ │  │
│  │  │                │  │                │  │                │ │  │
│  │  │ • Demographics │  │ • Backstories  │  │ • Dialogue     │ │  │
│  │  │ • Roles        │  │ • Values       │  │ • Thoughts     │ │  │
│  │  │ • Families     │  │ • Fears        │  │ • Impact       │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  │                                                              │  │
│  │  ┌────────────────┐  ┌────────────────┐                     │  │
│  │  │    Society     │  │  Agent Brain   │                     │  │
│  │  │  Orchestrator  │  │  (Decisions)   │                     │  │
│  │  │                │  │                │                     │  │
│  │  │ • Structures   │  │ • Actions      │                     │  │
│  │  │ • Events       │  │ • Reasoning    │                     │  │
│  │  │ • Stressors    │  │ • Context      │                     │  │
│  │  └────────────────┘  └────────────────┘                     │  │
│  │                                                              │  │
│  │  Model: Qwen 3.5 122B (qwen/qwen3.5-122b-a10b)             │  │
│  │  Multi-model load balancing: 4 models                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Database (SQLite)                                           │  │
│  │                                                              │  │
│  │  • Agents table                                             │  │
│  │  • Actions table                                            │  │
│  │  • Mental health history                                    │  │
│  │  • Relationships table                                      │  │
│  │  • Conversations table                                      │  │
│  │  • Events table                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Population Generation
```
User Description
      │
      ▼
Society Orchestrator (LLM)
      │
      ├─► Roles, Events, Stressors
      ├─► Locations
      └─► Social Structures
      │
      ▼
Population Generator (LLM)
      │
      ├─► Demographics
      ├─► Families
      └─► Relationships
      │
      ▼
Identity Generator (LLM)
      │
      └─► Unique backstories for each agent
      │
      ▼
Agents Created
```

### 2. Real-Time Simulation Loop
```
┌─────────────────────────────────────────┐
│  Simulation Engine (10-30 FPS)         │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  For each agent:                        │
│  1. Update current action               │
│  2. Check if action complete            │
│  3. Decide next action (LLM or rules)   │
│  4. Update position (movement system)   │
│  5. Check for nearby agents             │
│  6. Trigger conversations (if nearby)   │
│  7. Update mental health                │
│  8. Create memories                     │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Visualizer (60 FPS)                    │
│  • Render locations                     │
│  • Render agents (colored by MH)        │
│  • Render paths                         │
│  • Render UI                            │
└─────────────────────────────────────────┘
```

### 3. Conversation Flow
```
Agent A nearby Agent B
      │
      ▼
Check cooldown (30 min)
      │
      ▼
Check relationship (30% friends, 5% strangers)
      │
      ▼
Conversation Generator (LLM)
      │
      ├─► Context: identities, memories, relationship
      ├─► Generate dialogue (3-6 exchanges)
      ├─► Include internal thoughts
      └─► Calculate mental health impact
      │
      ▼
Apply Effects
      │
      ├─► Update mental health (both agents)
      ├─► Update relationship quality
      └─► Create memories (both agents)
```

### 4. Movement Flow
```
Agent needs to move to location
      │
      ▼
Movement System
      │
      ▼
Pathfinder (A*)
      │
      ├─► Check if direct path clear
      ├─► If not, run A* pathfinding
      ├─► Simplify path (remove redundant waypoints)
      └─► Return waypoints
      │
      ▼
Agent follows path
      │
      ├─► Move towards current waypoint
      ├─► Update velocity
      ├─► Update position
      └─► When reached, move to next waypoint
      │
      ▼
Agent arrives at destination
```

---

## Component Interactions

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Visualizer │────▶│ Spatial World│────▶│    Agents    │
│   (Pygame)   │     │   (2D Space) │     │  (Identity)  │
└──────────────┘     └──────────────┘     └──────────────┘
       │                     │                     │
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Camera    │     │   Movement   │     │ Mental Health│
│  (Pan/Zoom)  │     │   System     │     │    State     │
└──────────────┘     └──────────────┘     └──────────────┘
                             │                     │
                             │                     │
                             ▼                     ▼
                     ┌──────────────┐     ┌──────────────┐
                     │  Pathfinder  │     │ Relationships│
                     │     (A*)     │     │   Manager    │
                     └──────────────┘     └──────────────┘
                                                  │
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │ Conversation │
                                          │  Generator   │
                                          └──────────────┘
                                                  │
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │  LLM Client  │
                                          │ (NVIDIA API) │
                                          └──────────────┘
```

---

## File Structure Map

```
synesthesia/
│
├── agent/                    # AGENT LAYER
│   ├── agent.py             # Agent class
│   ├── state.py             # Mental health state
│   ├── relationships.py     # Relationship system
│   └── identity.py          # Identity & memory
│
├── actions/                  # ACTION SYSTEM
│   ├── types.py             # Action types
│   ├── executor.py          # Action execution
│   └── realtime_action.py   # Real-time actions
│
├── database/                 # DATA LAYER
│   ├── schema.py            # Database schema
│   └── models.py            # Database ORM
│
├── llm/                      # LLM INTELLIGENCE LAYER
│   ├── agent_brain.py       # LLM decision making
│   ├── identity_generator.py # Generate identities
│   └── conversation_generator.py # Generate conversations
│
├── simulation/               # SIMULATION ENGINE LAYER
│   ├── engine.py            # Turn-based engine
│   └── realtime_engine.py   # Real-time engine
│
├── world/                    # SPATIAL WORLD LAYER
│   ├── location.py          # Abstract locations
│   ├── spatial_world.py     # 2D spatial world
│   ├── movement_system.py   # Pathfinding
│   ├── society_orchestrator.py # LLM society generation
│   └── family_generator.py  # Family generation
│
├── visualization/            # USER INTERFACE LAYER
│   └── visualizer.py        # Pygame 2D renderer
│
└── utils/
    └── ...
```

---

## Technology Stack

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  • Python 3.x                           │
│  • Pygame (2D rendering)                │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Simulation Layer                │
│  • Real-time engine                     │
│  • Event-driven system                  │
│  • Spatial grid optimization            │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Intelligence Layer              │
│  • NVIDIA Build API                     │
│  • Qwen 3.5 122B                        │
│  • Multi-model load balancing           │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Data Layer                      │
│  • SQLite                               │
│  • JSON (config)                        │
└─────────────────────────────────────────┘
```

---

## Scalability Architecture

```
Current: Single Process
┌─────────────────────────────────────────┐
│  Main Process                           │
│  ├─ Simulation Engine                   │
│  ├─ Spatial World                       │
│  ├─ LLM Client                          │
│  └─ Visualizer                          │
└─────────────────────────────────────────┘

Future: Distributed (10,000+ agents)
┌─────────────────────────────────────────┐
│  Master Process                         │
│  ├─ Orchestrator                        │
│  └─ Visualizer                          │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Worker Processes (N workers)           │
│  ├─ Simulation Engine (shard 1)         │
│  ├─ Simulation Engine (shard 2)         │
│  └─ Simulation Engine (shard N)         │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  LLM Pool (M clients)                   │
│  ├─ LLM Client 1 (Qwen 3.5)            │
│  ├─ LLM Client 2 (Llama 3.3)           │
│  ├─ LLM Client 3 (Mistral)             │
│  └─ LLM Client 4 (Nemotron)            │
└─────────────────────────────────────────┘
```

---

This architecture enables:
- ✅ **Emergent complexity** from simple rules
- ✅ **Scalability** to 10,000+ agents
- ✅ **Real-time visualization** at 60 FPS
- ✅ **Deep individual simulation** with LLM intelligence
- ✅ **Spatial awareness** in 2D continuous space
