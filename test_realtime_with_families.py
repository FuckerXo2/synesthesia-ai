#!/usr/bin/env python3
"""
Real-Time Simulation with Families - Agents living with their families
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.realtime_engine import RealtimeSimulationEngine
from synesthesia.world.location import World, LocationType
from synesthesia.world.family_generator import FamilyGenerator
from synesthesia.agent.agent import Agent
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("🎮 SYNESTHESIA - REAL-TIME SIMULATION WITH FAMILIES")
print("="*60)
print()

# Configuration
population = 100
sim_hours = 4  # 4 hours of simulation time

print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {sim_hours} simulation hours")
print(f"🎮 Mode: Real-time continuous with families!")
print()

# Create society config
config = SocietyConfig(
    society_description="Suburban community with families",
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

# Create world with locations
print("🌍 Creating world...")
world = World()

# Create homes (one per family + extras for singles)
homes = []
for i in range(len(families) + 10):
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
for i in range(3):
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
for i in range(10):
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

gym = world.create_location(
    name="Community Gym",
    location_type=LocationType.GYM,
    x=random.uniform(0, 100),
    y=random.uniform(0, 100),
    capacity=30
)

cafe = world.create_location(
    name="Coffee Shop",
    location_type=LocationType.RESTAURANT,
    x=random.uniform(0, 100),
    y=random.uniform(0, 100),
    capacity=20
)

print(f"✅ Created world with {len(world.locations)} locations:")
print(f"   - {len(homes)} homes")
print(f"   - {len(schools)} schools")
print(f"   - {len(workplaces)} workplaces")
print(f"   - 1 park, 1 gym, 1 coffee shop")
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

# Assign coworkers to workplaces
workplace_ids = [wp.location_id for wp in workplaces]
workplace_assignments = family_gen.assign_coworkers(workplace_ids)
print()

# Generate friend networks
family_gen.generate_friend_networks(avg_friends=3)
print()

# Generate neighbor relationships
home_ids = [h.location_id for h in homes]
family_gen.generate_neighbor_relationships(home_ids, home_assignments)
print()

# Show relationship stats
stats = family_gen.get_relationship_stats()
print("📊 Relationship Statistics:")
print(f"   Total relationships: {stats['total_relationships']:,}")
print(f"   Avg per agent: {stats['avg_relationships_per_agent']:.1f}")
print(f"   Family: {stats['family_relationships']}")
print(f"   Friends: {stats['friend_relationships']}")
print(f"   Coworkers: {stats['coworker_relationships']}")
print(f"   Neighbors: {stats['neighbor_relationships']}")
print()

# Show example family
print("👨‍👩‍👧‍👦 Example Family:")
example_family = families[0]
print(f"   Family {example_family.family_id} (Home {example_family.home_id}):")
for parent_id in example_family.parents:
    parent = agents[parent_id - 1]
    print(f"      👤 {parent.name} (age {parent.age}, {parent.role})")
if example_family.children:
    for child_id in example_family.children:
        child = agents[child_id - 1]
        print(f"         👶 {child.name} (age {child.age})")
print()

# Initialize database
print("💾 Initializing database...")
db = Database("test_realtime_families.db")
print("✅ Database ready!")
print()

# Create real-time simulation
print("🎮 Creating real-time simulation engine...")
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="realtime-families-001",
    time_scale=600.0,  # 1 real second = 10 sim minutes
    llm_client=None  # No LLM for now
)

# Store family and workplace assignments in engine
engine.families = families
engine.workplace_assignments = workplace_assignments
print()

# Place agents in their homes
print("🏠 Placing agents in their homes...")
for family in families:
    for agent_id in family.all_members():
        engine.move_agent_to_location(agent_id, family.home_id)
print("✅ All agents placed in their homes!")
print()

print("🚀 Starting real-time simulation...")
print("   (Watch families live their lives!)")
print("   Press Ctrl+C to stop")
print()

# Run simulation
try:
    engine.run(
        target_fps=10.0,
        duration_hours=sim_hours
    )
    
    print("\n📊 Final Statistics:")
    print(f"   Total agents: {len(agents)}")
    print(f"   Total families: {len(families)}")
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
    
    # Show mental health summary
    total_anxiety = sum(a.mental_health.anxiety for a in agents)
    total_depression = sum(a.mental_health.depression for a in agents)
    total_stress = sum(a.mental_health.stress for a in agents)
    total_wellbeing = sum(a.mental_health.wellbeing for a in agents)
    
    print(f"\n🧠 Mental Health Summary:")
    print(f"   Avg Anxiety: {total_anxiety / len(agents):.2f}")
    print(f"   Avg Depression: {total_depression / len(agents):.2f}")
    print(f"   Avg Stress: {total_stress / len(agents):.2f}")
    print(f"   Avg Wellbeing: {total_wellbeing / len(agents):.2f}")
    
    print(f"\n✅ Real-time simulation with families complete!")
    print(f"📁 Database: test_realtime_families.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
