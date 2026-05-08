# Phase 4: 2D Spatial World - GTA-Style Visualization 🎮

## What We Built

### Phase 4A: Spatial Foundation ✅

Built the foundation for a **GTA-style 2D world** where agents move through continuous space instead of teleporting between abstract locations.

---

## 1. Spatial World System ✅

**File**: `synesthesia/world/spatial_world.py`

### SpatialLocation
Extends base `Location` with spatial properties:
- **Boundaries**: Rectangle (x, y, width, height)
- **Entry points**: Where agents spawn when entering
- **Obstacles**: For pathfinding (future)
- **Spatial queries**: `contains_point()`, `distance_to()`, `get_random_point_inside()`

### SpatialAgent
Agents with physics and movement:
- **Position**: (x, y) coordinates in meters
- **Velocity**: (vx, vy) for smooth movement
- **Speed**: Movement speed (default 2 m/s)
- **Target**: Where agent is moving to
- **Path**: List of waypoints to follow
- **Movement state**: `is_moving`, `current_location_id`

### SpatialWorld
Manages the 2D world:
- **World size**: Configurable (default 1000m x 1000m)
- **Spatial grid**: Fast proximity queries (50m cells)
- **Agent management**: Add, update, query agents
- **Location management**: Create, query locations
- **Proximity queries**: `get_nearby_agents(radius)`, `get_agents_at_location()`

**Example**:
```python
# Create world
world = SpatialWorld(width=1000, height=1000)

# Create location
office = world.create_location(
    name="Tech Office",
    location_type=LocationType.WORKPLACE,
    x=100, y=100,
    width=80, height=60
)

# Add agent
spatial_agent = world.add_agent(
    agent_id=1,
    x=50, y=50,
    speed=2.0
)

# Move agent
world.move_agent_to_location(agent_id=1, location_id=office.location_id)

# Update (every frame)
world.update_agent(agent_id=1, delta_time=0.016)  # 60 FPS
```

---

## 2. Movement & Pathfinding System ✅

**File**: `synesthesia/world/movement_system.py`

### Pathfinder
A* pathfinding algorithm:
- **Grid-based**: 2m resolution for pathfinding
- **Obstacle avoidance**: Avoids obstacles in locations
- **Path simplification**: Removes unnecessary waypoints using line-of-sight
- **Direct path optimization**: Uses straight line if clear
- **8-directional movement**: Cardinal + diagonal

### MovementSystem
High-level movement API:
- `move_agent_to_position(agent_id, x, y)` - Move to specific coordinates
- `move_agent_to_location(agent_id, location_id)` - Move to location entry point
- `stop_agent(agent_id)` - Stop movement
- `update(delta_time)` - Update all agents

**Example**:
```python
movement = MovementSystem(spatial_world)

# Move agent to specific position
movement.move_agent_to_position(agent_id=1, target_x=500, target_y=300)

# Move agent to location
movement.move_agent_to_location(agent_id=1, location_id=office.location_id)

# Update every frame
movement.update(delta_time=0.016)
```

**Pathfinding Features**:
- ✅ A* algorithm with heuristic
- ✅ Obstacle detection
- ✅ Path simplification (removes redundant waypoints)
- ✅ Direct path optimization
- ✅ Smooth movement along path

---

## 3. 2D Visualization (Pygame) ✅

**File**: `synesthesia/visualization/visualizer.py`

### Visualizer
Real-time 2D rendering:
- **Window**: 1200x800 default, resizable
- **Camera**: Pan, zoom, follow
- **Rendering**: 60 FPS target
- **Interactive**: Click agents, drag camera, zoom

### Visual Elements

**Locations**:
- Color-coded by type (homes=brown, offices=blue, parks=green, etc.)
- Shows boundaries and names
- Agents inside are visible

**Agents**:
- **Color = Mental Health**:
  - 🟢 Green: Thriving
  - 🔵 Blue: Stable
  - 🟡 Yellow: Struggling
  - 🔴 Red: Crisis
- Shows name labels (when zoomed in)
- Selection indicator (white ring)
- Movement paths (dotted lines)

**UI Overlay**:
- Current simulation time
- FPS counter
- Agent count
- Mental health summary (counts by category)
- Controls help

**Agent Details Panel** (when selected):
- Name, age, role
- Mental health stats (anxiety, depression, stress, wellbeing)
- Current position
- Movement status
- Recent actions

### Camera Controls
- **WASD / Arrow keys**: Pan camera
- **Mouse wheel**: Zoom in/out
- **Middle mouse drag**: Pan camera
- **Left click**: Select agent
- **SPACE**: Pause/resume
- **L**: Toggle labels
- **P**: Toggle paths
- **ESC**: Quit

---

## 4. Test Script ✅

**File**: `test_spatial_visualization.py`

Creates a test world with:
- **30 agents** moving around
- **Small city layout**:
  - 6 homes (residential area)
  - 2 offices (center)
  - 1 park (bottom)
  - 1 grocery store
  - 1 coffee shop
  - 1 gym
- **Continuous movement**: Agents pick random destinations
- **Real-time rendering**: 60 FPS

**Run it**:
```bash
python3 test_spatial_visualization.py
```

---

## Architecture

```
Spatial World
  ├── SpatialWorld (manages world)
  │   ├── SpatialLocations (physical places)
  │   ├── SpatialAgents (agents with position/velocity)
  │   └── Spatial Grid (fast proximity queries)
  │
  ├── MovementSystem (high-level movement)
  │   └── Pathfinder (A* pathfinding)
  │
  └── Visualizer (pygame rendering)
      ├── Camera (pan/zoom)
      ├── Renderer (draw world)
      └── UI (overlay + agent details)
```

