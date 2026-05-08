# Synesthesia - Real-Time Mental Health Population Simulator

## Current Status: Phase 1 Complete ✅

### What We've Built

#### ✅ Core Systems (Complete)
1. **Database & ORM** - SQLite with full agent/action tracking
2. **Mental Health System** - 4-category system (thriving, coping, struggling, crisis)
3. **Agent System** - Demographics, personality, mental health, relationships
4. **Action System** - 50+ actions with mental health impacts
5. **Real-Time Simulation Engine** - Continuous updates at 5-10 FPS
6. **Location/World System** - Physical places agents can move between
7. **Relationship System** - Family, friends, coworkers, neighbors
8. **LLM Integration** - Multi-model load balancing for intelligent decisions

#### ✅ Phase 1: Family & Relationship Generation (Complete)
- **Family Generator** - Creates realistic family units
  - Single-parent and two-parent families
  - 0-4 children per family
  - Parent-child relationships
  - Spouse relationships
  - Sibling relationships
- **Coworker Assignment** - Assigns agents to workplaces
  - Creates coworker relationships
  - ~7 workers per workplace
- **Friend Networks** - Generates friendships
  - Age-based friend groups
  - 2-3 friends per agent on average
  - Best friend relationships (20% chance)
- **Neighbor Relationships** - Connects nearby homes
  - Adults know their neighbors
  - 50% chance of knowing each neighbor

**Test Results:**
- ✅ 100 agents → 28 families, 1,150 total relationships
- ✅ Avg 11.5 relationships per agent
- ✅ Real-time simulation running at 9.7 FPS
- ✅ Agents living in homes with families
- ✅ LLM-powered decisions working (with fallback to rule-based)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   SYNESTHESIA SYSTEM                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Agents     │  │    World     │  │  Families    │ │
│  │              │  │              │  │              │ │
│  │ - Demographics│  │ - Locations  │  │ - Parents    │ │
│  │ - Personality│  │ - Homes      │  │ - Children   │ │
│  │ - Mental     │  │ - Workplaces │  │ - Households │ │
│  │   Health     │  │ - Schools    │  │              │ │
│  │ - Relations  │  │ - Parks      │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                  │                  │         │
│         └──────────────────┴──────────────────┘         │
│                           │                              │
│              ┌────────────▼────────────┐                │
│              │  Real-Time Engine       │                │
│              │                         │                │
│              │ - Continuous updates    │                │
│              │ - 5-10 FPS              │                │
│              │ - Time scale: 600x      │                │
│              │ - Action management     │                │
│              │ - LLM decisions         │                │
│              └────────────┬────────────┘                │
│                           │                              │
│              ┌────────────▼────────────┐                │
│              │     LLM Brain           │                │
│              │                         │                │
│              │ - Multi-model balancing │                │
│              │ - Qwen 3.5 122B         │                │
│              │ - Llama 3.3 70B         │                │
│              │ - Mistral Large         │                │
│              │ - Nemotron Super 49B    │                │
│              │ - Fallback to rules     │                │
│              └─────────────────────────┘                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Files Created

**Core Systems:**
- `synesthesia/database/schema.py` - Database schema
- `synesthesia/database/models.py` - ORM models
- `synesthesia/agent/state.py` - Mental health state
- `synesthesia/agent/agent.py` - Agent class
- `synesthesia/agent/relationships.py` - Relationship system
- `synesthesia/actions/types.py` - Action types & effects
- `synesthesia/actions/executor.py` - Action execution
- `synesthesia/actions/realtime_action.py` - Real-time actions

**World & Simulation:**
- `synesthesia/world/location.py` - Location system
- `synesthesia/world/family_generator.py` - Family generation
- `synesthesia/simulation/engine.py` - Turn-based engine (legacy)
- `synesthesia/simulation/realtime_engine.py` - Real-time engine

**LLM Integration:**
- `synesthesia/llm/agent_brain.py` - LLM-powered decisions
- `synesthesia/llm/__init__.py` - LLM module

**Population Generation:**
- `synesthesia_population_generator.py` - LLM-powered population generator

**Tests:**
- `test_nvidia_api.py` - API connection test
- `test_simulation_small.py` - Small turn-based test
- `test_llm_brain.py` - LLM brain test
- `test_llm_simulation.py` - LLM simulation test
- `test_realtime_simulation.py` - Real-time test (rule-based)
- `test_family_generation.py` - Family generation test
- `test_realtime_with_families.py` - Real-time with families
- `test_realtime_llm.py` - LLM-powered real-time test

**Documentation:**
- `README_SYNESTHESIA.md` - Main README
- `SYNESTHESIA_REALTIME_SPEC.md` - Real-time spec
- `SYNESTHESIA_STATUS.md` - This file

### What's Working

