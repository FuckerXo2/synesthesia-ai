"""
Action types and definitions for daily life simulation
"""

from enum import Enum
from typing import Dict
from dataclasses import dataclass


class ActionType(Enum):
    """All possible actions agents can take"""
    
    # Morning routine
    WAKE_UP = "wake_up"
    MORNING_ROUTINE = "morning_routine"
    BREAKFAST = "breakfast"
    
    # Work/School
    GO_TO_WORK = "go_to_work"
    GO_TO_SCHOOL = "go_to_school"
    WORK = "work"
    STUDY = "study"
    ATTEND_CLASS = "attend_class"
    TAKE_BREAK = "take_break"
    SKIP_WORK = "skip_work"
    SKIP_CLASS = "skip_class"
    
    # Social interactions
    SOCIALIZE = "socialize"
    CALL_FRIEND = "call_friend"
    CALL_FAMILY = "call_family"
    FAMILY_TIME = "family_time"
    ATTEND_EVENT = "attend_event"
    MAKE_NEW_FRIEND = "make_new_friend"
    
    # Self-care (positive)
    EXERCISE = "exercise"
    MEDITATE = "meditate"
    HOBBY = "hobby"
    RELAX = "relax"
    TAKE_WALK = "take_walk"
    LISTEN_MUSIC = "listen_music"
    READ_BOOK = "read_book"
    
    # Mental health care
    SEEK_THERAPY = "seek_therapy"
    ATTEND_THERAPY = "attend_therapy"
    TAKE_MEDICATION = "take_medication"
    JOURNAL = "journal"
    REACH_OUT_FOR_HELP = "reach_out_for_help"
    JOIN_SUPPORT_GROUP = "join_support_group"
    
    # Negative coping
    ISOLATE = "isolate"
    SUBSTANCE_USE = "substance_use"
    AVOID_RESPONSIBILITIES = "avoid_responsibilities"
    RUMINATE = "ruminate"
    SELF_HARM = "self_harm"  # Serious - triggers crisis intervention
    
    # Conflict/Stress
    ARGUMENT = "argument"
    CONFLICT_AT_WORK = "conflict_at_work"
    CONFLICT_AT_HOME = "conflict_at_home"
    RECEIVE_BAD_NEWS = "receive_bad_news"
    
    # Evening routine
    DINNER = "dinner"
    EVENING_ROUTINE = "evening_routine"
    PREPARE_FOR_BED = "prepare_for_bed"
    SLEEP = "sleep"
    
    # Passive
    DO_NOTHING = "do_nothing"
    SCROLL_SOCIAL_MEDIA = "scroll_social_media"
    WATCH_TV = "watch_tv"


@dataclass
class ActionEffect:
    """Defines the mental health effects of an action"""
    anxiety_change: float = 0.0
    depression_change: float = 0.0
    stress_change: float = 0.0
    wellbeing_change: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "anxiety": self.anxiety_change,
            "depression": self.depression_change,
            "stress": self.stress_change,
            "wellbeing": self.wellbeing_change
        }


