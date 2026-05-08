#!/usr/bin/env python3
"""
Quick Conversation Simulation Test - Minimal agents, focus on conversations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.database.models import Database
from synesthesia.simulation.realtime_engine import RealtimeSimulationEngine
from synesthesia.world.location import World, LocationType
from synesthesia.agent.agent import Agent
from synesthesia.agent.state import MentalHealthState
from synesthesia.agent.relationships import RelationshipType
from synesthesia.agent.identity import AgentIdentity, MemoryManager
from synesthesia.llm.agent_brain import AgentBrain
from datetime import datetime
import random

print("="*60)
print("🗣️  QUICK CONVERSATION SIMULATION TEST")
print("="*60)
print()

# Create 5 agents manually (skip LLM generation for speed)
print("👤 Creating 5 agents...")

agents = []

# Agent 1: Sarah (stressed engineer)
agent1 = Agent(
    agent_id=1,
    name="Sarah Chen",
    age=28,
    role="engineer",
    personality_traits=["introverted", "perfectionist"],
    mental_health=MentalHealthState(anxiety=0.7, depression=0.4, stress=0.8, wellbeing=0.3)
)
agent1.identity = AgentIdentity(
    agent_id=1,
    backstory="Immigrant parents sacrificed everything. Feels pressure to succeed. Imposter syndrome.",
    values=["family", "achievement"],
    fears=["failure", "disappointing_parents"],
    goals=["get_promoted", "make_parents_proud"],
    coping_mechanisms=["overwork", "isolate"],
    quirks=["always_early", "too_much_coffee"]
)
agents.append(agent1)

# Agent 2: Mike (supportive friend)
agent2 = Agent(
    agent_id=2,
    name="Mike Johnson",
    age=30,
    role="engineer",
    personality_traits=["empathetic", "laid_back"],
    mental_health=MentalHealthState(anxiety=0.4, depression=0.3, stress=0.5, wellbeing=0.6)
)
agent2.identity = AgentIdentity(
    agent_id=2,
    backstory="Grew up in supportive family. Learned to help others. Good listener.",
    values=["friendship", "balance"],
    fears=["letting_friends_down"],
    goals=["help_others", "find_meaning"],
    coping_mechanisms=["talk_to_friends", "exercise"],
    quirks=["always_smiling", "brings_snacks"]
)
agents.append(agent2)

# Agent 3: Emma (designer, anxious)
agent3 = Agent(
    agent_id=3,
    name="Emma Davis",
    age=26,
    role="designer",
    personality_traits=["creative", "anxious"],
    mental_health=MentalHealthState(anxiety=0.6, depression=0.4, stress=0.6, wellbeing=0.4)
)
agent3.identity = AgentIdentity(
    agent_id=3,
    backstory="Art school debt. Pressure to prove creative work is valuable. Self-doubt.",
    values=["creativity", "authenticity"],
    fears=["being_mediocre", "financial_instability"],
    goals=["create_meaningful_work", "pay_off_debt"],
    coping_mechanisms=["art", "music"],
    quirks=["doodles_constantly", "wears_headphones"]
)
agents.append(agent3)

# Agent 4: Alex (PM, burned out)
agent4 = Agent(
    agent_id=4,
    name="Alex Rodriguez",
    age=35,
    role="product_manager",
    personality_traits=["organized", "stressed"],
    mental_health=MentalHealthState(anxiety=0.8, depression=0.5, stress=0.9, wellbeing=0.2)
)
agent4.identity = AgentIdentity(
    agent_id=4,
    backstory="Climbed corporate ladder. Now questioning if it was worth it. Burnout.",
    values=["success", "control"],
    fears=["losing_control", "being_replaced"],
    goals=["survive", "find_exit_strategy"],
    coping_mechanisms=["work_harder", "avoid_feelings"],
    quirks=["checks_phone_constantly", "never_takes_breaks"]
)
agents.append(agent4)

# Agent 5: Jordan (junior, eager)
agent5 = Agent(
    agent_id=5,
    name="Jordan Lee",
    age=23,
    role="engineer",
    personality_traits=["enthusiastic", "naive"],
    mental_health=MentalHealthState(anxiety=0.5, depression=0.2, stress=0.4, wellbeing=0.7)
)
agent5.identity = AgentIdentity(
    agent_id=5,
    backstory="Fresh grad. Excited about tech. Hasn't experienced burnout yet.",
    values=["learning", "innovation"],
    fears=["not_being_good_enough"],
    goals=["learn_everything", "make_impact"],
    coping_mechanisms=["ask_questions", "stay_positive"],
    quirks=["takes_notes_on_everything", "asks_lots_of_questions"]
)
agents.append(agent5)

print(f"✅ Created {len(agents)} agents!")
print()

# Create relationships
print("🤝 Creating relationships...")
# Sarah and Mike are friends
agents[0].relationships.add_relationship(2, RelationshipType.FRIEND, strength=0.7)
agents[1].relationships.add_relationship(1, RelationshipType.FRIEND, strength=0.7)

# Emma and Sarah are coworkers
agents[0].relationships.add_relationship(3, RelationshipType.COWORKER, strength=0.5)
agents[2].relationships.add_relationship(1, RelationshipType.COWORKER, strength=0.5)

# Alex is everyone's boss
for i in range(4):
    agents[i].relationships.add_relationship(4, RelationshipType.BOSS, strength=0.4)
    agents[4].relationships.add_relationship(i+1, RelationshipType.EMPLOYEE, strength=0.4)

print("✅ Relationships created!")
print()

# Create world
print("🌍 Creating world...")
world = World()

office = world.create_location("Office", LocationType.WORKPLACE, 50, 50, 50)
cafe = world.create_location("Coffee Shop", LocationType.RESTAURANT, 60, 60, 20)
park = world.create_location("Park", LocationType.PARK, 70, 70, 30)

print(f"✅ Created {len(world.locations)} locations")
print()

# Initialize LLM
print("🧠 Initializing LLM...")
llm_brain = AgentBrain(use_load_balancing=True)
print("✅ LLM ready!")
print()

# Initialize database
db = Database("test_quick_conversations.db")

# Create simulation
print("🎮 Creating simulation...")
engine = RealtimeSimulationEngine(
    agents=agents,
    world=world,
    db=db,
    simulation_id="quick-conv-001",
    time_scale=600.0,
    llm_client=llm_brain
)
print("✅ Engine ready!")
print()

# Place agents at office (so they're near each other)
print("🏢 Placing agents at office...")
for agent in agents:
    engine.move_agent_to_location(agent.agent_id, office.location_id)
print("✅ All agents at office!")
print()

print("="*60)
print("🚀 STARTING SIMULATION")
print("="*60)
print("   5 agents at the office")
print("   They will have conversations!")
print("   Watch for 💬 notifications")
print()
print("   Press Ctrl+C to stop")
print("="*60)
print()

# Run for 1 hour
try:
    engine.run(target_fps=5.0, duration_hours=1.0)
    
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    
    print(f"\n💬 Conversations: {len(engine.last_conversation_time)}")
    
    print(f"\n🧠 Agent Memories:")
    for agent in agents:
        if agent.memory and agent.memory.memories:
            print(f"\n   {agent.name}:")
            for mem in agent.memory.get_recent_memories(2):
                print(f"      • {mem.description}")
    
    print("\n✅ Test complete!")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n⚠️  Interrupted")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
