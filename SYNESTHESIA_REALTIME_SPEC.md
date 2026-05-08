# Synesthesia - Real-Time Life Simulator

## Vision
A living, breathing world where 5,000-10,000 AI agents live continuous lives like NPCs in games. Not turn-based - **real-time continuous simulation** where you can watch agents move, interact, and live.

## Core Concept
**"The Sims meets Black Mirror meets GTA"**
- Agents live in real-time (not hourly ticks)
- Physical world with locations
- Real relationships (families, coworkers, friends)
- Mental health tracked like weather patterns
- LLM orchestrates emergent daily life
- God's-eye view: zoom from city-wide to individual

## What We've Built ✅

### 1. Real-Time Simulation Engine
- **Continuous updates** at 10-30 FPS
- **Time scale**: 1 real second = 10 simulation minutes (configurable)
- **Actions take time**: Walking = 5 min, Work = 1 hour, Sleep = 8 hours
- **Agents update every frame** like NPCs in games

### 2. Physical World System
- **Locations**: Homes, workplaces, schools, parks, gyms, etc.
- **Spatial coordinates**: (x, y) for visualization
- **Capacity limits**: Locations can fill up
- **Movement**: Agents move between locations

### 3. Action System
- **Real-time actions** with duration
- **Action states**: Not started, in progress, completed, interrupted
- **Progress tracking**: See how far along an action is
- **50+ action types** with realistic durations

### 4. Relationship System
- **Relationship types**: Parent, child, spouse, sibling, friend, coworker, boss, etc.
- **Relationship quality**: Trust, affection, respect
- **Interaction history**: Track conversations and events
- **Bidirectional**: Both agents know about the relationship

### 5. Agent System
- **Demographics**: Age, role, family status
- **Personality traits**: Introverted, perfectionist, optimistic, etc.
- **Mental health**: Anxiety, depression, stress, wellbeing
- **Schedules**: Work hours, sleep hours, active hours
- **Relationships**: Integrated relationship manager

### 6. LLM Integration
- **Multi-model load balancing**: Qwen 3.5, Llama 3.3, Mistral, Nemotron
- **Agent decisions**: LLM decides what agents do based on context
- **Conversations**: Real dialogue between agents
- **Internal thoughts**: Agents have inner monologues

## What We're Building Next 🚧

### Phase 1: Family & Relationship Generation
**Goal**: Generate realistic families and social networks

**Features**:
- Family units (parents + children)
- Households (who lives together)
- Coworker groups (who works together)
- Friend networks (social connections)
- Neighbor relationships

**Implementation**:
```python
# Generate families
families = generate_families(population, demographics)
# families = [
#   Family(parents=[Agent#1, Agent#2], children=[Agent#3, Agent#4]),
#   Family(parents=[Agent#5], children=[Agent#6]),  # Single parent
#   ...
# ]

# Assign homes
assign_families_to_homes(families, homes)

# Create coworker groups
assign_coworkers(agents, workplaces)

# Generate friendships
generate_friend_networks(agents, config)
```

### Phase 2: LLM-Powered Agent Decisions
**Goal**: Agents make intelligent decisions based on full context

**Context for decisions**:
- Current time and location
- Mental health state
- Personality traits
- Relationships (who they care about)
- Recent events
- Nearby agents
- World state

**Example**:
```
Agent: Dad (stressed, at home, 6pm)
Context: Son just got home from school, looks sad
Relationships: Son (child, strong bond)
Recent: Had stressful day at work

LLM Decision: "Talk to son about his day" (15 min conversation)
→ Generates actual dialogue
→ Updates both agents' mental health
→ Strengthens relationship
```

### Phase 3: World Event Orchestrator
**Goal**: LLM generates emergent events based on society type

**How it works**:
```python
# Every simulation hour, LLM decides what's happening
world_events = llm.orchestrate_world_events(
    society_type="tech startup city",
    current_time="2pm Tuesday",
    recent_events=["Product launch yesterday", "Layoffs last week"],
    agent_states=population_summary
)

# Returns:
# [
#   Event(type="investor_meeting", location=Office#3, participants=[CEO, investors]),
#   Event(type="team_standup", location=Office#1, participants=engineering_team),
#   Event(type="school_pickup", location=School#1, participants=parents),
# ]
```

**Society-specific events**:
- **Tech startup**: Product launches, funding rounds, hackathons, layoffs
- **College town**: Exams, parties, sports games, graduation
- **Suburban**: PTA meetings, block parties, little league games
- **Legal district**: Court cases, depositions, bar association events

### Phase 4: Continuous Conversations
**Goal**: Agents have real conversations when they interact

