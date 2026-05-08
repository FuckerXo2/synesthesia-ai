#!/usr/bin/env python3
"""
Full Synesthesia Simulation - Society Orchestrator + Real-Time Engine
LLM generates society structure, then runs real-time simulation with emergent events
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.realtime_engine import RealtimeSimulationEngine
from synesthesia.world.location import World, LocationType
from synesthesia.world.family_generator import FamilyGenerator
from synesthesia.world.society_orchestrator import SocietyOrchestrator
from synesthesia.agent.agent import Agent
from synesthesia.llm.agent_brain import AgentBrain
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("🌍 SYNESTHESIA - FULL SIMULATION")
print("   Society Orchestrator + Real-Time Engine")
print("="*60)
print()

# Configuration
population = 100
sim_hours = 4

# User describes the society
society_description = input("Describe the society you want to simulate: ").strip()
if not society_description:
    society_description = "Tech startup city with burnout culture, long hours, high stress"
    print(f"Using default: {society_description}")

print()
print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {sim_hours} simulation hours")
print(f"🧠 Mode: LLM-powered with emergent events!")
print()

# Step 1: Generate society structure
print("STEP 1: Generate Society Structure")
print("-"*60)
orchestrator = SocietyOrchestrator()
society_structure = orchestrator.generate_society_structure(
    user_description=society_description,
    population=population
)
print(orchestrator.get_society_summary())

# Step 2: Generate population based on society structure
print("STEP 2: Generate Population")
print("-"*60)

# Convert society structure to SocietyConfig
roles = society_structure.get('roles', {})
demographics = {role: details['percentage'] for role, details in roles.items()}

# Create age ranges (simplified)
age_ranges = {}
for role in roles.keys():
    if 'child' in role.lower() or 'adolescent' in role.lower():
        age_ranges[role] = (5, 17)
    elif 'elder' in role.lower() or 'retiree' in role.lower():
        age_ranges[role] = (60, 80)
    else:
        age_ranges[role] = (22, 60)

# Mental health baselines from society structure
mental_health_baselines = {}
for role, details in roles.items():
    stress = details.get('stress_baseline', 0.5)
    mental_health_baselines[role] = {
        "anxiety": (stress - 0.1, stress + 0.1),
        "depression": (0.2, 0.4),
        "stress": (stress - 0.1, stress + 0.1),
        "wellbeing": (0.6 - stress, 0.8 - stress)
    }

config = SocietyConfig(
    society_description=society_description,
    total_population=population,
    demographics=demographics,
    age_ranges=age_ranges,
    stressors=society_structure.get('stressors', []),
    mental_health_baselines=mental_health_baselines
)

print("👤 Generating agents...")
pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
agents = [Agent.from_dict(a.to_dict()) for a in agents_data]

# Update work hours from society structure
for agent in agents:
    role_info = roles.get(agent.role, {})
    if 'work_hours' in role_info:
        work_start, work_end = role_info['work_hours']
        if work_end < work_start:  # Wraps around midnight
            agent.work_hours = list(range(work_start, 24)) + list(range(0, work_end))
        else:
            agent.work_hours = list(range(work_start, work_end))

print(f"✅ Generated {len(agents)} agents!")
print()

# Step 3: Generate families and relationships
print("STEP 3: Generate Families & Relationships")
print("-"*60)
family_gen = FamilyGenerator(agents)
families = family_gen.generate_families()
print()

# Step 4: Create world based on society structure
print("STEP 4: Create World")
print("-"*60)
world = World()

locations_config = society_structure.get('locations', {})

# Create locations based on society structure
all_locations = []

for loc_type, loc_info in locations_config.items():
    count = loc_info.get('count', 10)
    capacity = loc_info.get('capacity', 50)
    
    # Map to LocationType
    if 'home' in loc_type.lower() or 'apartment' in loc_type.lower():
        location_type = LocationType.HOME
    elif 'work' in loc_type.lower() or 'office' in loc_type.lower() or 'hub' in loc_type.lower():
        location_type = LocationType.WORKPLACE
    elif 'school' in loc_type.lower():
        location_type = LocationType.SCHOOL
    elif 'cafe' in loc_type.lower() or 'restaurant' in loc_type.lower():
        location_type = LocationType.RESTAURANT
    elif 'gym' in loc_type.lower() or 'fitness' in loc_type.lower():
        location_type = LocationType.GYM
    elif 'hospital' in loc_type.lower() or 'clinic' in loc_type.lower() or 'counseling' in loc_type.lower():
        location_type = LocationType.HOSPITAL
    elif 'park' in loc_type.lower():
        location_type = LocationType.PARK
    else:
        location_type = LocationType.OTHER
    
    for i in range(min(count, 50)):  # Limit to 50 per type
        loc = world.create_location(
            name=f"{loc_type} {i+1}",
            location_type=location_type,
            x=random.uniform(0, 100),
            y=random.uniform(0, 100),
            capacity=capacity
        )
        all_locations.append(loc)

print(f"✅ Created world with {len(world.locations)} locations")
print()

# Step 5: Assign families to homes
print("STEP 5: Assign Families to Homes")
print("-"*60)
homes = world.get_locations_by_type(LocationType.HOME)
if not homes:
    # Create homes if none exist
    for i in range(len(families) + 10):
        home = world.create_location(
            name=f"Home {i+1}",
            location_type=LocationType.HOME,
            x=random.uniform(0, 100),
            y=random.uniform(0, 100),
            capacity=6
        )
        homes.append(home)

home_assignments = {}
for i, family in enumerate(families):
    home = homes[i % len(homes)]
    family.home_id = home.location_id
    home_assignments[home.location_id] = family.all_members()

print(f"✅ Assigned {len(families)} families to homes!")
print()

# Assign coworkers
workplaces = world.get_locations_by_type(LocationType.WORKPLACE)
if workplaces:
    workplace_ids = [wp.location_id for wp in workplaces]
    workplace_assignments = family_gen.assign_coworkers(workplace_ids)
    print()

# Generate friend networks
family_gen.generate_friend_networks(avg_friends=2)
print()

# Step 6: Initialize LLM brain
print("STEP 6: Initialize LLM Brain")
print("-"*60)
llm_brain = AgentBrain(use_load_balancing=True)
print("✅ LLM brain ready!")
print()

# Step 7: Initialize database
print("STEP 7: Initialize Database")
print("-"*60)
db = Database("synesthesia_full_simulation.db")
print("✅ Database ready!")
print()

# Step 8: Create real-time simulation
print("STEP 8: Create Real-Time Simulation")
print("-"*60)
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="full-sim-001",
    time_scale=600.0,  # 1 real second = 10 sim minutes
    llm_client=llm_brain
)

# Attach orchestrator to engine
engine.society_orchestrator = orchestrator
engine.families = families

print("✅ Real-time engine ready!")
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
print("   The society is now alive!")
print("   - Agents living with families")
print("   - LLM making decisions")
print("   - Emergent events happening")
print("   - Mental health evolving")
print()
print("   Press Ctrl+C to stop")
print("="*60)
print()

# Run simulation
try:
    engine.run(
        target_fps=5.0,
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
    
    # Crisis count
    crisis_count = sum(1 for a in agents if a.mental_health.category.value == 'crisis')
    print(f"   Agents in crisis: {crisis_count}")
    
    print(f"\n✅ Simulation complete!")
    print(f"📁 Database: synesthesia_full_simulation.db")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n⚠️  Simulation interrupted by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
