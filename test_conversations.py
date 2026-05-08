#!/usr/bin/env python3
"""
Test Conversation System - Agents having real conversations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.agent.agent import Agent
from synesthesia.agent.relationships import RelationshipType
from synesthesia.llm.identity_generator import IdentityGenerator
from synesthesia.llm.conversation_generator import ConversationGenerator
from synesthesia.agent.identity import Memory
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
from datetime import datetime

print("="*60)
print("🗣️  SYNESTHESIA - CONVERSATION SYSTEM TEST")
print("="*60)
print()

# Generate a small population
population = 5

print(f"👤 Generating {population} agents...")
config = SocietyConfig(
    society_description="Tech startup",
    total_population=population,
    demographics={
        "engineer": 60,
        "designer": 40
    },
    age_ranges={
        "engineer": (24, 35),
        "designer": (23, 32)
    },
    stressors=["work_stress", "burnout"],
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
        }
    }
)

pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
agents = [Agent.from_dict(a.to_dict()) for a in agents_data]
print(f"✅ Generated {len(agents)} agents!")
print()

# Generate identities
print("🎭 Generating identities...")
identity_gen = IdentityGenerator()

society_context = "Tech startup with burnout culture"

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

identities = identity_gen.generate_batch_identities(agent_dicts, society_context, batch_size=5)

for agent in agents:
    agent.identity = identities.get(agent.agent_id)

print()

# Create some relationships
print("🤝 Creating relationships...")
# Make agent 0 and 1 friends
agents[0].relationships.add_relationship(
    agents[1].agent_id,
    RelationshipType.FRIEND,
    strength=0.7
)
agents[1].relationships.add_relationship(
    agents[0].agent_id,
    RelationshipType.FRIEND,
    strength=0.7
)

# Make agent 2 and 3 coworkers
agents[2].relationships.add_relationship(
    agents[3].agent_id,
    RelationshipType.COWORKER,
    strength=0.5
)
agents[3].relationships.add_relationship(
    agents[2].agent_id,
    RelationshipType.COWORKER,
    strength=0.5
)

print("✅ Relationships created!")
print()

# Add some memories to make conversations richer
print("🧠 Adding some memories...")

# Agent 0 had a bad day
memory = Memory(
    event_type="work_event",
    description="Failed product launch - devastating",
    timestamp=datetime.now(),
    emotional_impact=-0.8,
    emotional_tags=["stressful", "embarrassing"],
    people_involved=[],
    mental_health_change={"anxiety": 0.3, "stress": 0.4},
    location="Office"
)
agents[0].remember(memory)

# Agent 2 is stressed about deadline
memory = Memory(
    event_type="work_event",
    description="Impossible deadline announced - feeling overwhelmed",
    timestamp=datetime.now(),
    emotional_impact=-0.6,
    emotional_tags=["stressful", "anxious"],
    people_involved=[3],  # Coworker
    mental_health_change={"anxiety": 0.2, "stress": 0.3},
    location="Office"
)
agents[2].remember(memory)

print("✅ Memories added!")
print()

# Initialize conversation generator
print("🗣️  Initializing conversation generator...")
conv_gen = ConversationGenerator()
print("✅ Ready!")
print()

# Test 1: Friends talking (one had a bad day)
print("="*60)
print("TEST 1: Friends Conversation")
print("="*60)
print()

agent1 = agents[0]
agent2 = agents[1]

print(f"👤 {agent1.name} (age {agent1.age}, {agent1.role})")
print(f"   Mental state: {agent1.mental_health.category.value}")
print(f"   Anxiety: {agent1.mental_health.anxiety:.2f}, Stress: {agent1.mental_health.stress:.2f}")
if agent1.identity:
    print(f"   Backstory: {agent1.identity.backstory[:100]}...")
print()

print(f"👤 {agent2.name} (age {agent2.age}, {agent2.role})")
print(f"   Mental state: {agent2.mental_health.category.value}")
print(f"   Anxiety: {agent2.mental_health.anxiety:.2f}, Stress: {agent2.mental_health.stress:.2f}")
if agent2.identity:
    print(f"   Backstory: {agent2.identity.backstory[:100]}...")
print()

print(f"🤝 Relationship: friends (strength 0.7)")
print(f"📍 Context: Coffee shop, after work")
print()

print("🗣️  Generating conversation...")
conversation = conv_gen.generate_conversation(
    agent1,
    agent2,
    context={
        "location": "Coffee shop",
        "situation": "After work, grabbing coffee",
        "time": "6pm"
    }
)

print()
print("💬 CONVERSATION:")
print("-"*60)
for exchange in conversation['conversation']:
    speaker = exchange['speaker']
    text = exchange['text']
    print(f"{speaker}: \"{text}\"")
    if 'internal_thought' in exchange and exchange['internal_thought']:
        print(f"   💭 ({exchange['internal_thought']})")
    print()

print("-"*60)
print(f"📝 Summary: {conversation['summary']}")
print(f"🎭 Tone: {conversation.get('emotional_tone', 'unknown')}")
print()

print(f"📊 Impact on {agent1.name}:")
impact1 = conversation['impact_agent1']
print(f"   Anxiety: {impact1.get('anxiety_change', 0):+.2f}")
print(f"   Depression: {impact1.get('depression_change', 0):+.2f}")
print(f"   Stress: {impact1.get('stress_change', 0):+.2f}")
print(f"   Wellbeing: {impact1.get('wellbeing_change', 0):+.2f}")
print(f"   Emotional impact: {impact1.get('emotional_impact', 0):.2f}")
print(f"   Why: {impact1.get('why', 'N/A')}")
print()

print(f"📊 Impact on {agent2.name}:")
impact2 = conversation['impact_agent2']
print(f"   Anxiety: {impact2.get('anxiety_change', 0):+.2f}")
print(f"   Depression: {impact2.get('depression_change', 0):+.2f}")
print(f"   Stress: {impact2.get('stress_change', 0):+.2f}")
print(f"   Wellbeing: {impact2.get('wellbeing_change', 0):+.2f}")
print(f"   Emotional impact: {impact2.get('emotional_impact', 0):.2f}")
print(f"   Why: {impact2.get('why', 'N/A')}")
print()

print(f"🤝 Relationship change: {conversation.get('relationship_change', 0):+.2f}")
print(f"   Reason: {conversation.get('relationship_reason', 'N/A')}")
print()

# Apply effects
print("✨ Applying conversation effects...")
conv_gen.apply_conversation_effects(
    agent1,
    agent2,
    conversation,
    location="Coffee shop",
    timestamp=datetime.now()
)

print(f"✅ Effects applied!")
print()

print(f"📊 After conversation:")
print(f"   {agent1.name}: Anxiety {agent1.mental_health.anxiety:.2f}, Stress {agent1.mental_health.stress:.2f}")
print(f"   {agent2.name}: Anxiety {agent2.mental_health.anxiety:.2f}, Stress {agent2.mental_health.stress:.2f}")
print(f"   Relationship strength: {agent1.relationships.get_relationship(agent2.agent_id).strength:.2f}")
print()

# Check memories
print(f"🧠 {agent1.name}'s memories:")
for i, mem in enumerate(agent1.memory.get_recent_memories(2), 1):
    print(f"   {i}. {mem.description}")
print()

# Test 2: Coworkers talking (stressed about deadline)
print("="*60)
print("TEST 2: Coworkers Conversation")
print("="*60)
print()

agent3 = agents[2]
agent4 = agents[3]

print(f"👤 {agent3.name} (stressed about deadline)")
print(f"👤 {agent4.name}")
print(f"🤝 Relationship: coworkers")
print()

print("🗣️  Generating conversation...")
conversation2 = conv_gen.generate_conversation(
    agent3,
    agent4,
    context={
        "location": "Office",
        "situation": "Working late on project",
        "time": "8pm"
    }
)

print()
print("💬 CONVERSATION:")
print("-"*60)
for exchange in conversation2['conversation']:
    print(f"{exchange['speaker']}: \"{exchange['text']}\"")
    print()

print("-"*60)
print(f"📝 Summary: {conversation2['summary']}")
print()

# Apply effects
conv_gen.apply_conversation_effects(agent3, agent4, conversation2, "Office")

print("="*60)
print("✅ CONVERSATION SYSTEM TEST COMPLETE!")
print("="*60)
print()
print("📊 Summary:")
print("   • Generated 2 realistic conversations")
print("   • Used identity + memories + relationships")
print("   • Applied mental health impacts")
print("   • Updated relationships")
print("   • Created memories")
print()
print("🎯 Agents are now having REAL conversations!")
print("="*60)
