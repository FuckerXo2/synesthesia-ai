# Synesthesia - Build from Scratch Plan

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Synesthesia Core                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Agent      │  │  Simulation  │  │   Mental     │      │
│  │   System     │  │   Engine     │  │   Health     │      │
│  │              │  │              │  │   Tracker    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Action     │  │   Database   │  │   Oracle     │      │
│  │   Handler    │  │   Layer      │  │   AI         │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components to Build

### 1. Agent System (3-4 days)
**What:** Core agent class with state management

**Files:**
- `synesthesia/agent/agent.py` - Agent class
- `synesthesia/agent/state.py` - Mental health state
- `synesthesia/agent/memory.py` - Agent memory system
- `synesthesia/agent/decision.py` - Decision-making logic

**Key Features:**
- Agent profile (name, age, role, personality)
- Mental health state (anxiety, depression, stress, wellbeing)
- Memory of past events
- Decision-making based on current state
- LLM integration for realistic behavior

**Complexity:** Medium-High
- Need to design state management
- LLM prompting for agent decisions
- Memory system for context

---

### 2. Action System (2-3 days)
**What:** Define and execute daily life actions

**Files:**
- `synesthesia/actions/types.py` - Action type definitions
- `synesthesia/actions/executor.py` - Action execution engine
- `synesthesia/actions/effects.py` - Mental health effects

**Actions to Implement:**
```python
class DailyLifeAction(Enum):
    # Morning
    WAKE_UP = "wake_up"
    MORNING_ROUTINE = "morning_routine"
    
    # Work/School
    GO_TO_WORK = "go_to_work"
    GO_TO_SCHOOL = "go_to_school"
    WORK = "work"
    STUDY = "study"
    TAKE_BREAK = "take_break"
    
    # Social
    SOCIALIZE = "socialize"
    CALL_FRIEND = "call_friend"
    FAMILY_TIME = "family_time"
    ATTEND_EVENT = "attend_event"
    
    # Self-care
    EXERCISE = "exercise"
    MEDITATE = "meditate"
    HOBBY = "hobby"
    RELAX = "relax"
    
    # Mental Health
    SEEK_THERAPY = "seek_therapy"
    TAKE_MEDICATION = "take_medication"
    JOURNAL = "journal"
    REACH_OUT = "reach_out"
    
    # Negative
    ISOLATE = "isolate"
    SUBSTANCE_USE = "substance_use"
    SKIP_WORK = "skip_work"
    CONFLICT = "conflict"
    
    # Evening
    DINNER = "dinner"
    EVENING_ROUTINE = "evening_routine"
    SLEEP = "sleep"
    
    # Passive
    DO_NOTHING = "do_nothing"
```

**Complexity:** Medium
- Need to define effects for each action
- State transitions
- Validation logic

---

### 3. Simulation Engine (4-5 days)
**What:** Main loop that runs the simulation

**Files:**
- `synesthesia/simulation/engine.py` - Main simulation loop
- `synesthesia/simulation/scheduler.py` - Time management
- `synesthesia/simulation/events.py` - Random event generation
- `synesthesia/simulation/runner.py` - CLI runner

**Key Features:**
- Time progression (hourly rounds)
- Agent scheduling (who acts when)
- Event generation (random life events)
- State updates
- Parallel execution (for 10k agents)
- Progress tracking

**Complexity:** High
- Need efficient scheduling for 10k agents
- Parallel processing
- State synchronization
- Event system

---

### 4. Database Layer (2-3 days)
**What:** Store simulation data

**Files:**
- `synesthesia/database/schema.py` - Database schema
- `synesthesia/database/models.py` - ORM models
- `synesthesia/database/queries.py` - Query helpers

**Schema:**
```sql
-- Agents table
CREATE TABLE agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    role TEXT,
    sub_role TEXT,
    gender TEXT,
    family_status TEXT,
    created_at TIMESTAMP
);

-- Mental health states (time series)
CREATE TABLE mental_health_states (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    timestamp TIMESTAMP,
    anxiety REAL,
    depression REAL,
    stress REAL,
    wellbeing REAL,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

-- Actions log
CREATE TABLE actions (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    timestamp TIMESTAMP,
    action_type TEXT,
    action_details JSON,
    mental_health_impact JSON,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

-- Social connections
CREATE TABLE connections (
    id INTEGER PRIMARY KEY,
    agent_id_1 INTEGER,
    agent_id_2 INTEGER,
    connection_type TEXT, -- friend, family, colleague
    strength REAL,
    FOREIGN KEY (agent_id_1) REFERENCES agents(agent_id),
    FOREIGN KEY (agent_id_2) REFERENCES agents(agent_id)
);

-- Life events
CREATE TABLE life_events (
    id INTEGER PRIMARY KEY,
    agent_id INTEGER,
    timestamp TIMESTAMP,
    event_type TEXT,
    event_details JSON,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);
```

**Complexity:** Medium
- Schema design
- ORM setup (SQLAlchemy)
- Query optimization for 10k agents

---

### 5. Mental Health Tracker (2-3 days)
**What:** Track and analyze mental health trends

