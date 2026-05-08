#!/usr/bin/env python3
"""
Real-Time Simulation with Conversations
Agents live, work, and talk to each other with real dialogue
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
from synesthesia.llm.identity_generator import IdentityGenerator
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("🗣️  SYNESTHESIA - REAL-TIME WITH CONVERSATIONS")
print("="*60)
print()

# Configuration
population = 30  # Small for testing conversations
sim_hours = 2

print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {sim_hours} simulation hours")
print(f"🗣️  Mode: Real-time with conversations!")
print()

# Create society config
config = SocietyConfig(
    society_description="Tech startup",
    total_population=population,
    demographics={
        "engineer": 50,
        "designer": 30,
        "product_manager": 20
    },
    age_ranges={
        "engineer": (24, 35),
        "designer": (23, 32),
        "product_manager": (28, 40)
    },
    stressors=["work_stress", "burnout", "imposter_syndrome"],
    mental_health_baselines={
        "engineer": {
            "anxiety": (0.5, 0.7),
            "depression": (0.3, 0.5),
            "stress": (0.6, 0.8),
            "wellbeing": (0.3, 0.5)
        },
        "designer": {
            "anxiety": (0.4, 0.6),
            "depression": (0.3, 0.5),
            "stress": (0.5, 0.7),
            "wellbeing": (0.4, 0.6)
        },
        "product_manager": {
            "anxiety": (0.6, 0.8),
            "depression": (0.3, 0.5),
            "stress": (0.7, 0.9),
            "wellbeing": (0.3, 0.5)
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

# Generate identities
print("🎭 Generating identities...")
identity_gen = IdentityGenerator()

society_context = "Tech startup with burnout culture, long hours, high stress"

agent_dicts = [
    {
        "agent_id": a.agent_id,
        "name": a.name,
        "age": a.age,
        "role": a.role,
        "personality_traits": a.personality_traits
    }
    for a in agents
]

identities = identity_gen.generate_batch_identities(agent_dicts, society_context, batch_size=10)

for agent in agents:
    agent.identity = identities.get(agent.agent_id)

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

# Create workplaces
workplaces = []
for i in range(3):
    workplace = world.create_location(
        name=f"Office {i+1}",
        location_type=LocationType.WORKPLACE,
        x=random.uniform(0, 100),
        y=random.uniform(0, 100),
        capacity=30
    )
    workplaces.append(workplace)

# Create social locations
cafe = world.create_location(
    name="Coffee Shop",
    location_type=LocationType.RESTAURANT,
    x=50,
    y=50,
    capacity=20
)

park = world.create_location(
    name="Central Park",
    location_type=LocationType.PARK,
    x=60,
    y=60,
    capacity=50
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
print(f"✅ Assigned {len(families)} families!")
print()

# Assign coworkers
workplace_ids = [wp.location_id for wp in workplaces]
workplace_assignments = family_gen.assign_coworkers(workplace_ids)
print()

# Generate friend networks
family_gen.generate_friend_networks(avg_friends=2)
print()

# Show relationship stats
stats = family_gen.get_relationship_stats()
print("📊 Relationship Statistics:")
print(f"   Total relationships: {stats['total_relationships']:,}")
print(f"   Avg per agent: {stats['avg_relationships_per_agent']:.1f}")
print(f"   Friends: {stats['friend_relationships']}")
print(f"   Coworkers: {stats['coworker_relationships']}")
print()

# Initialize LLM brain
print("🧠 Initializing LLM brain...")
llm_brain = AgentBrain(use_load_balancing=True)
print("✅ LLM brain ready!")
print()

# Initialize database
print("💾 Initializing database...")
db = Database("test_realtime_conversations.db")
print("✅ Database ready!")
print()

# Create real-time simulation with conversations
print("🎮 Creating real-time simulation with conversations...")
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="realtime-conversations-001",
    time_scale=600.0,  # 1 real second = 10 sim minutes
    llm_client=llm_brain
)

engine.families = families
engine.workplace_assignments = workplace_assignments
print("✅ Engine ready with conversation system!")
print()

# Place agents in their homes
print("🏠 Placing agents in their homes...")
for family in families:
    for agent_id in family.all_members():
        engine.move_agent_to_location(agent_id, family.home_id)
print("✅ All agents placed!")
print()

print("="*60)
print("🚀 STARTING SIMULATION")
print("="*60)
print("   Agents will:")
print("   - Live their daily lives")
print("   - Move between locations")
print("   - Have conversations when nearby")
print("   - Build memories and relationships")
print()
print("   Watch for 💬 conversation notifications!")
print("   Press Ctrl+C to stop")
print("="*60)
print()

# Run simulation
try:
    engine.run(
        target_fps=5.0,  # Slower for conversation generation
        duration_hours=sim_hours
    )
    
    print("\n" + "="*60)
    print("📊 SIMULATION COMPLETE")
    print("="*60)
    
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
    
    # Conversation summary
    print(f"\n💬 Conversation Summary:")
    print(f"   Total conversations: {len(engine.last_conversation_time)}")
    
    # Show some agent memories
    print(f"\n🧠 Sample Agent Memories:")
    for agent in agents[:3]:
        if agent.memory and agent.memory.memories:
            print(f"\n   {agent.name}:")
            for mem in agent.memory.get_recent_memories(3):
                print(f"      • {mem.description}")
    
    print(f"\n✅ Simulation complete!")
    print(f"📁 Database: test_realtime_conversations.db")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n⚠️  Simulation interrupted by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
