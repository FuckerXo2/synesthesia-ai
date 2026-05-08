"""
Family and Relationship Generator - Create realistic families and social networks
"""

import random
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

from synesthesia.agent.agent import Agent
from synesthesia.agent.relationships import (
    RelationshipManager,
    RelationshipType,
    create_family_relationships,
    create_spouse_relationships,
    create_coworker_relationships,
    create_friend_relationships
)


@dataclass
class Family:
    """A family unit"""
    family_id: int
    parents: List[int]  # Agent IDs
    children: List[int]  # Agent IDs
    home_id: int = None  # Location ID of home
    
    def all_members(self) -> List[int]:
        """Get all family member IDs"""
        return self.parents + self.children
    
    def size(self) -> int:
        """Get family size"""
        return len(self.parents) + len(self.children)


class FamilyGenerator:
    """Generate families and social networks"""
    
    def __init__(self, agents: List[Agent]):
        """
        Initialize family generator
        
        Args:
            agents: List of all agents
        """
        self.agents = {agent.agent_id: agent for agent in agents}
        self.relationship_managers = {
            agent.agent_id: agent.relationships
            for agent in agents
        }
    
    def generate_families(self) -> List[Family]:
        """
        Generate family units from agents
        
        Strategy:
        1. Identify potential parents (age 25-60)
        2. Identify potential children (age 0-18)
        3. Create family units with 1-2 parents and 0-4 children
        4. Create parent-child relationships
        5. Create spouse relationships for two-parent families
        6. Create sibling relationships
        """
        print("👨‍👩‍👧‍👦 Generating families...")
        
        # Separate agents by age
        potential_parents = []
        potential_children = []
        
        for agent in self.agents.values():
            if 25 <= agent.age <= 60:
                potential_parents.append(agent.agent_id)
            elif agent.age <= 18:
                potential_children.append(agent.agent_id)
        
        print(f"   Found {len(potential_parents)} potential parents")
        print(f"   Found {len(potential_children)} potential children")
        
        # Shuffle for randomness
        random.shuffle(potential_parents)
        random.shuffle(potential_children)
        
        families = []
        family_id = 1
        used_parents = set()
        used_children = set()
        
        # Create families
        while potential_parents or potential_children:
            # Decide family structure
            if not potential_parents:
                break
            
            # Number of parents (1 or 2)
            num_parents = random.choices([1, 2], weights=[0.2, 0.8])[0]  # 80% two-parent
            
            # Get parents
            parents = []
            for _ in range(num_parents):
                if potential_parents:
                    parent_id = potential_parents.pop(0)
                    parents.append(parent_id)
                    used_parents.add(parent_id)
            
            if not parents:
                break
            
            # Number of children (0-4)
            num_children = random.choices([0, 1, 2, 3, 4], weights=[0.1, 0.3, 0.4, 0.15, 0.05])[0]
            
            # Get children
            children = []
            for _ in range(num_children):
                if potential_children:
                    child_id = potential_children.pop(0)
                    children.append(child_id)
                    used_children.add(child_id)
            
            # Create family
            family = Family(
                family_id=family_id,
                parents=parents,
                children=children
            )
            families.append(family)
            family_id += 1
            
            # Create relationships
            self._create_family_relationships(family)
        
        print(f"✅ Created {len(families)} families")
        
        # Stats
        single_parent = sum(1 for f in families if len(f.parents) == 1)
        two_parent = sum(1 for f in families if len(f.parents) == 2)
        with_children = sum(1 for f in families if len(f.children) > 0)
        
        print(f"   - {single_parent} single-parent families")
        print(f"   - {two_parent} two-parent families")
        print(f"   - {with_children} families with children")
        
        return families
    
    def _create_family_relationships(self, family: Family):
        """Create relationships within a family"""
        # Parent-child relationships
        if family.children:
            create_family_relationships(
                family.parents,
                family.children,
                self.relationship_managers
            )
        
        # Spouse relationships (if two parents)
        if len(family.parents) == 2:
            create_spouse_relationships(
                family.parents[0],
                family.parents[1],
                self.relationship_managers
            )
        
        # Sibling relationships
        if len(family.children) >= 2:
            for i, child1_id in enumerate(family.children):
                for child2_id in family.children[i+1:]:
                    # Bidirectional sibling relationship
                    if child1_id in self.relationship_managers:
                        self.relationship_managers[child1_id].add_relationship(
                            child2_id,
                            RelationshipType.SIBLING,
                            strength=0.7
                        )
                    
                    if child2_id in self.relationship_managers:
                        self.relationship_managers[child2_id].add_relationship(
                            child1_id,
                            RelationshipType.SIBLING,
                            strength=0.7
                        )
    
    def assign_coworkers(self, workplaces: List[int]) -> Dict[int, List[int]]:
        """
        Assign agents to workplaces and create coworker relationships
        
        Args:
            workplaces: List of workplace location IDs
        
        Returns:
            Dict mapping workplace_id -> list of agent_ids
        """
        print("💼 Assigning coworkers...")
        
        # Find working-age agents
        workers = [
            agent_id for agent_id, agent in self.agents.items()
            if 18 <= agent.age <= 65 and agent.role not in ["student", "retired"]
        ]
        
        print(f"   Found {len(workers)} workers")
        
        # Shuffle workers
        random.shuffle(workers)
        
        # Assign to workplaces
        workplace_assignments = {wp_id: [] for wp_id in workplaces}
        
        for i, worker_id in enumerate(workers):
            workplace_id = workplaces[i % len(workplaces)]
            workplace_assignments[workplace_id].append(worker_id)
        
        # Create coworker relationships within each workplace
        total_coworker_relationships = 0
        for workplace_id, worker_ids in workplace_assignments.items():
            if len(worker_ids) >= 2:
                create_coworker_relationships(worker_ids, self.relationship_managers)
                # Count relationships created
                total_coworker_relationships += len(worker_ids) * (len(worker_ids) - 1) // 2
        
        print(f"✅ Created {total_coworker_relationships} coworker relationships")
        print(f"   Average {len(workers) / len(workplaces):.1f} workers per workplace")
        
        return workplace_assignments
    
    def generate_friend_networks(self, avg_friends: int = 3) -> int:
        """
        Generate friend networks
        
        Strategy:
        - Each agent gets 1-5 friends
        - Friends are similar age (within 10 years)
        - Some friendships are stronger (best friends)
        
        Args:
            avg_friends: Average number of friends per agent
        
        Returns:
            Number of friendships created
        """
        print("👥 Generating friend networks...")
        
        friendships_created = 0
        
        # Group agents by age range
        age_groups = {}
        for agent_id, agent in self.agents.items():
            age_group = agent.age // 10  # 0-9, 10-19, 20-29, etc.
            if age_group not in age_groups:
                age_groups[age_group] = []
            age_groups[age_group].append(agent_id)
        
        # Create friendships within age groups
        for age_group, agent_ids in age_groups.items():
            if len(agent_ids) < 2:
                continue
            
            for agent_id in agent_ids:
                # Skip if already has enough friends
                current_friends = len(self.relationship_managers[agent_id].get_friends())
                if current_friends >= avg_friends + 2:
                    continue
                
                # Decide how many friends to add
                num_friends = random.randint(1, avg_friends + 2) - current_friends
                if num_friends <= 0:
                    continue
                
                # Find potential friends (same age group, not already friends)
                potential_friends = [
                    other_id for other_id in agent_ids
                    if other_id != agent_id
                    and not self.relationship_managers[agent_id].has_relationship(other_id, RelationshipType.FRIEND)
                    and not self.relationship_managers[agent_id].has_relationship(other_id, RelationshipType.BEST_FRIEND)
                ]
                
                # Add friends
                num_to_add = min(num_friends, len(potential_friends))
                friends_to_add = random.sample(potential_friends, num_to_add)
                
                for friend_id in friends_to_add:
                    # 20% chance of best friend
                    is_best_friend = random.random() < 0.2
                    
                    create_friend_relationships(
                        agent_id,
                        friend_id,
                        self.relationship_managers,
                        is_best_friend=is_best_friend
                    )
                    
                    friendships_created += 1
        
        print(f"✅ Created {friendships_created} friendships")
        print(f"   Average {friendships_created / len(self.agents):.1f} friends per agent")
        
        return friendships_created
    
    def generate_neighbor_relationships(self, homes: List[int], home_assignments: Dict[int, List[int]]):
        """
        Generate neighbor relationships
        
        Args:
            homes: List of home location IDs
            home_assignments: Dict mapping home_id -> list of agent_ids living there
        """
        print("🏘️  Generating neighbor relationships...")
        
        neighbors_created = 0
        
        # For each home, find nearby homes and create neighbor relationships
        for i, home_id in enumerate(homes):
            agents_in_home = home_assignments.get(home_id, [])
            if not agents_in_home:
                continue
            
            # Find nearby homes (next 2-3 homes in list)
            nearby_homes = homes[max(0, i-2):i] + homes[i+1:min(len(homes), i+3)]
            
            for nearby_home_id in nearby_homes:
                agents_in_nearby = home_assignments.get(nearby_home_id, [])
                
                # Create neighbor relationships between adults
                for agent_id in agents_in_home:
                    agent = self.agents[agent_id]
                    if agent.age < 18:
                        continue
                    
                    for neighbor_id in agents_in_nearby:
                        neighbor = self.agents[neighbor_id]
                        if neighbor.age < 18:
                            continue
                        
                        # 50% chance of knowing neighbor
                        if random.random() < 0.5:
                            # Check if relationship already exists
                            if not self.relationship_managers[agent_id].has_relationship(neighbor_id):
                                # Create neighbor relationship
                                if agent_id in self.relationship_managers:
                                    self.relationship_managers[agent_id].add_relationship(
                                        neighbor_id,
                                        RelationshipType.NEIGHBOR,
                                        strength=0.4
                                    )
                                
                                if neighbor_id in self.relationship_managers:
                                    self.relationship_managers[neighbor_id].add_relationship(
                                        agent_id,
                                        RelationshipType.NEIGHBOR,
                                        strength=0.4
                                    )
                                
                                neighbors_created += 1
        
        print(f"✅ Created {neighbors_created} neighbor relationships")
    
    def get_relationship_stats(self) -> Dict:
        """Get statistics about relationships"""
        total_relationships = 0
        family_count = 0
        friend_count = 0
        coworker_count = 0
        neighbor_count = 0
        
        for manager in self.relationship_managers.values():
            total_relationships += len(manager.relationships)
            family_count += len(manager.get_family())
            friend_count += len(manager.get_friends())
            coworker_count += len(manager.get_coworkers())
            neighbor_count += len(manager.get_relationships_by_type(RelationshipType.NEIGHBOR))
        
        return {
            "total_relationships": total_relationships,
            "avg_relationships_per_agent": total_relationships / len(self.agents) if self.agents else 0,
            "family_relationships": family_count,
            "friend_relationships": friend_count,
            "coworker_relationships": coworker_count,
            "neighbor_relationships": neighbor_count
        }
