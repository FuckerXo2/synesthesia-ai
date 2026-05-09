"""
Agent Memory System
Agents remember past interactions, events, and experiences
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque


class Memory:
    """Represents a single memory"""
    
    def __init__(
        self,
        memory_type: str,
        content: str,
        timestamp: datetime,
        emotional_impact: float = 0.0,
        importance: float = 0.5
    ):
        self.memory_type = memory_type  # conversation, event, action, observation
        self.content = content
        self.timestamp = timestamp
        self.emotional_impact = emotional_impact  # -1.0 (negative) to 1.0 (positive)
        self.importance = importance  # 0.0 to 1.0
        self.recall_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'memory_type': self.memory_type,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'emotional_impact': self.emotional_impact,
            'importance': self.importance,
            'recall_count': self.recall_count
        }


class AgentMemory:
    """Memory system for an agent"""
    
    def __init__(self, max_short_term: int = 20, max_long_term: int = 100):
        self.short_term = deque(maxlen=max_short_term)  # Recent memories
        self.long_term = deque(maxlen=max_long_term)    # Important memories
        self.working_memory = []  # Currently active memories
        
    def add_memory(
        self,
        memory_type: str,
        content: str,
        emotional_impact: float = 0.0,
        importance: float = 0.5
    ):
        """Add a new memory"""
        memory = Memory(
            memory_type=memory_type,
            content=content,
            timestamp=datetime.now(),
            emotional_impact=emotional_impact,
            importance=importance
        )
        
        # Add to short-term memory
        self.short_term.append(memory)
        
        # If important enough, add to long-term memory
        if importance > 0.7 or abs(emotional_impact) > 0.7:
            self.long_term.append(memory)
    
    def recall_recent(self, n: int = 5) -> List[Memory]:
        """Recall the N most recent memories"""
        memories = list(self.short_term)[-n:]
        for memory in memories:
            memory.recall_count += 1
        return memories
    
    def recall_important(self, n: int = 5) -> List[Memory]:
        """Recall the N most important memories"""
        memories = sorted(
            self.long_term,
            key=lambda m: m.importance * (1 + m.recall_count * 0.1),
            reverse=True
        )[:n]
        for memory in memories:
            memory.recall_count += 1
        return memories
    
    def recall_by_type(self, memory_type: str, n: int = 5) -> List[Memory]:
        """Recall memories of a specific type"""
        all_memories = list(self.short_term) + list(self.long_term)
        filtered = [m for m in all_memories if m.memory_type == memory_type]
        return sorted(filtered, key=lambda m: m.timestamp, reverse=True)[:n]
    
    def recall_emotional(self, positive: bool = True, n: int = 5) -> List[Memory]:
        """Recall emotionally charged memories"""
        all_memories = list(self.short_term) + list(self.long_term)
        if positive:
            filtered = [m for m in all_memories if m.emotional_impact > 0.5]
        else:
            filtered = [m for m in all_memories if m.emotional_impact < -0.5]
        return sorted(filtered, key=lambda m: abs(m.emotional_impact), reverse=True)[:n]
    
    def get_context_summary(self, max_memories: int = 10) -> str:
        """Get a text summary of recent context for LLM prompts"""
        recent = self.recall_recent(max_memories // 2)
        important = self.recall_important(max_memories // 2)
        
        # Combine and deduplicate
        all_memories = list(set(recent + important))
        all_memories.sort(key=lambda m: m.timestamp, reverse=True)
        
        if not all_memories:
            return "No significant memories."
        
        summary_parts = []
        for memory in all_memories[:max_memories]:
            summary_parts.append(f"- {memory.content}")
        
        return "\n".join(summary_parts)
    
    def clear_working_memory(self):
        """Clear working memory (used between decision cycles)"""
        self.working_memory = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory for storage"""
        return {
            'short_term': [m.to_dict() for m in self.short_term],
            'long_term': [m.to_dict() for m in self.long_term],
            'working_memory': [m.to_dict() for m in self.working_memory]
        }
