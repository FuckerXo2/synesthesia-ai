#!/usr/bin/env python3
"""
Test the LLM-powered agent brain
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.llm.agent_brain import AgentBrain
from synesthesia.actions.types import ActionType

print("="*60)
print("🧠 TESTING LLM AGENT BRAIN")
print("="*60)
print()

# Initialize the brain
brain = AgentBrain()

# Test 1: Decision making for a stressed student
print("Test 1: Stressed Student Decision")
print("-" * 40)

student_context = {
    "name": "Alex",
    "age": 20,
    "role": "student",
    "personality_traits": ["introverted", "perfectionist", "anxious"],
    "mental_health": {
        "anxiety": 0.8,
        "depression": 0.4,
        "stress": 0.9,
        "wellbeing": 0.3,
        "category": "struggling"
    }
}

available_actions = [
    ActionType.STUDY,
    ActionType.EXERCISE,
    ActionType.CALL_FRIEND,
    ActionType.ISOLATE,
    ActionType.SEEK_THERAPY,
    ActionType.SCROLL_SOCIAL_MEDIA
]

recent_events = [
    "failed an exam",
    "skipped class due to anxiety",
    "isolated themselves"
]

print(f"Agent: {student_context['name']}, {student_context['age']}, {student_context['role']}")
print(f"Personality: {', '.join(student_context['personality_traits'])}")
print(f"Mental State: {student_context['mental_health']['category']}")
print(f"Anxiety: {student_context['mental_health']['anxiety']:.2f}")
print(f"Recent: {', '.join(recent_events)}")
print()

action = brain.decide_action(student_context, available_actions, 14, recent_events)
print(f"✅ Decision: {action.value}")
print()

# Test 2: Decision making for a thriving professional
print("Test 2: Thriving Professional Decision")
print("-" * 40)

professional_context = {
    "name": "Jordan",
    "age": 35,
    "role": "tech_worker",
    "personality_traits": ["extroverted", "optimistic", "confident"],
    "mental_health": {
        "anxiety": 0.2,
        "depression": 0.1,
        "stress": 0.3,
        "wellbeing": 0.9,
        "category": "thriving"
    }
}

recent_events = [
    "completed a successful project",
    "received praise from manager",
    "had lunch with colleagues"
]

print(f"Agent: {professional_context['name']}, {professional_context['age']}, {professional_context['role']}")
print(f"Personality: {', '.join(professional_context['personality_traits'])}")
print(f"Mental State: {professional_context['mental_health']['category']}")
print(f"Wellbeing: {professional_context['mental_health']['wellbeing']:.2f}")
print(f"Recent: {', '.join(recent_events)}")
print()

action = brain.decide_action(professional_context, available_actions, 18, recent_events)
print(f"✅ Decision: {action.value}")
print()

# Test 3: Generate a conversation
print("Test 3: Generate Conversation")
print("-" * 40)

agent1 = {
    "name": "Alex",
    "age": 20,
    "role": "student",
    "personality_traits": ["introverted", "perfectionist", "anxious"],
    "mental_health": {
        "anxiety": 0.8,
        "depression": 0.4,
        "stress": 0.9,
        "wellbeing": 0.3,
        "category": "struggling"
    }
}

agent2 = {
    "name": "Sam",
    "age": 21,
    "role": "student",
    "personality_traits": ["extroverted", "empathetic", "optimistic"],
    "mental_health": {
        "anxiety": 0.3,
        "depression": 0.2,
        "stress": 0.4,
        "wellbeing": 0.7,
        "category": "coping"
    }
}

print(f"{agent1['name']} (struggling) meets {agent2['name']} (coping)")
print()

conversation = brain.generate_conversation(agent1, agent2, "friend")

print("Conversation:")
for exchange in conversation['conversation']:
    print(f"  {exchange['speaker']}: {exchange['text']}")
print()

print(f"Summary: {conversation['summary']}")
print()

print(f"Impact on {agent1['name']}:")
for key, value in conversation['impact_agent1'].items():
    print(f"  {key}: {value:+.3f}")
print()

print(f"Impact on {agent2['name']}:")
for key, value in conversation['impact_agent2'].items():
    print(f"  {key}: {value:+.3f}")
print()

print(f"Relationship change: {conversation['relationship_change']:+.3f}")
print()

# Test 4: Internal monologue
print("Test 4: Internal Monologue")
print("-" * 40)

print(f"{agent1['name']}'s thoughts:")
monologue = brain.generate_internal_monologue(agent1, recent_events)
print(f'  "{monologue}"')
print()

print("="*60)
print("✅ All tests complete!")
print("="*60)
