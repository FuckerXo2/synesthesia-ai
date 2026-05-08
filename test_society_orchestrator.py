#!/usr/bin/env python3
"""
Test Society Orchestrator - LLM generates society structure on the fly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.world.society_orchestrator import SocietyOrchestrator
from datetime import datetime, timedelta
import json

print("="*60)
print("🧠 SYNESTHESIA - SOCIETY ORCHESTRATOR TEST")
print("="*60)
print()

# Initialize orchestrator
orchestrator = SocietyOrchestrator()

# Test 1: Tech Startup City
print("TEST 1: Tech Startup City")
print("-"*60)

structure1 = orchestrator.generate_society_structure(
    user_description="Tech startup city with burnout culture, long hours, high stress",
    population=5000,
    additional_context="Focus on mental health impacts of startup culture"
)

print("\n" + orchestrator.get_society_summary())

# Save structure
with open("society_structure_tech_startup.json", "w") as f:
    json.dump(structure1, f, indent=2)
print("💾 Saved to: society_structure_tech_startup.json")

print("\n" + "="*60)
print()

# Test 2: Medieval Village
print("TEST 2: Medieval Village")
print("-"*60)

structure2 = orchestrator.generate_society_structure(
    user_description="Medieval village during harsh winter, food scarcity, disease spreading",
    population=500,
    additional_context="Focus on survival stress and community bonds"
)

print("\n" + orchestrator.get_society_summary())

# Save structure
with open("society_structure_medieval.json", "w") as f:
    json.dump(structure2, f, indent=2)
print("💾 Saved to: society_structure_medieval.json")

print("\n" + "="*60)
print()

# Test 3: Event Orchestration
print("TEST 3: Event Orchestration (Tech Startup)")
print("-"*60)

# Simulate different times and states
test_scenarios = [
    {
        "time": datetime(2026, 5, 5, 10, 0),  # Monday 10am
        "state": {
            "avg_stress": 0.6,
            "avg_anxiety": 0.5,
            "avg_depression": 0.3,
            "avg_wellbeing": 0.5,
            "crisis_count": 2
        },
        "recent": ["Product launch yesterday", "Team worked late"]
    },
    {
        "time": datetime(2026, 5, 5, 18, 0),  # Monday 6pm
        "state": {
            "avg_stress": 0.8,
            "avg_anxiety": 0.7,
            "avg_depression": 0.4,
            "avg_wellbeing": 0.3,
            "crisis_count": 5
        },
        "recent": ["Product launch yesterday", "Team worked late", "CEO announced layoffs"]
    },
    {
        "time": datetime(2026, 5, 9, 16, 0),  # Friday 4pm
        "state": {
            "avg_stress": 0.5,
            "avg_anxiety": 0.4,
            "avg_depression": 0.3,
            "avg_wellbeing": 0.6,
            "crisis_count": 1
        },
        "recent": ["Week went well", "Demo day success"]
    }
]

# Use tech startup structure
orchestrator.society_structure = structure1

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\nScenario {i}: {scenario['time'].strftime('%A %I:%M %p')}")
    print(f"Population state: Stress={scenario['state']['avg_stress']:.2f}, "
          f"Crisis={scenario['state']['crisis_count']}")
    
    events = orchestrator.orchestrate_events(
        scenario['time'],
        scenario['state'],
        scenario['recent']
    )
    
    if events:
        print(f"📅 Generated {len(events)} events:")
        for event in events:
            print(f"   • [{event['type']}] {event['name']}")
            print(f"     {event.get('description', '')}")
            if 'mental_health_impact' in event:
                impacts = event['mental_health_impact']
                if impacts:
                    print(f"     Impact: {impacts}")
    else:
        print("   (no events this time)")

print("\n" + "="*60)
print()

# Test 4: Space Station (Creative Test)
print("TEST 4: Space Station (Creative Test)")
print("-"*60)

structure3 = orchestrator.generate_society_structure(
    user_description="Space station orbiting Mars, 1000 people, oxygen shortage crisis, isolation stress",
    population=1000,
    additional_context="Focus on isolation, confined spaces, and life-or-death stress"
)

print("\n" + orchestrator.get_society_summary())

# Save structure
with open("society_structure_space_station.json", "w") as f:
    json.dump(structure3, f, indent=2)
print("💾 Saved to: society_structure_space_station.json")

print("\n" + "="*60)
print("✅ Society Orchestrator Test Complete!")
print("="*60)
print()
print("📊 Summary:")
print("   • Generated 3 different society structures")
print("   • Tech startup: realistic startup culture")
print("   • Medieval village: survival stress")
print("   • Space station: sci-fi scenario")
print("   • Event orchestration working")
print("   • LLM creates everything on the fly!")
print()
print("🎯 Next: Integrate into real-time simulation")
print("="*60)