**Features**:
- **Proximity-based**: Agents talk when in same location
- **Context-aware**: Conversations reflect relationship and situation
- **Mental health impact**: Good conversations help, bad ones hurt
- **Relationship changes**: Conversations strengthen or weaken bonds

**Example**:
```
Dad and Son at home, 6pm
Dad notices Son is sad (mental health: depression 0.7)

LLM generates conversation:
Dad: "Hey buddy, you seem down. Rough day at school?"
Son: "I failed my math test. I studied so hard but I just... I'm so stupid."
Dad: "You're not stupid. Math is hard. Want to go over it together?"
Son: "I guess... thanks dad."

Result:
- Son: depression -0.1, wellbeing +0.1
- Dad: stress +0.05 (worried about son), wellbeing +0.05 (helped son)
- Relationship: trust +0.05, affection +0.05
```

### Phase 5: Emergent Life Stories
**Goal**: Complex narratives emerge from simple rules

**Examples of emergent stories**:
1. **Burnout Cascade**
   - Startup announces layoffs
   - 50 agents lose jobs
   - Mental health crashes
   - Families affected (stress spreads)
   - Some seek therapy, some isolate
   - Community support groups form

2. **Family Drama**
   - Dad works long hours (stress high)
   - Misses son's school events
   - Son develops anxiety
   - Mom notices, talks to dad
   - Dad reduces hours, spends time with son
   - Family mental health improves

3. **Community Response**
   - Multiple agents in crisis
   - Neighbors notice
   - Community meeting organized
   - Support network forms
   - Mental health resources shared
   - Crisis rate decreases

## Technical Architecture

### Real-Time Loop
```python
while simulation_running:
    delta_time = get_delta_time()  # Real seconds elapsed
    sim_delta = delta_time * time_scale  # Simulation seconds
    
    # Update all agents
    for agent in agents:
        if agent.action_complete():
            # LLM decides next action
            next_action = llm.decide_action(agent, world_state)
            agent.start_action(next_action)
        
        agent.update(sim_delta)
    
    # Check for interactions
    for location in world.locations:
        agents_here = location.get_agents()
        if len(agents_here) >= 2:
            # LLM generates interactions
            interactions = llm.generate_interactions(agents_here, location)
            apply_interactions(interactions)
    
    # World events
    if should_generate_events():
        events = llm.orchestrate_events(world_state)
        apply_events(events)
    
    sleep(1.0 / target_fps)
```

### Data Flow
```
User Input: "Tech startup city, 5000 people, burnout culture"
    ↓
LLM generates world structure
    ↓
Generate 5000 agents with relationships
    ↓
Place agents in world (homes, offices, etc.)
    ↓
Start real-time simulation
    ↓
Every frame:
  - Update agent actions
  - Generate interactions
  - Orchestrate events
  - Track mental health
    ↓
User can:
  - Watch in real-time
  - Query: "Show me agents in crisis"
  - Interview: "Talk to Agent #42"
  - Zoom: City view → Neighborhood → Individual
```

## Performance Targets

- **Population**: 5,000-10,000 agents
- **FPS**: 10-30 updates per second
- **Time scale**: 60x-600x (1 real min = 1-10 sim hours)
- **LLM calls**: ~100-500 per minute (with load balancing)
- **Database**: SQLite, optimized for time-series queries

## Demo Flow

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

## Success Criteria

✅ **It feels alive**: Agents behave like real people, not robots
✅ **Stories emerge**: Complex narratives without hardcoded scenarios
✅ **Scale works**: 5,000+ agents running smoothly
✅ **Mental health matters**: Realistic psychological dynamics
✅ **Relationships matter**: Family and friends affect outcomes
✅ **LLM orchestrates**: World events emerge from AI, not scripts

## Current Status

**Completed**:
- ✅ Real-time simulation engine
- ✅ Location/world system
- ✅ Action system with durations
- ✅ Relationship system
- ✅ Agent system with mental health
- ✅ LLM integration with load balancing
- ✅ Basic test running (50 agents, 2 hours)

**In Progress**:
- 🚧 Family generation
- 🚧 LLM-powered agent decisions
- 🚧 World event orchestrator

**Next Up**:
- ⏳ Continuous conversations
- ⏳ Oracle AI (query system)
- ⏳ Interview system
- ⏳ Visualization/UI

## Timeline

- **Week 1**: Core simulation (DONE ✅)
- **Week 2**: Relationships + LLM decisions (IN PROGRESS 🚧)
- **Week 3**: World events + conversations
- **Week 4**: Polish + demo prep

**Hackathon deadline**: 1 month from now
