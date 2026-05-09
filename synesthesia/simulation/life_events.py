"""
Life Events System
Random events that happen to agents (job loss, promotion, breakup, etc.)
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class LifeEventType(Enum):
    """Types of life events"""
    # Positive events
    PROMOTION = "promotion"
    NEW_RELATIONSHIP = "new_relationship"
    MARRIAGE = "marriage"
    BIRTH_OF_CHILD = "birth_of_child"
    NEW_FRIENDSHIP = "new_friendship"
    ACHIEVEMENT = "achievement"
    WINDFALL = "windfall"
    RECOVERY = "recovery"
    
    # Negative events
    JOB_LOSS = "job_loss"
    BREAKUP = "breakup"
    DIVORCE = "divorce"
    DEATH_OF_LOVED_ONE = "death_of_loved_one"
    ILLNESS = "illness"
    INJURY = "injury"
    FINANCIAL_CRISIS = "financial_crisis"
    CONFLICT = "conflict"
    BETRAYAL = "betrayal"
    
    # Neutral/Mixed events
    JOB_CHANGE = "job_change"
    RELOCATION = "relocation"
    MAJOR_PURCHASE = "major_purchase"
    LIFE_MILESTONE = "life_milestone"


class LifeEvent:
    """Represents a life event"""
    
    def __init__(
        self,
        event_type: LifeEventType,
        description: str,
        mental_health_impact: Dict[str, float],
        duration_hours: int = 24,
        severity: float = 0.5
    ):
        self.event_type = event_type
        self.description = description
        self.mental_health_impact = mental_health_impact
        self.duration_hours = duration_hours
        self.severity = severity
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type.value,
            'description': self.description,
            'mental_health_impact': self.mental_health_impact,
            'duration_hours': self.duration_hours,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat()
        }


class LifeEventGenerator:
    """Generates random life events for agents"""
    
    # Event probabilities per 24-hour period
    EVENT_PROBABILITIES = {
        # Positive events (5% chance per day)
        LifeEventType.PROMOTION: 0.001,
        LifeEventType.NEW_RELATIONSHIP: 0.002,
        LifeEventType.MARRIAGE: 0.0005,
        LifeEventType.BIRTH_OF_CHILD: 0.0003,
        LifeEventType.NEW_FRIENDSHIP: 0.01,
        LifeEventType.ACHIEVEMENT: 0.005,
        LifeEventType.WINDFALL: 0.001,
        LifeEventType.RECOVERY: 0.002,
        
        # Negative events (3% chance per day)
        LifeEventType.JOB_LOSS: 0.001,
        LifeEventType.BREAKUP: 0.002,
        LifeEventType.DIVORCE: 0.0005,
        LifeEventType.DEATH_OF_LOVED_ONE: 0.0003,
        LifeEventType.ILLNESS: 0.005,
        LifeEventType.INJURY: 0.003,
        LifeEventType.FINANCIAL_CRISIS: 0.002,
        LifeEventType.CONFLICT: 0.01,
        LifeEventType.BETRAYAL: 0.001,
        
        # Neutral events (2% chance per day)
        LifeEventType.JOB_CHANGE: 0.002,
        LifeEventType.RELOCATION: 0.001,
        LifeEventType.MAJOR_PURCHASE: 0.005,
        LifeEventType.LIFE_MILESTONE: 0.002,
    }
    
    # Mental health impacts for each event type
    EVENT_IMPACTS = {
        # Positive events
        LifeEventType.PROMOTION: {
            'anxiety': -0.15,
            'depression': -0.20,
            'stress': 0.05,  # Initial stress from new responsibilities
            'wellbeing': 0.25
        },
        LifeEventType.NEW_RELATIONSHIP: {
            'anxiety': -0.10,
            'depression': -0.25,
            'stress': -0.05,
            'wellbeing': 0.30
        },
        LifeEventType.MARRIAGE: {
            'anxiety': -0.05,
            'depression': -0.20,
            'stress': 0.10,  # Wedding stress
            'wellbeing': 0.35
        },
        LifeEventType.BIRTH_OF_CHILD: {
            'anxiety': 0.15,  # New parent anxiety
            'depression': -0.10,
            'stress': 0.25,
            'wellbeing': 0.20
        },
        LifeEventType.NEW_FRIENDSHIP: {
            'anxiety': -0.05,
            'depression': -0.10,
            'stress': -0.05,
            'wellbeing': 0.15
        },
        LifeEventType.ACHIEVEMENT: {
            'anxiety': -0.10,
            'depression': -0.15,
            'stress': -0.10,
            'wellbeing': 0.25
        },
        LifeEventType.WINDFALL: {
            'anxiety': -0.15,
            'depression': -0.10,
            'stress': -0.20,
            'wellbeing': 0.30
        },
        LifeEventType.RECOVERY: {
            'anxiety': -0.20,
            'depression': -0.25,
            'stress': -0.15,
            'wellbeing': 0.35
        },
        
        # Negative events
        LifeEventType.JOB_LOSS: {
            'anxiety': 0.30,
            'depression': 0.25,
            'stress': 0.35,
            'wellbeing': -0.40
        },
        LifeEventType.BREAKUP: {
            'anxiety': 0.20,
            'depression': 0.30,
            'stress': 0.15,
            'wellbeing': -0.35
        },
        LifeEventType.DIVORCE: {
            'anxiety': 0.25,
            'depression': 0.35,
            'stress': 0.30,
            'wellbeing': -0.45
        },
        LifeEventType.DEATH_OF_LOVED_ONE: {
            'anxiety': 0.20,
            'depression': 0.50,
            'stress': 0.25,
            'wellbeing': -0.60
        },
        LifeEventType.ILLNESS: {
            'anxiety': 0.25,
            'depression': 0.20,
            'stress': 0.20,
            'wellbeing': -0.30
        },
        LifeEventType.INJURY: {
            'anxiety': 0.20,
            'depression': 0.15,
            'stress': 0.25,
            'wellbeing': -0.25
        },
        LifeEventType.FINANCIAL_CRISIS: {
            'anxiety': 0.35,
            'depression': 0.25,
            'stress': 0.40,
            'wellbeing': -0.35
        },
        LifeEventType.CONFLICT: {
            'anxiety': 0.15,
            'depression': 0.10,
            'stress': 0.20,
            'wellbeing': -0.15
        },
        LifeEventType.BETRAYAL: {
            'anxiety': 0.25,
            'depression': 0.30,
            'stress': 0.20,
            'wellbeing': -0.40
        },
        
        # Neutral events
        LifeEventType.JOB_CHANGE: {
            'anxiety': 0.10,
            'depression': 0.0,
            'stress': 0.15,
            'wellbeing': 0.05
        },
        LifeEventType.RELOCATION: {
            'anxiety': 0.15,
            'depression': 0.05,
            'stress': 0.20,
            'wellbeing': -0.05
        },
        LifeEventType.MAJOR_PURCHASE: {
            'anxiety': 0.10,
            'depression': -0.05,
            'stress': 0.10,
            'wellbeing': 0.10
        },
        LifeEventType.LIFE_MILESTONE: {
            'anxiety': 0.05,
            'depression': -0.10,
            'stress': 0.05,
            'wellbeing': 0.15
        },
    }
    
    def __init__(self, event_rate_multiplier: float = 1.0):
        """
        Initialize life event generator
        
        Args:
            event_rate_multiplier: Multiply event probabilities (1.0 = normal, 2.0 = 2x events)
        """
        self.event_rate_multiplier = event_rate_multiplier
    
    def generate_event_for_agent(self, agent_data: Dict[str, Any]) -> Optional[LifeEvent]:
        """
        Generate a random life event for an agent
        
        Args:
            agent_data: Agent information (role, age, mental health, etc.)
            
        Returns:
            LifeEvent if one occurs, None otherwise
        """
        # Check each event type
        for event_type, base_probability in self.EVENT_PROBABILITIES.items():
            # Adjust probability based on agent context
            probability = base_probability * self.event_rate_multiplier
            probability = self._adjust_probability_for_agent(event_type, agent_data, probability)
            
            # Roll for event
            if random.random() < probability:
                return self._create_event(event_type, agent_data)
        
        return None
    
    def _adjust_probability_for_agent(
        self,
        event_type: LifeEventType,
        agent_data: Dict[str, Any],
        base_probability: float
    ) -> float:
        """Adjust event probability based on agent characteristics"""
        probability = base_probability
        
        # Age-based adjustments
        age = agent_data.get('age', 30)
        if event_type == LifeEventType.BIRTH_OF_CHILD:
            if 25 <= age <= 40:
                probability *= 3.0
            elif age < 20 or age > 45:
                probability *= 0.1
        
        # Role-based adjustments
        role = agent_data.get('role', '').lower()
        if 'student' in role:
            if event_type == LifeEventType.ACHIEVEMENT:
                probability *= 2.0
            if event_type == LifeEventType.JOB_LOSS:
                probability *= 0.1
        
        # Mental health-based adjustments
        mental_health = agent_data.get('mental_health', {})
        stress = mental_health.get('stress', 0.5)
        depression = mental_health.get('depression', 0.5)
        
        if stress > 0.7:
            if event_type in [LifeEventType.ILLNESS, LifeEventType.CONFLICT]:
                probability *= 1.5
        
        if depression > 0.7:
            if event_type in [LifeEventType.BREAKUP, LifeEventType.JOB_LOSS]:
                probability *= 1.3
        
        return probability
    
    def _create_event(self, event_type: LifeEventType, agent_data: Dict[str, Any]) -> LifeEvent:
        """Create a life event with description"""
        name = agent_data.get('name', 'Agent')
        role = agent_data.get('role', 'person')
        
        # Generate description based on event type
        descriptions = {
            LifeEventType.PROMOTION: f"{name} got promoted at work!",
            LifeEventType.NEW_RELATIONSHIP: f"{name} started a new relationship.",
            LifeEventType.MARRIAGE: f"{name} got married!",
            LifeEventType.BIRTH_OF_CHILD: f"{name} had a baby!",
            LifeEventType.NEW_FRIENDSHIP: f"{name} made a new friend.",
            LifeEventType.ACHIEVEMENT: f"{name} achieved a major goal.",
            LifeEventType.WINDFALL: f"{name} received unexpected money.",
            LifeEventType.RECOVERY: f"{name} recovered from a difficult period.",
            
            LifeEventType.JOB_LOSS: f"{name} lost their job.",
            LifeEventType.BREAKUP: f"{name} went through a breakup.",
            LifeEventType.DIVORCE: f"{name} got divorced.",
            LifeEventType.DEATH_OF_LOVED_ONE: f"{name} lost a loved one.",
            LifeEventType.ILLNESS: f"{name} fell ill.",
            LifeEventType.INJURY: f"{name} got injured.",
            LifeEventType.FINANCIAL_CRISIS: f"{name} faced a financial crisis.",
            LifeEventType.CONFLICT: f"{name} had a major conflict.",
            LifeEventType.BETRAYAL: f"{name} was betrayed by someone close.",
            
            LifeEventType.JOB_CHANGE: f"{name} changed jobs.",
            LifeEventType.RELOCATION: f"{name} moved to a new place.",
            LifeEventType.MAJOR_PURCHASE: f"{name} made a major purchase.",
            LifeEventType.LIFE_MILESTONE: f"{name} reached a life milestone.",
        }
        
        description = descriptions.get(event_type, f"{name} experienced {event_type.value}")
        impact = self.EVENT_IMPACTS[event_type].copy()
        
        # Add some randomness to impact
        for key in impact:
            impact[key] *= random.uniform(0.8, 1.2)
        
        # Determine duration (negative events last longer)
        if event_type.value in ['job_loss', 'divorce', 'death_of_loved_one', 'illness']:
            duration = random.randint(168, 720)  # 1 week to 1 month
        elif event_type.value in ['breakup', 'financial_crisis', 'injury']:
            duration = random.randint(72, 336)  # 3 days to 2 weeks
        else:
            duration = random.randint(24, 168)  # 1 day to 1 week
        
        severity = abs(sum(impact.values()) / len(impact))
        
        return LifeEvent(
            event_type=event_type,
            description=description,
            mental_health_impact=impact,
            duration_hours=duration,
            severity=severity
        )