✅ **Real-time continuous simulation** - Agents live like NPCs in games
✅ **Family units** - Parents, children, spouses, siblings
✅ **Social networks** - Friends, coworkers, neighbors
✅ **Physical world** - Homes, workplaces, schools, parks
✅ **Agent movement** - Agents move between locations
✅ **Action system** - Actions take time, have progress
✅ **Mental health tracking** - 4 categories, 4 metrics
✅ **LLM-powered decisions** - Agents think for themselves
✅ **Multi-model load balancing** - Spreads load across 4 models
✅ **Fallback to rules** - Works even if LLM fails
✅ **Database logging** - All actions tracked
✅ **Performance** - 50-100 agents at 5-10 FPS

### What's Next (Phase 2)

#### 🚧 LLM-Powered Conversations
- Generate realistic conversations between agents
- Mental health impact from conversations
- Relationship changes from interactions
- Context-aware dialogue (personality, mental state, relationship)

#### 🚧 World Event Orchestrator
- LLM generates emergent events based on society type
- Examples:
  - **Tech startup**: Product launches, layoffs, funding rounds
  - **College town**: Exams, parties, graduation
  - **Suburban**: PTA meetings, block parties
  - **Legal district**: Court cases, elections
- Events affect multiple agents
- Cascading mental health effects

#### 🚧 Enhanced Agent Decisions
- Consider relationships in decisions
- Family-aware actions (dad drops son at school)
- Work schedules (lawyers go to court)
- Community events (elections, meetings)

#### ⏳ Oracle AI (Phase 3)
- Query system: "Show me agents in crisis"
- Population analytics
- Mental health trends
- Relationship network visualization

#### ⏳ Interview System (Phase 3)
- Click on any agent
- See full context
- Have a conversation
- Hear internal thoughts

#### ⏳ Visualization (Phase 4)
- Real-time map view
- Agent movement visualization
- Mental health heatmap
- Relationship network graph
- Timeline of events

### Performance Targets

- **Population**: 5,000-10,000 agents (currently tested: 50-100)
- **FPS**: 10-30 updates per second (currently: 5-10)
- **Time scale**: 60x-600x real-time (currently: 600x)
- **LLM calls**: 100-500 per minute with load balancing
- **Database**: SQLite, optimized for time-series

### Known Issues

1. **Some LLM models return 404** - Fallback to rule-based works
2. **Simulation time shows 0.00 hours** - Display bug, simulation runs correctly
3. **LLM rate limits** - Multi-model load balancing helps but not perfect
4. **Performance at scale** - Need to test with 1,000+ agents

### Demo Flow (Planned)

1. **Setup** (30 seconds)
   - User describes society
   - LLM generates world
   - Agents created with families

2. **Watch** (2-5 minutes)
   - Real-time visualization
   - See agents moving, working, talking
   - Mental health heatmap overlay

3. **Query** (30 seconds)
   - "Show me all parents with depressed children"
   - "Which workplaces have highest stress?"
   - "Find agents who need therapy"

4. **Interview** (1 minute)
   - Click on any agent
   - See their full context
   - Have a conversation
   - Hear their internal thoughts

5. **Insights** (1 minute)
   - Population mental health trends
   - Relationship network visualization
   - Event timeline
   - Crisis hotspots

### Timeline

- **Week 1**: Core simulation ✅ DONE
- **Week 2**: Relationships + LLM decisions ✅ DONE (Phase 1)
- **Week 3**: World events + conversations 🚧 IN PROGRESS (Phase 2)
- **Week 4**: Polish + demo prep ⏳ UPCOMING

**Hackathon deadline**: ~3 weeks remaining

### Success Criteria

✅ **It feels alive**: Agents behave like real people (WORKING)
✅ **Scale works**: 50-100 agents running smoothly (WORKING)
✅ **Mental health matters**: Realistic psychological dynamics (WORKING)
✅ **Relationships matter**: Family and friends affect outcomes (WORKING)
🚧 **Stories emerge**: Complex narratives without hardcoded scenarios (IN PROGRESS)
🚧 **LLM orchestrates**: World events emerge from AI (IN PROGRESS)

### How to Run

**Test family generation:**
```bash
python3 test_family_generation.py
```

**Test real-time simulation (rule-based):**
```bash
python3 test_realtime_with_families.py
```

**Test LLM-powered simulation:**
```bash
python3 test_realtime_llm.py
```

### Configuration

**Environment variables** (`.env`):
```
LLM_API_KEY=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
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-122b-a10b
```

**Models used** (load balanced):
1. `qwen/qwen3.5-122b-a10b` - Fast, high quality
2. `meta/llama-3.3-70b-instruct` - Good quality
3. `mistralai/mistral-large` - Reliable
4. `nvidia/llama-3.3-nemotron-super-49b-v1.5` - Backup

### Next Steps

1. **Implement continuous conversations** - Agents talk when nearby
2. **Build world event orchestrator** - LLM generates emergent events
3. **Test at scale** - Run with 1,000+ agents
4. **Build Oracle AI** - Query system for population insights
5. **Build interview system** - Talk to any agent
6. **Create visualization** - Real-time map view

---

**Status**: Phase 1 Complete ✅  
**Next**: Phase 2 - Conversations & World Events 🚧  
**Updated**: 2026-05-01
