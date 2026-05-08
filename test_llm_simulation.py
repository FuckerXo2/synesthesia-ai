#!/usr/bin/env python3
"""
LLM-Powered Simulation Test - Agents think for themselves!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.engine import SimulationEngine
from synesthesia.llm.agent_brain import AgentBrain
from synesthesia_population_generator import SocietyConfig, PopulationGenerator

print("="*60)
print("🧠 SYNESTHESIA - LLM-POWERED SIMULATION")
print("="*60)
print()

# Small test configuration
population = 20  # Start small to test LLM integration
total_hours = 12  # 12 hours starting from 8am

print(f"👥 Population: {population} agents")
print(f"⏱️  Duration: {total_hours} hours")
print(f"🤖 LLM: Qwen 3.5 122B (agents think for themselves!)")
print()

# Create default config
config = SocietyConfig(
    society_description="Small college dorm, high stress",
    total_population=population,
    demographics={
        "students": 80,
        "staff": 20
    },
    age_ranges={
        "students": (18, 22),
        "staff": (25, 50)
    },
    stressors=["academic_pressure", "social_anxiety", "financial_stress"],
    mental_health_baselines={
        "students": {
            "anxiety": (0.4, 0.7),
            "depression": (0.2, 0.5),
            "stress": (0.5, 0.8),
            "wellbeing": (0.3, 0.6)
        },
        "staff": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.3, 0.5),
            "wellbeing": (0.5, 0.7)
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
db = Database("test_llm_simulation.db")
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

# Initialize LLM brain
print("🧠 Initializing LLM brain...")
llm_brain = AgentBrain()
print("✅ LLM brain ready!")
print()

# Create simulation with LLM enabled
print("🌍 Creating LLM-powered simulation engine...")
engine = SimulationEngine(
    agents=agents,
    db=db,
    total_hours=total_hours,
    minutes_per_round=60,
    use_llm=True,  # 🔥 LLM MODE ENABLED!
    llm_client=llm_brain,
    max_workers=2  # Lower workers for LLM calls
)

# Override starting time to 8am (round 8)
engine.current_round = 8
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

print("🚀 Starting LLM-powered simulation...")
print("   (Agents are making their own decisions!)")
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
    
    # Show some agent stories
    print("📖 Agent Stories:")
    print("-" * 60)
    for agent in agents[:3]:
        print(f"\n{agent.name} ({agent.role}, {agent.age})")
        print(f"Personality: {', '.join(agent.personality_traits)}")
        print(f"Mental Health: {agent.mental_health.category.value}")
        print(f"Recent actions:")
        for action in agent.recent_actions[-5:]:
            print(f"  - {action}")
    print()
    
    print("✅ LLM simulation complete!")
    print(f"📁 Database: test_llm_simulation.db")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("="*60)
