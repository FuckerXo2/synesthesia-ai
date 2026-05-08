"""
Mental health state management for agents
"""

from dataclasses import dataclass, field
from typing import Dict
from enum import Enum


class MentalHealthCategory(Enum):
    """Mental health state categories"""
    THRIVING = "thriving"  # 0.0-0.2 distress
    COPING = "coping"  # 0.2-0.4 distress
    STRUGGLING = "struggling"  # 0.4-0.6 distress
    CRISIS = "crisis"  # 0.6-1.0 distress


@dataclass
class MentalHealthState:
    """Represents an agent's mental health state"""
    anxiety: float = 0.3  # 0.0 (none) to 1.0 (severe)
    depression: float = 0.3
    stress: float = 0.3
    wellbeing: float = 0.7  # 0.0 (poor) to 1.0 (excellent)
    
    def __post_init__(self):
        """Validate values are in range [0, 1]"""
        for attr in ['anxiety', 'depression', 'stress', 'wellbeing']:
            value = getattr(self, attr)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{attr} must be between 0.0 and 1.0, got {value}")
    
    @property
    def overall_distress(self) -> float:
        """Calculate overall distress level"""
        return (self.anxiety + self.depression + self.stress) / 3
    
    @property
    def category(self) -> MentalHealthCategory:
        """Determine mental health category"""
        distress = self.overall_distress
        if distress < 0.2:
            return MentalHealthCategory.THRIVING
        elif distress < 0.4:
            return MentalHealthCategory.COPING
        elif distress < 0.6:
            return MentalHealthCategory.STRUGGLING
        else:
            return MentalHealthCategory.CRISIS
    
    def update(self, changes: Dict[str, float]):
        """
        Update mental health state with changes
        
        Args:
            changes: Dict of metric changes, e.g. {"anxiety": -0.1, "stress": 0.05}
        """
        for metric, change in changes.items():
            if hasattr(self, metric):
                current = getattr(self, metric)
                new_value = max(0.0, min(1.0, current + change))
                setattr(self, metric, new_value)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "anxiety": self.anxiety,
            "depression": self.depression,
            "stress": self.stress,
            "wellbeing": self.wellbeing,
            "overall_distress": self.overall_distress,
            "mental_health_state": self.category.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'MentalHealthState':
        """Create from dictionary"""
        return cls(
            anxiety=data.get('anxiety', 0.3),
            depression=data.get('depression', 0.3),
            stress=data.get('stress', 0.3),
            wellbeing=data.get('wellbeing', 0.7)
        )
    
    def __repr__(self) -> str:
        return (f"MentalHealthState(anxiety={self.anxiety:.2f}, "
                f"depression={self.depression:.2f}, stress={self.stress:.2f}, "
                f"wellbeing={self.wellbeing:.2f}, category={self.category.value})")
