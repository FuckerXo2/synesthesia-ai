"""
Real-Time Action System - Actions that take time and have duration
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import time


class ActionState(Enum):
    """State of an action"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"


@dataclass
class RealtimeAction:
    """An action that takes real time to complete"""
    action_type: str
    duration_seconds: float  # How long this action takes
    target_location_id: Optional[int] = None  # Where this action happens
    target_agent_id: Optional[int] = None  # Who this action is with
    
    # State
    state: ActionState = ActionState.NOT_STARTED
    start_time: Optional[float] = None
    elapsed_time: float = 0.0
    
    # Metadata
    description: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def start(self):
        """Start the action"""
        self.state = ActionState.IN_PROGRESS
        self.start_time = time.time()
        self.elapsed_time = 0.0
    
    def update(self, delta_time: float) -> bool:
        """
        Update the action
        
        Args:
            delta_time: Time elapsed since last update (seconds)
            
        Returns:
            True if action is complete
        """
        if self.state != ActionState.IN_PROGRESS:
            return self.state == ActionState.COMPLETED
        
        self.elapsed_time += delta_time
        
        if self.elapsed_time >= self.duration_seconds:
            self.state = ActionState.COMPLETED
            return True
        
        return False
    
    def interrupt(self):
        """Interrupt the action"""
        self.state = ActionState.INTERRUPTED
    
    def get_progress(self) -> float:
        """Get progress as a percentage (0.0 to 1.0)"""
        if self.duration_seconds == 0:
            return 1.0
        return min(1.0, self.elapsed_time / self.duration_seconds)
    
    def time_remaining(self) -> float:
        """Get time remaining in seconds"""
        return max(0.0, self.duration_seconds - self.elapsed_time)
    
    def is_complete(self) -> bool:
        """Check if action is complete"""
        return self.state == ActionState.COMPLETED
    
    def is_in_progress(self) -> bool:
        """Check if action is in progress"""
        return self.state == ActionState.IN_PROGRESS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "action_type": self.action_type,
            "duration_seconds": self.duration_seconds,
            "target_location_id": self.target_location_id,
            "target_agent_id": self.target_agent_id,
            "state": self.state.value,
            "elapsed_time": self.elapsed_time,
            "progress": self.get_progress(),
            "time_remaining": self.time_remaining(),
            "description": self.description,
            "metadata": self.metadata
        }


# Action duration presets (in seconds, simulation time)
ACTION_DURATIONS = {
    # Movement
    "walk_short": 60,  # 1 minute
    "walk_medium": 300,  # 5 minutes
    "walk_long": 900,  # 15 minutes
    "drive_short": 300,  # 5 minutes
    "drive_medium": 900,  # 15 minutes
    "drive_long": 1800,  # 30 minutes
    
    # Daily activities
    "wake_up": 300,  # 5 minutes
    "morning_routine": 1800,  # 30 minutes
    "breakfast": 900,  # 15 minutes
    "lunch": 1800,  # 30 minutes
    "dinner": 2400,  # 40 minutes
    "shower": 900,  # 15 minutes
    "sleep": 28800,  # 8 hours
    
    # Work/School
    "work_session": 3600,  # 1 hour
    "meeting": 1800,  # 30 minutes
    "class": 3600,  # 1 hour
    "study_session": 2700,  # 45 minutes
    
    # Social
    "conversation_short": 300,  # 5 minutes
    "conversation_medium": 900,  # 15 minutes
    "conversation_long": 1800,  # 30 minutes
    "socialize": 3600,  # 1 hour
    "date": 7200,  # 2 hours
    
    # Self-care
    "exercise": 2700,  # 45 minutes
    "meditate": 1200,  # 20 minutes
    "therapy_session": 3600,  # 1 hour
    "doctor_visit": 2700,  # 45 minutes
    
    # Entertainment
    "watch_tv": 3600,  # 1 hour
    "play_game": 3600,  # 1 hour
    "read": 1800,  # 30 minutes
    "read_book": 1800,  # 30 minutes
    "hobby": 2700,  # 45 minutes
    "relax": 1800,  # 30 minutes
    "take_walk": 1200,  # 20 minutes
    "listen_music": 1200,  # 20 minutes
    
    # Quick actions
    "phone_call": 600,  # 10 minutes
    "take_break": 900,  # 15 minutes
    "text_message": 60,  # 1 minute
    "check_phone": 180,  # 3 minutes
    "bathroom": 300,  # 5 minutes
    "snack": 300,  # 5 minutes
}


def get_action_duration(action_type: str) -> float:
    """Get the duration for an action type"""
    return ACTION_DURATIONS.get(action_type, 600)  # Default 10 minutes
