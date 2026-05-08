#!/usr/bin/env python3
"""
Quick test simulation - 100 agents, 24 hours
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.engine import SimulationEngine
from synesthesia_population_generator import SocietyGenerator, PopulationGenerator

print("="*60)
print("🧪 SYNESTHESIA TEST - Small Simulation")
print("="*60)
print()

# Small test configuration
description = "Small college town, 100 students, high academic stress"
population = 100
total_hours = 24

print(f"📝 Society: {description}")
print(f"👥 Population: {population}")
print(f"⏱️  Duration: {total_hours} hours")
print()

# Generate society
print("🤖 Generating society configuration...")
society_gen = SocietyGenerator()

try:
    config = society_gen.generate_society_config(description, population)
    print("✅ Society configuration generated!")
except Exception as e:
    print(f"⚠️  LLM failed: {e}")
    print("Using default config...")
    config = society_gen._get_default_config(description, population)

print()
print("📊 Demographics:")
for role, pct in config.demographics.items():
    count = int(population * (pct / 100))
    print(f"   {role}: {pct}% ({count} people)")
print()

# Generate agents
print("👤 Generating agents...")
pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
print(f"✅ Generated {len(agents_data)} agents!")
print()

# Initialize database
print("💾 Initializing database...")
db = Database("test_simulation.db")
print("✅ Database ready!")
print()

# Create Agent objects
print("📥 Loading agents...")
from synesthesia.agent.agent import Agent

agents = []
for agent_data in agents_data:
    agent = Agent.from_dict(agent_data.to_dict())
    agents.append(agent)

db.batch_insert_agents([a.to_dict() for a in agents])
print(f"✅ Loaded {len(agents)} agents!")
print()

# Create simulation
print("🌍 Creating simulation engine...")
engine = SimulationEngine(
    agents=agents,
    db=db,
    total_hours=total_hours,
    minutes_per_round=60,
    use_llm=False,
    max_workers=4
)
print()

# Show initial state
summary = engine.get_simulation_summary()
print("📊 Initial State:")
print(f"   In Crisis: {summary['population']['in_crisis']} ({summary['population']['crisis_rate']*100:.1f}%)")
print(f"   Thriving: {summary['population']['thriving']} ({summary['population']['thriving_rate']*100:.1f}%)")
print(f"   Avg Distress: {summary['mental_health']['avg_distress']:.2f}")
print()

print("🚀 Starting simulation...")
print()

# Run simulation
try:
    engine.run()
    
    # Show final state
    print("\n📊 Final State:")
    summary = engine.get_simulation_summary()
    print(f"   In Crisis: {summary['population']['in_crisis']} ({summary['population']['crisis_rate']*100:.1f}%)")
    print(f"   Thriving: {summary['population']['thriving']} ({summary['population']['thriving_rate']*100:.1f}%)")
    print(f"   Avg Distress: {summary['mental_health']['avg_distress']:.2f}")
    print()
    
    print("✅ Test simulation complete!")
    print(f"📁 Database: test_simulation.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
