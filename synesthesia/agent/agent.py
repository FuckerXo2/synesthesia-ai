"""
Agent class - represents a person in the simulation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from synesthesia.agent.state import MentalHealthState, MentalHealthCategory
from synesthesia.agent.relationships import RelationshipManager
from synesthesia.agent.identity import AgentIdentity, MemoryManager, Memory


@dataclass
class Agent:
    """Represents a person in the Synesthesia simulation"""
    
    # Identity
    agent_id: int
    name: str
    age: int
    role: str  # student, worker, parent, etc.
    sub_role: str = ""  # freshman, software_engineer, single_parent, etc.
    
    # Demographics
    gender: str = "non-binary"
    family_status: str = "single"
    has_children: bool = False
    num_children: int = 0
    
    # Personality
    personality_traits: List[str] = field(default_factory=list)
    
    # Mental health
    mental_health: MentalHealthState = field(default_factory=MentalHealthState)
    
    # Schedule (hours 0-23)
    work_hours: List[int] = field(default_factory=list)
    sleep_hours: List[int] = field(default_factory=list)
    active_hours: List[int] = field(default_factory=list)
    
    # Stressors and coping
    stressors: List[str] = field(default_factory=list)
    coping_mechanisms: List[str] = field(default_factory=list)
    
    # Therapy
    therapy_access: bool = False
    therapy_willingness: float = 0.5
    
    # Social connections (agent IDs)
    family_connections: List[int] = field(default_factory=list)
    friend_connections: List[int] = field(default_factory=list)
    work_connections: List[int] = field(default_factory=list)
    
    # Memory (recent events/actions)
    recent_actions: List[str] = field(default_factory=list)
    recent_events: List[str] = field(default_factory=list)
    
    # NEW: Identity and Memory
    identity: Optional[AgentIdentity] = None
    memory: Optional[MemoryManager] = None
    
    def __post_init__(self):
        """Initialize derived fields"""
        if isinstance(self.mental_health, dict):
            self.mental_health = MentalHealthState.from_dict(self.mental_health)
        
        # Initialize relationship manager
        self.relationships = RelationshipManager(self.agent_id)
        
        # Initialize memory manager if not provided
        if self.memory is None:
            self.memory = MemoryManager(self.agent_id)
    
    @property
    def is_in_crisis(self) -> bool:
        """Check if agent is in mental health crisis"""
        return self.mental_health.category == MentalHealthCategory.CRISIS
    
    @property
    def is_thriving(self) -> bool:
        """Check if agent is thriving"""
        return self.mental_health.category == MentalHealthCategory.THRIVING
    
    @property
    def needs_help(self) -> bool:
        """Check if agent needs mental health help"""
        return self.mental_health.overall_distress > 0.5
    
    def is_awake(self, current_hour: int) -> bool:
        """Check if agent is awake at given hour"""
        return current_hour not in self.sleep_hours
    
    def is_working(self, current_hour: int) -> bool:
        """Check if agent is at work/school"""
        return current_hour in self.work_hours
    
    def is_free(self, current_hour: int) -> bool:
        """Check if agent has free time"""
        return current_hour in self.active_hours
    
    def update_mental_health(self, changes: Dict[str, float]):
        """Update mental health state"""
        self.mental_health.update(changes)
    
    def add_recent_action(self, action: str, max_memory: int = 10):
        """Add action to recent memory"""
        self.recent_actions.append(action)
        if len(self.recent_actions) > max_memory:
            self.recent_actions.pop(0)
    
    def add_recent_event(self, event: str, max_memory: int = 10):
        """Add event to recent memory"""
        self.recent_events.append(event)
        if len(self.recent_events) > max_memory:
            self.recent_events.pop(0)
    
    def remember(self, memory: Memory):
        """Add a memory"""
        if self.memory:
            self.memory.add_memory(memory)
    
    def get_full_context(self) -> Dict[str, Any]:
        """
        Get complete agent context including identity and memories
        For LLM prompts
        """
        context = {
            "name": self.name,
            "age": self.age,
            "role": self.role,
            "personality_traits": self.personality_traits,
            "mental_health": {
                "anxiety": self.mental_health.anxiety,
                "depression": self.mental_health.depression,
                "stress": self.mental_health.stress,
                "wellbeing": self.mental_health.wellbeing,
                "category": self.mental_health.category.value
            }
        }
        
        # Add identity if available
        if self.identity:
            context["backstory"] = self.identity.backstory
            context["values"] = self.identity.values
            context["fears"] = self.identity.fears
            context["goals"] = self.identity.goals
            context["coping_mechanisms"] = self.identity.coping_mechanisms
            context["quirks"] = self.identity.quirks
        
        # Add recent memories if available
        if self.memory:
            context["recent_memories"] = self.memory.get_memory_context_for_llm(5)
            context["resilience"] = self.memory.get_resilience_score()
        
        return context
    
    def get_context(self) -> str:
        """
        Get agent context for LLM prompts
        
        Returns:
            String describing agent's current state
        """
        context = f"""
Agent Profile:
- Name: {self.name}
- Age: {self.age}
- Role: {self.role} ({self.sub_role})
- Family: {self.family_status}
{f"- Children: {self.num_children}" if self.has_children else ""}

Personality: {', '.join(self.personality_traits)}
"""
        
        # Add identity if available
        if self.identity and self.identity.backstory:
            context += f"\nBackstory: {self.identity.backstory}\n"
            if self.identity.values:
                context += f"Values: {', '.join(self.identity.values)}\n"
            if self.identity.fears:
                context += f"Fears: {', '.join(self.identity.fears)}\n"
        
        context += f"""
Mental Health:
- Anxiety: {self.mental_health.anxiety:.2f}
- Depression: {self.mental_health.depression:.2f}
- Stress: {self.mental_health.stress:.2f}
- Wellbeing: {self.mental_health.wellbeing:.2f}
- Overall State: {self.mental_health.category.value}

Current Stressors: {', '.join(self.stressors)}
Coping Mechanisms: {', '.join(self.coping_mechanisms)}
"""
        
        # Add memories if available
        if self.memory:
            context += f"\n{self.memory.get_memory_context_for_llm(5)}\n"
        else:
            context += f"\nRecent Actions: {', '.join(self.recent_actions[-5:]) if self.recent_actions else 'None'}\n"
            context += f"Recent Events: {', '.join(self.recent_events[-5:]) if self.recent_events else 'None'}\n"
        
        return context.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary for database storage"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "age": self.age,
            "role": self.role,
            "sub_role": self.sub_role,
            "gender": self.gender,
            "family_status": self.family_status,
            "has_children": self.has_children,
            "num_children": self.num_children,
            "personality_traits": self.personality_traits,
            "work_hours": self.work_hours,
            "sleep_hours": self.sleep_hours,
            "active_hours": self.active_hours,
            "stressors": self.stressors,
            "coping_mechanisms": self.coping_mechanisms,
            "therapy_access": self.therapy_access,
            "therapy_willingness": self.therapy_willingness,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Agent':
        """Create agent from dictionary"""
        # Extract mental health if present
        mental_health_data = {
            k: data.pop(k) for k in ['anxiety', 'depression', 'stress', 'wellbeing']
            if k in data
        }
        
        if mental_health_data:
            data['mental_health'] = MentalHealthState.from_dict(mental_health_data)
        
        return cls(**data)
    
    def __repr__(self) -> str:
        return (f"Agent(id={self.agent_id}, name='{self.name}', "
                f"role='{self.role}', state={self.mental_health.category.value})")
