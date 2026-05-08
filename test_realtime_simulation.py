#!/usr/bin/env python3
"""
Real-Time Simulation Test - Agents living continuously like NPCs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.realtime_engine import RealtimeSimulationEngine
from synesthesia.world.location import World, LocationType
from synesthesia.agent.agent import Agent
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("🎮 SYNESTHESIA - REAL-TIME SIMULATION (NPC MODE)")
print("="*60)
print()

# Small test
population = 50
sim_hours = 2  # 2 hours of simulation time

print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {sim_hours} simulation hours")
print(f"🎮 Mode: Real-time continuous (like NPCs in games!)")
print()

# Create society config
config = SocietyConfig(
    society_description="Small town",
    total_population=population,
    demographics={
        "students": 40,
        "workers": 40,
        "parents": 20
    },
    age_ranges={
        "students": (10, 18),
        "workers": (25, 55),
        "parents": (30, 50)
    },
    stressors=["school_pressure", "work_stress", "family_stress"],
    mental_health_baselines={
        "students": {
            "anxiety": (0.3, 0.6),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.7),
            "wellbeing": (0.4, 0.7)
        },
        "workers": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.6),
            "wellbeing": (0.5, 0.7)
        },
        "parents": {
            "anxiety": (0.4, 0.6),
            "depression": (0.2, 0.4),
            "stress": (0.5, 0.7),
            "wellbeing": (0.4, 0.6)
        }
    }
)

# Generate agents
print("👤 Generating agents...")
pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
agents = [Agent.from_dict(a.to_dict()) for a in agents_data]
print(f"✅ Generated {len(agents)} agents!")
print()

# Create world with locations
print("🌍 Creating world...")
world = World()

# Create locations
homes = []
for i in range(population // 3):  # 3 agents per home
    home = world.create_location(
        name=f"Home {i+1}",
        location_type=LocationType.HOME,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=5
    )
    homes.append(home)

schools = []
for i in range(3):
    school = world.create_location(
        name=f"School {i+1}",
        location_type=LocationType.SCHOOL,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=50
    )
    schools.append(school)

workplaces = []
for i in range(5):
    workplace = world.create_location(
        name=f"Office {i+1}",
        location_type=LocationType.WORKPLACE,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=30
    )
    workplaces.append(workplace)

# Add some community locations
park = world.create_location(
    name="Central Park",
    location_type=LocationType.PARK,
    x=50,
    y=50,
    capacity=100
)

gym = world.create_location(
    name="Community Gym",
    location_type=LocationType.GYM,
    x=random.uniform(0, 100),
    y=random.uniform(0, 100),
    capacity=30
)

print(f"✅ Created world with {len(world.locations)} locations:")
print(f"   - {len(homes)} homes")
print(f"   - {len(schools)} schools")
print(f"   - {len(workplaces)} workplaces")
print(f"   - 1 park, 1 gym")
print()

# Initialize database
print("💾 Initializing database...")
db = Database("test_realtime.db")
print("✅ Database ready!")
print()

# Create real-time simulation
print("🎮 Creating real-time simulation engine...")
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="realtime-test-001",
    time_scale=600.0,  # 1 real second = 10 sim minutes (fast for testing)
    llm_client=None  # No LLM for now, using rule-based
)
print()

# Assign agents to starting locations (homes)
print("🏠 Placing agents in homes...")
for i, agent in enumerate(agents):
    home = homes[i % len(homes)]
    engine.move_agent_to_location(agent.agent_id, home.location_id)
print("✅ All agents placed!")
print()

print("🚀 Starting real-time simulation...")
print("   (Watch agents live their lives in real-time!)")
print("   Press Ctrl+C to stop")
print()

# Run simulation
try:
    engine.run(
        target_fps=10.0,  # 10 updates per second
        duration_hours=sim_hours
    )
    
    print("\n📊 Final Statistics:")
    print(f"   Total agents: {len(agents)}")
    print(f"   Total locations: {len(world.locations)}")
    
    # Show where agents ended up
    location_counts = {}
    for agent_id, location_id in engine.agent_locations.items():
        location = world.get_location(location_id)
        if location:
            location_counts[location.name] = location_counts.get(location.name, 0) + 1
    
    print(f"\n📍 Agent distribution:")
    for loc_name, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {loc_name}: {count} agents")
    
    print(f"\n✅ Real-time simulation complete!")
    print(f"📁 Database: test_realtime.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