# Define mental health effects for each action
ACTION_EFFECTS: Dict[ActionType, ActionEffect] = {
    # Morning routine (slightly positive)
    ActionType.WAKE_UP: ActionEffect(wellbeing_change=0.01),
    ActionType.MORNING_ROUTINE: ActionEffect(stress_change=-0.02, wellbeing_change=0.02),
    ActionType.BREAKFAST: ActionEffect(wellbeing_change=0.03),
    
    # Work/School (neutral to stressful)
    ActionType.GO_TO_WORK: ActionEffect(stress_change=0.02),
    ActionType.GO_TO_SCHOOL: ActionEffect(anxiety_change=0.02),
    ActionType.WORK: ActionEffect(stress_change=0.05),
    ActionType.STUDY: ActionEffect(stress_change=0.04, anxiety_change=0.03),
    ActionType.ATTEND_CLASS: ActionEffect(anxiety_change=0.02),
    ActionType.TAKE_BREAK: ActionEffect(stress_change=-0.08, wellbeing_change=0.05),
    ActionType.SKIP_WORK: ActionEffect(anxiety_change=0.15, stress_change=-0.05, wellbeing_change=-0.10),
    ActionType.SKIP_CLASS: ActionEffect(anxiety_change=0.12, stress_change=-0.03, wellbeing_change=-0.08),
    
    # Social interactions (generally positive)
    ActionType.SOCIALIZE: ActionEffect(depression_change=-0.10, wellbeing_change=0.12, anxiety_change=-0.05),
    ActionType.CALL_FRIEND: ActionEffect(depression_change=-0.08, wellbeing_change=0.10),
    ActionType.CALL_FAMILY: ActionEffect(depression_change=-0.07, wellbeing_change=0.08),
    ActionType.FAMILY_TIME: ActionEffect(depression_change=-0.12, wellbeing_change=0.15, stress_change=-0.05),
    ActionType.ATTEND_EVENT: ActionEffect(anxiety_change=0.05, wellbeing_change=0.10, depression_change=-0.08),
    ActionType.MAKE_NEW_FRIEND: ActionEffect(anxiety_change=0.08, wellbeing_change=0.15, depression_change=-0.10),
    
    # Self-care (very positive)
    ActionType.EXERCISE: ActionEffect(depression_change=-0.12, anxiety_change=-0.10, stress_change=-0.08, wellbeing_change=0.15),
    ActionType.MEDITATE: ActionEffect(anxiety_change=-0.15, stress_change=-0.12, wellbeing_change=0.10),
    ActionType.HOBBY: ActionEffect(depression_change=-0.08, wellbeing_change=0.12, stress_change=-0.05),
    ActionType.RELAX: ActionEffect(stress_change=-0.10, anxiety_change=-0.08, wellbeing_change=0.08),
    ActionType.TAKE_WALK: ActionEffect(depression_change=-0.08, anxiety_change=-0.06, wellbeing_change=0.10),
    ActionType.LISTEN_MUSIC: ActionEffect(stress_change=-0.06, wellbeing_change=0.08),
    ActionType.READ_BOOK: ActionEffect(stress_change=-0.05, wellbeing_change=0.07),
    
    # Mental health care (very positive)
    ActionType.SEEK_THERAPY: ActionEffect(anxiety_change=-0.05, wellbeing_change=0.08),
    ActionType.ATTEND_THERAPY: ActionEffect(anxiety_change=-0.18, depression_change=-0.15, stress_change=-0.12, wellbeing_change=0.20),
    ActionType.TAKE_MEDICATION: ActionEffect(anxiety_change=-0.10, depression_change=-0.12),
    ActionType.JOURNAL: ActionEffect(anxiety_change=-0.08, stress_change=-0.06, wellbeing_change=0.08),
    ActionType.REACH_OUT_FOR_HELP: ActionEffect(anxiety_change=-0.12, depression_change=-0.10, wellbeing_change=0.15),
    ActionType.JOIN_SUPPORT_GROUP: ActionEffect(depression_change=-0.15, wellbeing_change=0.18, anxiety_change=-0.10),
    
    # Negative coping (harmful)
    ActionType.ISOLATE: ActionEffect(depression_change=0.12, wellbeing_change=-0.10, anxiety_change=0.05),
    ActionType.SUBSTANCE_USE: ActionEffect(stress_change=-0.05, anxiety_change=0.08, depression_change=0.10, wellbeing_change=-0.15),
    ActionType.AVOID_RESPONSIBILITIES: ActionEffect(anxiety_change=0.15, stress_change=-0.03, wellbeing_change=-0.08),
    ActionType.RUMINATE: ActionEffect(anxiety_change=0.12, depression_change=0.10, stress_change=0.08),
    ActionType.SELF_HARM: ActionEffect(depression_change=0.20, anxiety_change=0.15, wellbeing_change=-0.25),  # CRISIS
    
    # Conflict/Stress (negative)
    ActionType.ARGUMENT: ActionEffect(stress_change=0.15, anxiety_change=0.10, wellbeing_change=-0.08),
    ActionType.CONFLICT_AT_WORK: ActionEffect(stress_change=0.18, anxiety_change=0.12, wellbeing_change=-0.10),
    ActionType.CONFLICT_AT_HOME: ActionEffect(stress_change=0.20, anxiety_change=0.15, depression_change=0.08, wellbeing_change=-0.12),
    ActionType.RECEIVE_BAD_NEWS: ActionEffect(anxiety_change=0.15, stress_change=0.12, wellbeing_change=-0.10),
    
    # Evening routine (slightly positive)
    ActionType.DINNER: ActionEffect(wellbeing_change=0.03),
    ActionType.EVENING_ROUTINE: ActionEffect(stress_change=-0.05, wellbeing_change=0.05),
    ActionType.PREPARE_FOR_BED: ActionEffect(anxiety_change=-0.03, wellbeing_change=0.03),
    ActionType.SLEEP: ActionEffect(stress_change=-0.10, anxiety_change=-0.08, wellbeing_change=0.12),
    
    # Passive (slightly negative)
    ActionType.DO_NOTHING: ActionEffect(depression_change=0.05, wellbeing_change=-0.03),
    ActionType.SCROLL_SOCIAL_MEDIA: ActionEffect(anxiety_change=0.05, wellbeing_change=-0.02),
    ActionType.WATCH_TV: ActionEffect(wellbeing_change=0.02, stress_change=-0.03),
}


