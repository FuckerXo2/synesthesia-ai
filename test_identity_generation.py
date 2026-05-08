#!/usr/bin/env python3
"""
Test Identity Generation - LLM creates unique backstories for agents
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.agent.agent import Agent
from synesthesia.llm.identity_generator import IdentityGenerator
from synesthesia.agent.identity import Memory
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
from datetime import datetime

print("="*60)
print("🎭 SYNESTHESIA - IDENTITY GENERATION TEST")
print("="*60)
print()

# Generate a small population
population = 10

print(f"👤 Generating {population} agents...")
config = SocietyConfig(
    society_description="Tech startup city",
    total_population=population,
    demographics={
        "engineer": 40,
        "designer": 20,
        "product_manager": 20,
        "support_staff": 20
    },
    age_ranges={
        "engineer": (24, 35),
        "designer": (23, 32),
        "product_manager": (28, 40),
        "support_staff": (22, 50)
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
        },
        "support_staff": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.6),
            "wellbeing": (0.5, 0.7)
        }
    }
)

pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
agents = [Agent.from_dict(a.to_dict()) for a in agents_data]
print(f"✅ Generated {len(agents)} agents!")
print()

# Generate identities
print("🎭 Generating unique identities...")
identity_gen = IdentityGenerator()

society_context = """
Tech startup city with burnout culture. Long hours, high stress, 
constant pressure to perform. Fear of layoffs. Imposter syndrome common.
"""

# Generate identities for all agents
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

identities = identity_gen.generate_batch_identities(
    agent_dicts,
    society_context=society_context,
    batch_size=5
)

# Attach identities to agents
for agent in agents:
    agent.identity = identities.get(agent.agent_id)

print()

# Show detailed profiles for 3 agents
print("="*60)
print("👤 DETAILED AGENT PROFILES")
print("="*60)

for i, agent in enumerate(agents[:3]):
    print(f"\n{'='*60}")
    print(f"AGENT #{agent.agent_id}: {agent.name}")
    print(f"{'='*60}")
    print(f"Age: {agent.age}")
    print(f"Role: {agent.role}")
    print(f"Personality: {', '.join(agent.personality_traits)}")
    print()
    
    print(f"Mental Health:")
    print(f"  Anxiety: {agent.mental_health.anxiety:.2f}")
    print(f"  Depression: {agent.mental_health.depression:.2f}")
    print(f"  Stress: {agent.mental_health.stress:.2f}")
    print(f"  Wellbeing: {agent.mental_health.wellbeing:.2f}")
    print(f"  State: {agent.mental_health.category.value}")
    print()
    
    if agent.identity:
        print(f"IDENTITY:")
        print(f"  Backstory: {agent.identity.backstory}")
        print()
        print(f"  Values: {', '.join(agent.identity.values)}")
        print(f"  Fears: {', '.join(agent.identity.fears)}")
        print(f"  Goals: {', '.join(agent.identity.goals)}")
        print(f"  Coping: {', '.join(agent.identity.coping_mechanisms)}")
        print(f"  Quirks: {', '.join(agent.identity.quirks)}")
    else:
        print("  (No identity generated)")

print()
print("="*60)

# Test memory system
print("\n🧠 TESTING MEMORY SYSTEM")
print("="*60)

test_agent = agents[0]
print(f"\nAgent: {test_agent.name}")
print()

# Add some memories
print("Adding memories...")

memory1 = Memory(
    event_type="work_event",
    description="Failed product launch - devastating",
    timestamp=datetime.now(),
    emotional_impact=-0.8,
    emotional_tags=["stressful", "embarrassing", "failure"],
    people_involved=[2, 3],  # Boss and coworker
    mental_health_change={"anxiety": 0.3, "stress": 0.4, "wellbeing": -0.2},
    relationship_changes={2: -0.2, 3: -0.1},
    location="Office"
)

memory2 = Memory(
    event_type="conversation",
    description="Coffee with friend Emma - she listened to me vent",
    timestamp=datetime.now(),
    emotional_impact=0.5,
    emotional_tags=["comforting", "supportive", "grateful"],
    people_involved=[5],  # Friend
    mental_health_change={"anxiety": -0.1, "wellbeing": 0.1},
    relationship_changes={5: 0.1},
    location="Cafe",
    conversation_snippet="Emma: 'You're not a failure. One bad launch doesn't define you.'"
)

memory3 = Memory(
    event_type="crisis",
    description="Panic attack at desk - had to leave early",
    timestamp=datetime.now(),
    emotional_impact=-0.9,
    emotional_tags=["terrifying", "overwhelming", "helpless"],
    people_involved=[],
    mental_health_change={"anxiety": 0.5, "depression": 0.3, "wellbeing": -0.3},
    location="Office"
)

test_agent.remember(memory1)
test_agent.remember(memory2)
test_agent.remember(memory3)

print(f"✅ Added 3 memories")
print()

# Show memory summary
print("Memory Summary:")
print(f"  Total memories: {len(test_agent.memory.memories)}")
print(f"  Traumatic memories: {len(test_agent.memory.trauma)}")
print(f"  Positive memories: {len(test_agent.memory.positive_memories)}")
print(f"  Resilience score: {test_agent.memory.get_resilience_score():.2f}")
print()

print("Recent Memories:")
for i, mem in enumerate(test_agent.memory.get_recent_memories(3), 1):
    impact = "devastating" if mem.emotional_impact < -0.5 else \
             "negative" if mem.emotional_impact < 0 else \
             "neutral" if mem.emotional_impact < 0.3 else \
             "positive" if mem.emotional_impact < 0.7 else \
             "amazing"
    print(f"  {i}. {mem.description} ({impact})")

print()

# Show full context for LLM
print("="*60)
print("📝 FULL CONTEXT FOR LLM")
print("="*60)
print()
print(test_agent.get_context())

print()
print("="*60)
print("✅ Identity Generation Test Complete!")
print("="*60)
print()
print("📊 Summary:")
print(f"   • Generated {len(agents)} unique identities")
print(f"   • Each agent has backstory, values, fears, goals")
print(f"   • Memory system tracks events and emotional impact")
print(f"   • Agents now feel like REAL PEOPLE")
print()
print("🎯 Next: Build conversation system using these identities!")
print("="*60)
