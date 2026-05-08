#!/usr/bin/env python3
"""
Real-Time Simulation with LLM-Powered Agents
Agents make intelligent decisions based on their personality and mental health
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.realtime_engine import RealtimeSimulationEngine
from synesthesia.world.location import World, LocationType
from synesthesia.world.family_generator import FamilyGenerator
from synesthesia.agent.agent import Agent
from synesthesia.llm.agent_brain import AgentBrain
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("🧠 SYNESTHESIA - LLM-POWERED REAL-TIME SIMULATION")
print("="*60)
print()

# Configuration
population = 50  # Smaller for LLM testing
sim_hours = 2  # 2 hours

print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {sim_hours} simulation hours")
print(f"🧠 Mode: LLM-powered intelligent agents!")
print()

# Create society config
config = SocietyConfig(
    society_description="Small suburban community",
    total_population=population,
    demographics={
        "parents": 30,
        "children": 25,
        "young_adults": 20,
        "workers": 15,
        "retirees": 10
    },
    age_ranges={
        "parents": (30, 50),
        "children": (5, 17),
        "young_adults": (18, 25),
        "workers": (26, 60),
        "retirees": (61, 80)
    },
    stressors=["work_stress", "family_stress", "school_pressure"],
    mental_health_baselines={
        "parents": {
            "anxiety": (0.4, 0.6),
            "depression": (0.2, 0.4),
            "stress": (0.5, 0.7),
            "wellbeing": (0.4, 0.6)
        },
        "children": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.3, 0.5),
            "wellbeing": (0.5, 0.7)
        },
        "young_adults": {
            "anxiety": (0.4, 0.6),
            "depression": (0.3, 0.5),
            "stress": (0.4, 0.6),
            "wellbeing": (0.4, 0.6)
        },
        "workers": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.6),
            "wellbeing": (0.5, 0.7)
        },
        "retirees": {
            "anxiety": (0.2, 0.4),
            "depression": (0.3, 0.5),
            "stress": (0.2, 0.4),
            "wellbeing": (0.5, 0.7)
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

# Generate families and relationships
print("👨‍👩‍👧‍👦 Generating families and relationships...")
family_gen = FamilyGenerator(agents)
families = family_gen.generate_families()
print()

# Create world
print("🌍 Creating world...")
world = World()

# Create homes
homes = []
for i in range(len(families) + 5):
    home = world.create_location(
        name=f"Home {i+1}",
        location_type=LocationType.HOME,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=6
    )
    homes.append(home)

# Create schools
schools = []
for i in range(2):
    school = world.create_location(
        name=f"School {i+1}",
        location_type=LocationType.SCHOOL,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=50
    )
    schools.append(school)

# Create workplaces
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

# Add community locations
park = world.create_location(
    name="Central Park",
    location_type=LocationType.PARK,
    x=50,
    y=50,
    capacity=100
)

print(f"✅ Created world with {len(world.locations)} locations")
print()

# Assign families to homes
print("🏠 Assigning families to homes...")
home_assignments = {}
for i, family in enumerate(families):
    home = homes[i % len(homes)]
    family.home_id = home.location_id
    home_assignments[home.location_id] = family.all_members()
print(f"✅ Assigned {len(families)} families to homes!")
print()

# Assign coworkers
workplace_ids = [wp.location_id for wp in workplaces]
workplace_assignments = family_gen.assign_coworkers(workplace_ids)
print()

# Generate friend networks
family_gen.generate_friend_networks(avg_friends=2)
print()

# Initialize LLM brain
print("🧠 Initializing LLM brain...")
llm_brain = AgentBrain(use_load_balancing=True)
print("✅ LLM brain ready with multi-model load balancing!")
print(f"   Models: {', '.join(AgentBrain.AVAILABLE_MODELS)}")
print()

# Initialize database
print("💾 Initializing database...")
db = Database("test_realtime_llm.db")
print("✅ Database ready!")
print()

# Create real-time simulation with LLM
print("🎮 Creating LLM-powered real-time simulation...")
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="realtime-llm-001",
    time_scale=600.0,  # 1 real second = 10 sim minutes
    llm_client=llm_brain
)

engine.families = families
engine.workplace_assignments = workplace_assignments
print()

# Place agents in their homes
print("🏠 Placing agents in their homes...")
for family in families:
    for agent_id in family.all_members():
        engine.move_agent_to_location(agent_id, family.home_id)
print("✅ All agents placed!")
print()

print("🚀 Starting LLM-powered simulation...")
print("   (Agents are thinking for themselves!)")
print("   Press Ctrl+C to stop")
print()

# Run simulation
try:
    engine.run(
        target_fps=5.0,  # Slower FPS for LLM calls
        duration_hours=sim_hours
    )
    
    print("\n📊 Final Statistics:")
    print(f"   Total agents: {len(agents)}")
    print(f"   Total families: {len(families)}")
    
    # Mental health summary
    total_anxiety = sum(a.mental_health.anxiety for a in agents)
    total_depression = sum(a.mental_health.depression for a in agents)
    total_stress = sum(a.mental_health.stress for a in agents)
    total_wellbeing = sum(a.mental_health.wellbeing for a in agents)
    
    print(f"\n🧠 Mental Health Summary:")
    print(f"   Avg Anxiety: {total_anxiety / len(agents):.2f}")
    print(f"   Avg Depression: {total_depression / len(agents):.2f}")
    print(f"   Avg Stress: {total_stress / len(agents):.2f}")
    print(f"   Avg Wellbeing: {total_wellbeing / len(agents):.2f}")
    
    # Show some agent thoughts
    print(f"\n💭 Sample Agent Thoughts:")
    for i, agent in enumerate(agents[:3]):
        print(f"\n   {agent.name} (age {agent.age}, {agent.role}):")
        print(f"   Mental state: {agent.mental_health.category}")
        try:
            thought = llm_brain.generate_internal_monologue(
                {
                    "name": agent.name,
                    "age": agent.age,
                    "role": agent.role,
                    "personality_traits": agent.personality_traits,
                    "mental_health": {
                        "anxiety": agent.mental_health.anxiety,
                        "depression": agent.mental_health.depression,
                        "stress": agent.mental_health.stress,
                        "wellbeing": agent.mental_health.wellbeing,
                        "category": agent.mental_health.category
                    }
                },
                agent.recent_actions[-5:]
            )
            print(f"   💭 \"{thought}\"")
        except Exception as e:
            print(f"   💭 (Could not generate thought: {e})")
    
    print(f"\n✅ LLM-powered simulation complete!")
    print(f"📁 Database: test_realtime_llm.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
