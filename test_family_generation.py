#!/usr/bin/env python3
"""
Test Family and Relationship Generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synesthesia.agent.agent import Agent
from synesthesia.world.family_generator import FamilyGenerator
from synesthesia_population_generator import SocietyConfig, PopulationGenerator
import random

print("="*60)
print("👨‍👩‍👧‍👦 SYNESTHESIA - FAMILY GENERATION TEST")
print("="*60)
print()

# Generate a population
population = 100

print(f"👥 Generating {population} agents...")
config = SocietyConfig(
    society_description="Suburban community",
    total_population=population,
    demographics={
        "parents": 30,
        "children": 25,
        "young_adults": 20,
        "workers": 15,
        "retirees": 10
    },
    age_ranges={
        "parents": (30, 50),
        "children": (5, 17),
        "young_adults": (18, 25),
        "workers": (26, 60),
        "retirees": (61, 80)
    },
    stressors=["work_stress", "family_stress", "financial_stress"],
    mental_health_baselines={
        "parents": {
            "anxiety": (0.4, 0.6),
            "depression": (0.2, 0.4),
            "stress": (0.5, 0.7),
            "wellbeing": (0.4, 0.6)
        },
        "children": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.3, 0.5),
            "wellbeing": (0.5, 0.7)
        },
        "young_adults": {
            "anxiety": (0.4, 0.6),
            "depression": (0.3, 0.5),
            "stress": (0.4, 0.6),
            "wellbeing": (0.4, 0.6)
        },
        "workers": {
            "anxiety": (0.3, 0.5),
            "depression": (0.2, 0.4),
            "stress": (0.4, 0.6),
            "wellbeing": (0.5, 0.7)
        },
        "retirees": {
            "anxiety": (0.2, 0.4),
            "depression": (0.3, 0.5),
            "stress": (0.2, 0.4),
            "wellbeing": (0.5, 0.7)
        }
    }
)

pop_gen = PopulationGenerator()
agents_data = pop_gen.generate_population(config)
agents = [Agent.from_dict(a.to_dict()) for a in agents_data]
print(f"✅ Generated {len(agents)} agents!")
print()

# Show age distribution
age_groups = {}
for agent in agents:
    age_group = f"{(agent.age // 10) * 10}-{(agent.age // 10) * 10 + 9}"
    age_groups[age_group] = age_groups.get(age_group, 0) + 1

print("📊 Age Distribution:")
for age_group in sorted(age_groups.keys()):
    count = age_groups[age_group]
    bar = "█" * (count // 2)
    print(f"   {age_group}: {count:3d} {bar}")
print()

# Generate families
family_gen = FamilyGenerator(agents)
families = family_gen.generate_families()
print()

# Show some example families
print("👨‍👩‍👧‍👦 Example Families:")
for i, family in enumerate(families[:5]):
    print(f"\n   Family {family.family_id}:")
    
    # Parents
    for parent_id in family.parents:
        parent = agents[parent_id - 1]  # Assuming agent_id starts at 1
        print(f"      👤 {parent.name} (age {parent.age}, {parent.role})")
    
    # Children
    if family.children:
        for child_id in family.children:
            child = agents[child_id - 1]
            print(f"         👶 {child.name} (age {child.age})")
    else:
        print(f"         (no children)")

print()

# Generate coworker relationships
print("💼 Generating coworker relationships...")
workplaces = list(range(1, 11))  # 10 workplaces
workplace_assignments = family_gen.assign_coworkers(workplaces)
print()

# Show workplace distribution
print("🏢 Workplace Distribution:")
for workplace_id, worker_ids in sorted(workplace_assignments.items())[:5]:
    print(f"   Workplace {workplace_id}: {len(worker_ids)} workers")
print()

# Generate friend networks
print("👥 Generating friend networks...")
friendships = family_gen.generate_friend_networks(avg_friends=3)
print()

# Generate neighbor relationships
print("🏘️  Generating neighbor relationships...")
homes = list(range(1, 31))  # 30 homes
home_assignments = {}
for family in families:
    home_id = homes[family.family_id % len(homes)]
    home_assignments[home_id] = family.all_members()

family_gen.generate_neighbor_relationships(homes, home_assignments)
print()

# Get relationship statistics
print("📊 Relationship Statistics:")
stats = family_gen.get_relationship_stats()
print(f"   Total relationships: {stats['total_relationships']:,}")
print(f"   Avg per agent: {stats['avg_relationships_per_agent']:.1f}")
print(f"   Family: {stats['family_relationships']}")
print(f"   Friends: {stats['friend_relationships']}")
print(f"   Coworkers: {stats['coworker_relationships']}")
print(f"   Neighbors: {stats['neighbor_relationships']}")
print()

# Show example agent with all relationships
print("👤 Example Agent with Relationships:")
example_agent = agents[0]
print(f"\n   {example_agent.name} (age {example_agent.age}, {example_agent.role})")
print(f"   Mental Health: Anxiety={example_agent.mental_health.anxiety:.2f}, "
      f"Depression={example_agent.mental_health.depression:.2f}")
print()

# Show relationships
rel_manager = example_agent.relationships
if rel_manager.relationships:
    print(f"   Relationships ({len(rel_manager.relationships)}):")
    
    # Family
    family_rels = rel_manager.get_family()
    if family_rels:
        print(f"\n      Family ({len(family_rels)}):")
        for rel in family_rels:
            other_agent = agents[rel.agent_id - 1]
            print(f"         {rel.relationship_type.value}: {other_agent.name} "
                  f"(strength={rel.strength:.2f}, trust={rel.trust:.2f})")
    
    # Friends
    friend_rels = rel_manager.get_friends()
    if friend_rels:
        print(f"\n      Friends ({len(friend_rels)}):")
        for rel in friend_rels[:3]:  # Show first 3
            other_agent = agents[rel.agent_id - 1]
            print(f"         {rel.relationship_type.value}: {other_agent.name} "
                  f"(strength={rel.strength:.2f})")
    
    # Coworkers
    coworker_rels = rel_manager.get_coworkers()
    if coworker_rels:
        print(f"\n      Coworkers ({len(coworker_rels)}):")
        for rel in coworker_rels[:3]:  # Show first 3
            other_agent = agents[rel.agent_id - 1]
            print(f"         {rel.relationship_type.value}: {other_agent.name} "
                  f"(strength={rel.strength:.2f})")
    
    # Neighbors
    from synesthesia.agent.relationships import RelationshipType
    neighbor_rels = rel_manager.get_relationships_by_type(
        RelationshipType.NEIGHBOR
    )
    if neighbor_rels:
        print(f"\n      Neighbors ({len(neighbor_rels)}):")
        for rel in neighbor_rels[:3]:  # Show first 3
            other_agent = agents[rel.agent_id - 1]
            print(f"         neighbor: {other_agent.name} "
                  f"(strength={rel.strength:.2f})")
else:
    print("   (no relationships)")

print()
print("="*60)
print("✅ Family generation test complete!")
print("="*60)
