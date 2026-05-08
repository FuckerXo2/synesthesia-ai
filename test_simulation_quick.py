#!/usr/bin/env python3
"""
Quick test simulation - uses default config, no LLM needed
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.engine import SimulationEngine
from synesthesia_population_generator import SocietyConfig, PopulationGenerator

print("="*60)
print("🧪 SYNESTHESIA QUICK TEST - No LLM")
print("="*60)
print()

# Use default configuration (no LLM call)
population = 100
total_hours = 24

print(f"👥 Population: {population}")
print(f"⏱️  Duration: {total_hours} hours")
print()

# Create default config
config = SocietyConfig(
    society_description="Test college town",
    total_population=population,
    demographics={
        "students": 60,
        "professors": 10,
        "staff": 15,
        "retail_workers": 10,
        "unemployed": 5
    },
    age_ranges={
        "students": (18, 25),
        "professors": (30, 65),
        "staff": (25, 60),
        "retail_workers": (20, 50),
        "unemployed": (20, 60)
    },
    stressors=["academic_pressure", "financial_stress", "social_isolation"],
    mental_health_baselines={
        "students": {
            "anxiety": (0.4, 0.7),
            "depression": (0.2, 0.5),
            "stress": (0.5, 0.8),
            "wellbeing": (0.3, 0.6)
        },
        "professors": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.6),
            "wellbeing": (0.5, 0.7)
        },
        "staff": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.3, 0.5),
            "wellbeing": (0.5, 0.7)
        },
        "retail_workers": {
            "anxiety": (0.4, 0.6),
            "depression": (0.3, 0.5),
            "stress": (0.5, 0.7),
            "wellbeing": (0.4, 0.6)
        },
        "unemployed": {
            "anxiety": (0.5, 0.8),
            "depression": (0.4, 0.7),
            "stress": (0.6, 0.9),
            "wellbeing": (0.2, 0.5)
        }
    },
    community_cohesion=0.6,
    economic_stress_level=0.5,
    unemployment_rate=0.05,
    mental_health_stigma=0.4,
    help_seeking_culture=0.6
)

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
db = Database("test_quick.db")
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
print(f"   Avg Anxiety: {summary['mental_health']['avg_anxiety']:.2f}")
print(f"   Avg Depression: {summary['mental_health']['avg_depression']:.2f}")
print(f"   Avg Stress: {summary['mental_health']['avg_stress']:.2f}")
print(f"   Avg Wellbeing: {summary['mental_health']['avg_wellbeing']:.2f}")
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
    print(f"   Avg Anxiety: {summary['mental_health']['avg_anxiety']:.2f}")
    print(f"   Avg Depression: {summary['mental_health']['avg_depression']:.2f}")
    print(f"   Avg Stress: {summary['mental_health']['avg_stress']:.2f}")
    print(f"   Avg Wellbeing: {summary['mental_health']['avg_wellbeing']:.2f}")
    print()
    
    print("✅ Test simulation complete!")
    print(f"📁 Database: test_quick.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
