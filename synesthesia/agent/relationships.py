"""
Relationship System - Family, friends, coworkers, etc.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum


class RelationshipType(Enum):
    """Types of relationships between agents"""
    # Family
    PARENT = "parent"
    CHILD = "child"
    SPOUSE = "spouse"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"
    
    # Work
    COWORKER = "coworker"
    BOSS = "boss"
    EMPLOYEE = "employee"
    
    # Social
    FRIEND = "friend"
    BEST_FRIEND = "best_friend"
    ACQUAINTANCE = "acquaintance"
    NEIGHBOR = "neighbor"
    
    # Romantic
    DATING = "dating"
    EX = "ex"
    
    # Other
    THERAPIST = "therapist"
    DOCTOR = "doctor"
    TEACHER = "teacher"
    STUDENT = "student"


@dataclass
class Relationship:
    """A relationship between two agents"""
    agent_id: int  # The other agent
    relationship_type: RelationshipType
    strength: float = 0.5  # 0.0 (weak) to 1.0 (strong)
    
    # Relationship quality
    trust: float = 0.5
    affection: float = 0.5
    respect: float = 0.5
    
    # History
    interactions_count: int = 0
    last_interaction_time: Optional[str] = None
    
    # Metadata
    notes: List[str] = field(default_factory=list)
    
    def update_quality(self, trust_delta: float = 0, affection_delta: float = 0, respect_delta: float = 0):
        """Update relationship quality"""
        self.trust = max(0.0, min(1.0, self.trust + trust_delta))
        self.affection = max(0.0, min(1.0, self.affection + affection_delta))
        self.respect = max(0.0, min(1.0, self.respect + respect_delta))
        
        # Update overall strength
        self.strength = (self.trust + self.affection + self.respect) / 3.0
    
    def record_interaction(self, time: str, note: str = ""):
        """Record an interaction"""
        self.interactions_count += 1
        self.last_interaction_time = time
        if note:
            self.notes.append(f"[{time}] {note}")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "relationship_type": self.relationship_type.value,
            "strength": self.strength,
            "trust": self.trust,
            "affection": self.affection,
            "respect": self.respect,
            "interactions_count": self.interactions_count,
            "last_interaction_time": self.last_interaction_time,
            "notes": self.notes[-5:]  # Last 5 notes
        }


class RelationshipManager:
    """Manages relationships for an agent"""
    
    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.relationships: Dict[int, Relationship] = {}  # other_agent_id -> Relationship
    
    def add_relationship(
        self,
        other_agent_id: int,
        relationship_type: RelationshipType,
        strength: float = 0.5
    ) -> Relationship:
        """Add a new relationship"""
        rel = Relationship(
            agent_id=other_agent_id,
            relationship_type=relationship_type,
            strength=strength
        )
        self.relationships[other_agent_id] = rel
        return rel
    
    def get_relationship(self, other_agent_id: int) -> Optional[Relationship]:
        """Get relationship with another agent"""
        return self.relationships.get(other_agent_id)
    
    def has_relationship(self, other_agent_id: int, relationship_type: Optional[RelationshipType] = None) -> bool:
        """Check if has relationship with another agent"""
        rel = self.relationships.get(other_agent_id)
        if not rel:
            return False
        if relationship_type:
            return rel.relationship_type == relationship_type
        return True
    
    def get_relationships_by_type(self, relationship_type: RelationshipType) -> List[Relationship]:
        """Get all relationships of a specific type"""
        return [rel for rel in self.relationships.values() if rel.relationship_type == relationship_type]
    
    def get_family(self) -> List[Relationship]:
        """Get all family relationships"""
        family_types = {
            RelationshipType.PARENT,
            RelationshipType.CHILD,
            RelationshipType.SPOUSE,
            RelationshipType.SIBLING,
            RelationshipType.GRANDPARENT,
            RelationshipType.GRANDCHILD
        }
        return [rel for rel in self.relationships.values() if rel.relationship_type in family_types]
    
    def get_friends(self) -> List[Relationship]:
        """Get all friend relationships"""
        friend_types = {RelationshipType.FRIEND, RelationshipType.BEST_FRIEND}
        return [rel for rel in self.relationships.values() if rel.relationship_type in friend_types]
    
    def get_coworkers(self) -> List[Relationship]:
        """Get all coworker relationships"""
        work_types = {RelationshipType.COWORKER, RelationshipType.BOSS, RelationshipType.EMPLOYEE}
        return [rel for rel in self.relationships.values() if rel.relationship_type in work_types]
    
    def get_closest_relationships(self, limit: int = 5) -> List[Relationship]:
        """Get closest relationships by strength"""
        return sorted(self.relationships.values(), key=lambda r: r.strength, reverse=True)[:limit]
    
    def update_relationship_quality(
        self,
        other_agent_id: int,
        trust_delta: float = 0,
        affection_delta: float = 0,
        respect_delta: float = 0
    ):
        """Update relationship quality"""
        rel = self.relationships.get(other_agent_id)
        if rel:
            rel.update_quality(trust_delta, affection_delta, respect_delta)
    
    def record_interaction(self, other_agent_id: int, time: str, note: str = ""):
        """Record an interaction with another agent"""
        rel = self.relationships.get(other_agent_id)
        if rel:
            rel.record_interaction(time, note)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "total_relationships": len(self.relationships),
            "family": len(self.get_family()),
            "friends": len(self.get_friends()),
            "coworkers": len(self.get_coworkers()),
            "relationships": {
                other_id: rel.to_dict()
                for other_id, rel in self.relationships.items()
            }
        }


def create_family_relationships(
    parent_ids: List[int],
    child_ids: List[int],
    relationship_managers: Dict[int, RelationshipManager]
):
    """Create parent-child relationships"""
    for parent_id in parent_ids:
        for child_id in child_ids:
            # Parent -> Child
            if parent_id in relationship_managers:
                relationship_managers[parent_id].add_relationship(
                    child_id,
                    RelationshipType.CHILD,
                    strength=0.9
                )
            
            # Child -> Parent
            if child_id in relationship_managers:
                relationship_managers[child_id].add_relationship(
                    parent_id,
                    RelationshipType.PARENT,
                    strength=0.9
                )


def create_spouse_relationships(
    agent1_id: int,
    agent2_id: int,
    relationship_managers: Dict[int, RelationshipManager]
):
    """Create spouse relationships"""
    if agent1_id in relationship_managers:
        relationship_managers[agent1_id].add_relationship(
            agent2_id,
            RelationshipType.SPOUSE,
            strength=0.8
        )
    
    if agent2_id in relationship_managers:
        relationship_managers[agent2_id].add_relationship(
            agent1_id,
            RelationshipType.SPOUSE,
            strength=0.8
        )


def create_coworker_relationships(
    agent_ids: List[int],
    relationship_managers: Dict[int, RelationshipManager]
):
    """Create coworker relationships among a group"""
    for i, agent1_id in enumerate(agent_ids):
        for agent2_id in agent_ids[i+1:]:
            # Bidirectional coworker relationship
            if agent1_id in relationship_managers:
                relationship_managers[agent1_id].add_relationship(
                    agent2_id,
                    RelationshipType.COWORKER,
                    strength=0.5
                )
            
            if agent2_id in relationship_managers:
                relationship_managers[agent2_id].add_relationship(
                    agent1_id,
                    RelationshipType.COWORKER,
                    strength=0.5
                )


def create_friend_relationships(
    agent1_id: int,
    agent2_id: int,
    relationship_managers: Dict[int, RelationshipManager],
    is_best_friend: bool = False
):
    """Create friend relationships"""
    rel_type = RelationshipType.BEST_FRIEND if is_best_friend else RelationshipType.FRIEND
    strength = 0.8 if is_best_friend else 0.6
    
    if agent1_id in relationship_managers:
        relationship_managers[agent1_id].add_relationship(
            agent2_id,
            rel_type,
            strength=strength
        )
    
    if agent2_id in relationship_managers:
        relationship_managers[agent2_id].add_relationship(
            agent1_id,
            rel_type,
            strength=strength
        )
