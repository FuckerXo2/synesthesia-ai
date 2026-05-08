#!/usr/bin/env python3
"""
Synesthesia Simulation Runner
Quick start script to run a mental health population simulation
"""

import sys
import os

# Add synesthesia to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.engine import SimulationEngine
from synesthesia_population_generator import SocietyGenerator, PopulationGenerator


def main():
    print("="*60)
    print("🧠 SYNESTHESIA - Mental Health Population Simulator")
    print("="*60)
    print()
    
    # Configuration
    description = input("Describe the society (or press Enter for default): ").strip()
    if not description:
        description = "Small college town with 1000 people, high academic pressure, diverse student body"
    
    population_input = input("Population size (default 1000): ").strip()
    population = int(population_input) if population_input else 1000
    
    hours_input = input("Simulation hours (default 72): ").strip()
    total_hours = int(hours_input) if hours_input else 72
    
    print()
    print(f"📝 Society: {description}")
    print(f"👥 Population: {population:,}")
    print(f"⏱️  Duration: {total_hours} hours")
    print()
    
    # Step 1: Generate society configuration
    print("🤖 Generating society configuration...")
    society_gen = SocietyGenerator()
    
    try:
        config = society_gen.generate_society_config(description, population)
        print("✅ Society configuration generated!")
        print()
        print("📊 Demographics:")
        for role, pct in config.demographics.items():
            count = int(population * (pct / 100))
            print(f"   {role}: {pct}% ({count:,} people)")
        print()
    except Exception as e:
        print(f"⚠️  LLM generation failed: {e}")
        print("Using default configuration...")
        config = society_gen._get_default_config(description, population)
    
    # Step 2: Generate individual agents
    print("👤 Generating individual agent profiles...")
    pop_gen = PopulationGenerator()
    agents_data = pop_gen.generate_population(config)
    print(f"✅ Generated {len(agents_data):,} agent profiles!")
    print()
    
    # Step 3: Initialize database
    print("💾 Initializing database...")
    db = Database("synesthesia_simulation.db")
    print("✅ Database ready!")
    print()
    
    # Step 4: Create Agent objects and insert into database
    print("📥 Loading agents into database...")
    from synesthesia.agent.agent import Agent
    
    agents = []
    for agent_data in agents_data:
        # Create Agent object
        agent = Agent.from_dict(agent_data.to_dict())
        agents.append(agent)
    
    # Batch insert for performance
    db.batch_insert_agents([a.to_dict() for a in agents])
    print(f"✅ Loaded {len(agents):,} agents into database!")
    print()
    
    # Step 5: Create and run simulation
    print("🌍 Initializing simulation engine...")
    engine = SimulationEngine(
        agents=agents,
        db=db,
        total_hours=total_hours,
        minutes_per_round=60,  # 1 hour per round
        use_llm=False,  # Start with rule-based for speed
        max_workers=10
    )
    print()
    
    # Show initial state
    summary = engine.get_simulation_summary()
    print("📊 Initial Population State:")
    print(f"   Total: {summary['population']['total']:,}")
    print(f"   In Crisis: {summary['population']['in_crisis']} ({summary['population']['crisis_rate']*100:.1f}%)")
    print(f"   Thriving: {summary['population']['thriving']} ({summary['population']['thriving_rate']*100:.1f}%)")
    print(f"   Avg Anxiety: {summary['mental_health']['avg_anxiety']:.2f}")
    print(f"   Avg Depression: {summary['mental_health']['avg_depression']:.2f}")
    print(f"   Avg Stress: {summary['mental_health']['avg_stress']:.2f}")
    print(f"   Avg Wellbeing: {summary['mental_health']['avg_wellbeing']:.2f}")
    print()
    
    input("Press Enter to start simulation...")
    print()
    
    # Run simulation
    try:
        engine.run()
        
        # Show final state
        print("\n📊 Final Population State:")
        summary = engine.get_simulation_summary()
        print(f"   Total: {summary['population']['total']:,}")
        print(f"   In Crisis: {summary['population']['in_crisis']} ({summary['population']['crisis_rate']*100:.1f}%)")
        print(f"   Thriving: {summary['population']['thriving']} ({summary['population']['thriving_rate']*100:.1f}%)")
        print(f"   Avg Anxiety: {summary['mental_health']['avg_anxiety']:.2f}")
        print(f"   Avg Depression: {summary['mental_health']['avg_depression']:.2f}")
        print(f"   Avg Stress: {summary['mental_health']['avg_stress']:.2f}")
        print(f"   Avg Wellbeing: {summary['mental_health']['avg_wellbeing']:.2f}")
        print()
        
        # Show agents in crisis
        crisis_agents = engine.get_agents_in_crisis()
        if crisis_agents:
            print(f"⚠️  {len(crisis_agents)} agents in crisis:")
            for agent in crisis_agents[:10]:  # Show first 10
                print(f"   - {agent.name} ({agent.role}): "
                      f"Anxiety={agent.mental_health.anxiety:.2f}, "
                      f"Depression={agent.mental_health.depression:.2f}")
            if len(crisis_agents) > 10:
                print(f"   ... and {len(crisis_agents) - 10} more")
        
    except KeyboardInterrupt:
        print("\n⚠️  Simulation interrupted")
    finally:
        db.close()
        print("\n✅ Database closed")
    
    print()
    print("="*60)
    print("🎉 Simulation complete!")
    print(f"📁 Data saved to: synesthesia_simulation.db")
    print("="*60)


if __name__ == "__main__":
    main()