**Files:**
- `synesthesia/analytics/tracker.py` - Mental health tracking
- `synesthesia/analytics/aggregator.py` - Population-level stats
- `synesthesia/analytics/trends.py` - Trend detection

**Key Features:**
- Individual tracking (time series)
- Population aggregation (by role, age, etc.)
- Trend detection (rising depression, etc.)
- Risk identification (agents in crisis)
- Heatmap generation

**Complexity:** Medium
- Statistical analysis
- Efficient aggregation
- Real-time updates

---

### 6. LLM Integration (2-3 days)
**What:** Connect agents to LLM for realistic behavior

**Files:**
- `synesthesia/llm/client.py` - LLM client wrapper
- `synesthesia/llm/prompts.py` - Prompt templates
- `synesthesia/llm/parser.py` - Response parsing

**Key Features:**
- Agent decision-making prompts
- Interview responses
- Oracle AI queries
- Batch processing for efficiency
- Error handling and retries

**Complexity:** Medium
- Prompt engineering
- Response parsing
- Rate limiting
- Cost optimization

---

### 7. Oracle AI (2-3 days)
**What:** Query system for asking questions about the simulation

**Files:**
- `synesthesia/oracle/oracle.py` - Oracle AI system
- `synesthesia/oracle/queries.py` - Query handlers

**Example Queries:**
- "What's the depression rate in students?"
- "Which demographic is most stressed?"
- "Show me agents in crisis"
- "What's the trend in anxiety over the past week?"

**Complexity:** Medium
- Natural language query parsing
- Database query generation
- LLM integration for complex queries

---

### 8. Interview System (1-2 days)
**What:** Talk to individual agents

**Files:**
- `synesthesia/interview/interviewer.py` - Interview system

**Key Features:**
- Ask agents questions
- Get realistic responses based on state
- Track interview history

**Complexity:** Low-Medium
- LLM prompting
- Context management

---

### 9. Visualization (Optional, 3-4 days)
**What:** Dashboard for viewing simulation

**Files:**
- `synesthesia/viz/dashboard.py` - Web dashboard
- `synesthesia/viz/charts.py` - Chart generation

**Key Features:**
- Population mental health heatmap
- Individual agent timelines
- Real-time updates
- Zoom from macro to micro

**Complexity:** High
- Web framework (Flask/FastAPI)
- Frontend (React/Vue)
- Real-time updates (WebSockets)

---

## Total Effort Estimate

### Core Components (Required)
- Agent System: 3-4 days
- Action System: 2-3 days
- Simulation Engine: 4-5 days
- Database Layer: 2-3 days
- Mental Health Tracker: 2-3 days
- LLM Integration: 2-3 days
- Oracle AI: 2-3 days
- Interview System: 1-2 days

**Total: 18-26 days** (3-4 weeks of full-time work)

### Optional Components
- Visualization: 3-4 days
- Advanced analytics: 2-3 days
- Testing & debugging: 3-5 days

**Grand Total: 26-38 days** (4-6 weeks)

---

## Risk Assessment

### High Risk Areas
1. **Simulation Engine** - Complex, needs to handle 10k agents efficiently
2. **LLM Integration** - Prompt engineering is hard, costs can explode
3. **Time Constraint** - 1 month is tight for this scope

### Mitigation Strategies
1. Start with 100 agents, scale to 10k later
2. Use simple rule-based decisions first, add LLM later
3. Skip visualization for hackathon, focus on CLI
4. Use SQLite for simplicity, not PostgreSQL

---

## Recommended Approach

### Week 1: Core Infrastructure
- Agent System
- Action System
- Database Layer

### Week 2: Simulation
- Simulation Engine
- Mental Health Tracker
- Basic LLM Integration

### Week 3: Intelligence
- Oracle AI
- Interview System
- Advanced LLM prompts

### Week 4: Polish & Demo
- Testing
- Bug fixes
- Demo preparation
- Documentation

---

## Comparison: From Scratch vs. Adapt OASIS

| Aspect | From Scratch | Adapt OASIS |
|--------|--------------|-------------|
| **Time** | 3-4 weeks | 3-4 days |
| **Risk** | High | Low |
| **Quality** | Higher (cleaner) | Medium (hacky) |
| **Learning** | High | Medium |
| **Flexibility** | Complete | Limited |
| **Hackathon Fit** | Risky | Safe |
| **Production Ready** | Yes | No |

---

## My Recommendation

**For Hackathon (1 month):** Adapt OASIS
- Get working prototype in 1 week
- Spend 3 weeks on cool features (Oracle AI, visualization, mental health models)
- Lower risk of not finishing

**For Real Product (3+ months):** Build from Scratch
- Better architecture
- More maintainable
- Cleaner codebase
- Worth the investment

---

## Your Call

What do you want to do?

**Option A:** Adapt OASIS (fast, safe, hacky)
**Option B:** Build from scratch (slow, risky, clean)
**Option C:** Hybrid (start with OASIS, refactor later)

Let me know and I'll proceed accordingly!
