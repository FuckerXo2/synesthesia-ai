"""
Agent Identity System - Backstory, values, fears, goals, quirks
Makes each agent a unique individual with depth
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class AgentIdentity:
    """
    The core identity of an agent - who they are beyond stats
    """
    agent_id: int
    
    # Core identity (generated once by LLM)
    backstory: str = ""
    values: List[str] = field(default_factory=list)  # What matters to them
    fears: List[str] = field(default_factory=list)  # What scares them
    goals: List[str] = field(default_factory=list)  # What they want
    coping_mechanisms: List[str] = field(default_factory=list)  # How they handle stress
    quirks: List[str] = field(default_factory=list)  # Memorable traits
    
    # Social identity
    reputation: Dict[str, float] = field(default_factory=dict)  # How others see them
    social_groups: List[str] = field(default_factory=list)  # Groups they belong to
    
    # Metadata
    generated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "backstory": self.backstory,
            "values": self.values,
            "fears": self.fears,
            "goals": self.goals,
            "coping_mechanisms": self.coping_mechanisms,
            "quirks": self.quirks,
            "reputation": self.reputation,
            "social_groups": self.social_groups,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentIdentity':
        """Create from dictionary"""
        generated_at = None
        if data.get('generated_at'):
            generated_at = datetime.fromisoformat(data['generated_at'])
        
        return cls(
            agent_id=data['agent_id'],
            backstory=data.get('backstory', ''),
            values=data.get('values', []),
            fears=data.get('fears', []),
            goals=data.get('goals', []),
            coping_mechanisms=data.get('coping_mechanisms', []),
            quirks=data.get('quirks', []),
            reputation=data.get('reputation', {}),
            social_groups=data.get('social_groups', []),
            generated_at=generated_at
        )
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        summary = f"Agent #{self.agent_id} Identity:\n"
        
        if self.backstory:
            summary += f"\nBackstory: {self.backstory}\n"
        
        if self.values:
            summary += f"\nValues: {', '.join(self.values)}"
        
        if self.fears:
            summary += f"\nFears: {', '.join(self.fears)}"
        
        if self.goals:
            summary += f"\nGoals: {', '.join(self.goals)}"
        
        if self.coping_mechanisms:
            summary += f"\nCoping: {', '.join(self.coping_mechanisms)}"
        
        if self.quirks:
            summary += f"\nQuirks: {', '.join(self.quirks)}"
        
        if self.social_groups:
            summary += f"\nGroups: {', '.join(self.social_groups)}"
        
        return summary


@dataclass
class Memory:
    """
    A memory of an event that happened to an agent
    """
    event_type: str  # "conversation", "work_event", "crisis", etc.
    description: str
    timestamp: datetime
    
    # Emotional impact
    emotional_impact: float  # -1.0 (devastating) to 1.0 (amazing)
    emotional_tags: List[str] = field(default_factory=list)  # ["stressful", "comforting", etc.]
    
    # People involved
    people_involved: List[int] = field(default_factory=list)  # Agent IDs
    
    # Mental health changes
    mental_health_change: Dict[str, float] = field(default_factory=dict)
    
    # Relationship changes
    relationship_changes: Dict[int, float] = field(default_factory=dict)  # agent_id -> change
    
    # Additional context
    location: Optional[str] = None
    conversation_snippet: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_traumatic(self) -> bool:
        """Check if this is a traumatic memory"""
        return self.emotional_impact < -0.5
    
    def is_positive(self) -> bool:
        """Check if this is a positive memory"""
        return self.emotional_impact > 0.3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "event_type": self.event_type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "emotional_impact": self.emotional_impact,
            "emotional_tags": self.emotional_tags,
            "people_involved": self.people_involved,
            "mental_health_change": self.mental_health_change,
            "relationship_changes": self.relationship_changes,
            "location": self.location,
            "conversation_snippet": self.conversation_snippet,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        """Create from dictionary"""
        return cls(
            event_type=data['event_type'],
            description=data['description'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            emotional_impact=data.get('emotional_impact', 0.0),
            emotional_tags=data.get('emotional_tags', []),
            people_involved=data.get('people_involved', []),
            mental_health_change=data.get('mental_health_change', {}),
            relationship_changes=data.get('relationship_changes', {}),
            location=data.get('location'),
            conversation_snippet=data.get('conversation_snippet'),
            metadata=data.get('metadata', {})
        )


class MemoryManager:
    """
    Manages an agent's memories
    """
    
    def __init__(self, agent_id: int, max_memories: int = 50):
        """
        Initialize memory manager
        
        Args:
            agent_id: Agent ID
            max_memories: Maximum number of memories to keep
        """
        self.agent_id = agent_id
        self.max_memories = max_memories
        
        # All memories (recent)
        self.memories: List[Memory] = []
        
        # Special memory categories
        self.trauma: List[Memory] = []  # Traumatic events
        self.positive_memories: List[Memory] = []  # Happy memories (resilience)
        self.significant_relationships: Dict[int, List[Memory]] = {}  # Memories by person
    
    def add_memory(self, memory: Memory):
        """Add a new memory"""
        self.memories.append(memory)
        
        # Categorize
        if memory.is_traumatic():
            self.trauma.append(memory)
        elif memory.is_positive():
            self.positive_memories.append(memory)
        
        # Track by person
        for person_id in memory.people_involved:
            if person_id not in self.significant_relationships:
                self.significant_relationships[person_id] = []
            self.significant_relationships[person_id].append(memory)
        
        # Prune old memories if too many
        if len(self.memories) > self.max_memories:
            # Keep trauma and very positive memories
            important = [m for m in self.memories if m.is_traumatic() or m.emotional_impact > 0.7]
            recent = sorted(self.memories, key=lambda m: m.timestamp, reverse=True)[:self.max_memories - len(important)]
            self.memories = list(set(important + recent))
    
    def get_recent_memories(self, count: int = 10) -> List[Memory]:
        """Get most recent memories"""
        return sorted(self.memories, key=lambda m: m.timestamp, reverse=True)[:count]
    
    def get_memories_with_person(self, person_id: int, count: int = 5) -> List[Memory]:
        """Get memories involving a specific person"""
        memories = self.significant_relationships.get(person_id, [])
        return sorted(memories, key=lambda m: m.timestamp, reverse=True)[:count]
    
    def get_trauma_summary(self) -> str:
        """Get summary of traumatic experiences"""
        if not self.trauma:
            return "No significant trauma"
        
        recent_trauma = sorted(self.trauma, key=lambda m: m.timestamp, reverse=True)[:3]
        return "; ".join([m.description for m in recent_trauma])
    
    def get_resilience_score(self) -> float:
        """
        Calculate resilience based on positive vs negative memories
        More positive memories = higher resilience
        """
        if not self.memories:
            return 0.5
        
        positive_count = len(self.positive_memories)
        trauma_count = len(self.trauma)
        
        # Resilience = positive memories / (positive + trauma)
        total = positive_count + trauma_count
        if total == 0:
            return 0.5
        
        return positive_count / total
    
    def get_memory_context_for_llm(self, max_memories: int = 10) -> str:
        """
        Get memory context formatted for LLM
        """
        recent = self.get_recent_memories(max_memories)
        
        if not recent:
            return "No significant recent memories"
        
        context = "Recent memories:\n"
        for i, memory in enumerate(recent, 1):
            impact = "devastating" if memory.emotional_impact < -0.5 else \
                     "negative" if memory.emotional_impact < 0 else \
                     "neutral" if memory.emotional_impact < 0.3 else \
                     "positive" if memory.emotional_impact < 0.7 else \
                     "amazing"
            
            context += f"{i}. {memory.description} ({impact})\n"
        
        return context
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "max_memories": self.max_memories,
            "memories": [m.to_dict() for m in self.memories],
            "trauma": [m.to_dict() for m in self.trauma],
            "positive_memories": [m.to_dict() for m in self.positive_memories]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryManager':
        """Create from dictionary"""
        manager = cls(
            agent_id=data['agent_id'],
            max_memories=data.get('max_memories', 50)
        )
        
        manager.memories = [Memory.from_dict(m) for m in data.get('memories', [])]
        manager.trauma = [Memory.from_dict(m) for m in data.get('trauma', [])]
        manager.positive_memories = [Memory.from_dict(m) for m in data.get('positive_memories', [])]
        
        # Rebuild significant_relationships
        for memory in manager.memories:
            for person_id in memory.people_involved:
                if person_id not in manager.significant_relationships:
                    manager.significant_relationships[person_id] = []
                manager.significant_relationships[person_id].append(memory)
        
        return manager