def get_action_effect(action_type: ActionType) -> ActionEffect:
    """Get the mental health effect of an action"""
    return ACTION_EFFECTS.get(action_type, ActionEffect())


def get_available_actions(current_hour: int, agent_state: str) -> list[ActionType]:
    """
    Get list of available actions based on time of day and agent state
    
    Args:
        current_hour: Hour of day (0-23)
        agent_state: Agent's mental health state (thriving, coping, struggling, crisis)
        
    Returns:
        List of available ActionType values
    """
    actions = []
    
    # Morning (6-9)
    if 6 <= current_hour < 9:
        actions.extend([
            ActionType.WAKE_UP,
            ActionType.MORNING_ROUTINE,
            ActionType.BREAKFAST,
            ActionType.EXERCISE,
            ActionType.MEDITATE,
        ])
    
    # Work hours (9-17)
    elif 9 <= current_hour < 17:
        actions.extend([
            ActionType.WORK,
            ActionType.STUDY,
            ActionType.ATTEND_CLASS,
            ActionType.TAKE_BREAK,
            ActionType.CALL_FRIEND,
            ActionType.SKIP_WORK,
            ActionType.SKIP_CLASS,
        ])
    
    # Evening (17-22)
    elif 17 <= current_hour < 22:
        actions.extend([
            ActionType.SOCIALIZE,
            ActionType.FAMILY_TIME,
            ActionType.EXERCISE,
            ActionType.HOBBY,
            ActionType.RELAX,
            ActionType.DINNER,
            ActionType.ATTEND_EVENT,
        ])
    
    # Night (22-24, 0-6)
    else:
        actions.extend([
            ActionType.EVENING_ROUTINE,
            ActionType.PREPARE_FOR_BED,
            ActionType.SLEEP,
            ActionType.RELAX,
            ActionType.READ_BOOK,
        ])
    
    # Always available
    actions.extend([
        ActionType.JOURNAL,
        ActionType.MEDITATE,
        ActionType.LISTEN_MUSIC,
        ActionType.SCROLL_SOCIAL_MEDIA,
        ActionType.WATCH_TV,
        ActionType.DO_NOTHING,
    ])
    
    # Mental health specific actions
    if agent_state in ["struggling", "crisis"]:
        actions.extend([
            ActionType.SEEK_THERAPY,
            ActionType.REACH_OUT_FOR_HELP,
            ActionType.CALL_FRIEND,
            ActionType.CALL_FAMILY,
        ])
    
    # Negative actions (more likely when struggling)
    if agent_state in ["struggling", "crisis"]:
        actions.extend([
            ActionType.ISOLATE,
            ActionType.AVOID_RESPONSIBILITIES,
            ActionType.RUMINATE,
            ActionType.SUBSTANCE_USE,
        ])
    
    # Crisis-specific
    if agent_state == "crisis":
        actions.append(ActionType.SELF_HARM)
    
    return list(set(actions))  # Remove duplicates