---

## What This Enables

### Before Phase 4:
```python
# Abstract locations - agents teleport
agent.location = "Office"
# No spatial awareness
# No continuous movement
# No visualization
```

### After Phase 4:
```python
# Real 2D world - agents walk through space
agent.position = (150.5, 230.8)
agent.velocity = (1.2, 0.8)
agent.path = [(150, 230), (200, 250), (250, 250)]

# Watch agents move in real-time
# See mental health as colors
# Click agents to see details
# Pan/zoom around the world
```

---

## Key Features

✅ **Continuous 2D space** - Not grid-based, smooth movement
✅ **A* pathfinding** - Agents navigate around obstacles
✅ **Real-time visualization** - 60 FPS pygame rendering
✅ **Mental health colors** - Visual feedback at a glance
✅ **Interactive camera** - Pan, zoom, select agents
✅ **Agent details panel** - Click to see full info
✅ **Spatial queries** - Fast proximity detection
✅ **Smooth movement** - Velocity-based physics
✅ **Path following** - Agents follow waypoints
✅ **Location boundaries** - Agents move to entry points

---

## Performance

**Spatial Grid Optimization**:
- World divided into 50m x 50m cells
- Agents indexed by cell
- Proximity queries only check nearby cells
- O(1) insertion, O(k) query where k = nearby agents

**Rendering Optimization**:
- Off-screen culling (don't draw what you can't see)
- Conditional label rendering (only when zoomed in)
- 60 FPS target with 30+ agents

---

## What's Next (Phase 4B-D)

### Phase 4B: Enhanced Pathfinding
- [ ] Better obstacle avoidance
- [ ] Dynamic obstacles (other agents)
- [ ] Collision detection
- [ ] Formation movement (groups)

### Phase 4C: Visual Polish
- [ ] Agent sprites (instead of circles)
- [ ] Animated movement
- [ ] Conversation indicators (speech bubbles)
- [ ] Mental health color gradients
- [ ] Location interiors (zoom in to see inside buildings)
- [ ] Day/night cycle visuals

### Phase 4D: Granular Actions
- [ ] Break down "work" into micro-actions:
  - Walk to desk
  - Sit down
  - Open laptop
  - Type
  - Take break
  - Walk to coffee machine
  - Return to desk
- [ ] Action animations
- [ ] Context-aware actions (different actions at different locations)

### Phase 4E: Integration with Existing Systems
- [ ] Integrate with real-time simulation engine
- [ ] Trigger conversations when agents are nearby
- [ ] Show conversation indicators
- [ ] Update mental health in real-time
- [ ] Show relationship connections (lines between agents)

---

## Demo

```bash
# Install pygame (if not already)
pip3 install pygame

# Run spatial visualization test
python3 test_spatial_visualization.py

# Controls:
# - WASD: Move camera
# - Mouse wheel: Zoom
# - Click: Select agent
# - SPACE: Pause
# - L: Toggle labels
# - P: Toggle paths
```

---

## Files Created

**Core Systems**:
- `synesthesia/world/spatial_world.py` - Spatial world, locations, agents
- `synesthesia/world/movement_system.py` - Pathfinding and movement
- `synesthesia/visualization/visualizer.py` - Pygame 2D renderer
- `synesthesia/visualization/__init__.py` - Module init

**Tests**:
- `test_spatial_visualization.py` - Interactive visualization test

**Documentation**:
- `PHASE_4_SPATIAL_WORLD.md` - This file

**Dependencies**:
- Updated `requirements.txt` - Added pygame>=2.5.0

---

## Success Metrics

✅ **2D continuous space**: Agents have (x, y) positions
✅ **Smooth movement**: Velocity-based physics
✅ **Pathfinding**: A* algorithm working
✅ **Real-time rendering**: 60 FPS pygame visualization
✅ **Mental health colors**: Visual feedback
✅ **Interactive**: Click, pan, zoom
✅ **Agent details**: Full info panel
✅ **Spatial queries**: Fast proximity detection
✅ **Location boundaries**: Agents respect spatial constraints

---

## Timeline

- **Week 1**: Core simulation ✅ DONE
- **Week 2**: Relationships + LLM decisions ✅ DONE
- **Week 3**: Society Orchestrator + Identity + Conversations ✅ DONE
- **Week 4**: Spatial World + Visualization ✅ Phase 4A DONE
  - Phase 4A: Spatial foundation ✅ DONE
  - Phase 4B: Enhanced pathfinding ⏳ NEXT
  - Phase 4C: Visual polish ⏳ TODO
  - Phase 4D: Granular actions ⏳ TODO

**Hackathon deadline**: ~1 week remaining

---

## Conclusion

**Phase 4A is complete!** 🎉

We now have a **GTA-style 2D world** where:
- Agents move through continuous space (not teleporting)
- A* pathfinding navigates around obstacles
- Real-time pygame visualization at 60 FPS
- Mental health visible as colors
- Interactive camera (pan, zoom, select)
- Agent details panel on click

**This is the foundation for the full spatial simulation!**

Next steps:
1. Integrate with existing real-time simulation
2. Add conversation indicators
3. Polish visuals (sprites, animations)
4. Add granular actions (micro-behaviors)

---

**Status**: Phase 4A Complete ✅  
**Next**: Phase 4B - Enhanced Pathfinding 🚧  
**Updated**: 2026-05-02
