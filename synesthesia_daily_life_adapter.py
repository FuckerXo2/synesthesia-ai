#!/usr/bin/env python3
"""
Synesthesia Daily Life Adapter
Adapts OASIS Twitter platform to simulate daily life and mental health

Instead of building a custom platform from scratch, we repurpose Twitter's
social media actions to represent daily life activities and mental health states.

MAPPING:
- CREATE_POST → Express feelings/thoughts (journaling, venting)
- LIKE_POST → Positive social interaction (support someone)
- REPOST → Share/relate to experience
- FOLLOW → Form relationship (friend, support group)
- DO_NOTHING → Isolate/withdraw
- QUOTE_POST → Seek/offer advice
- REFRESH → Check in on community
- INTERVIEW → Talk to agent (therapy session, check-in)
"""

import random
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class MentalHealthState(Enum):
    """Mental health state categories"""
    THRIVING = "thriving"  # 0.0-0.2 distress
    COPING = "coping"  # 0.2-0.4 distress
    STRUGGLING = "struggling"  # 0.4-0.6 distress
    CRISIS = "crisis"  # 0.6-1.0 distress


class LifeEvent(Enum):
    """Daily life events that affect mental health"""
    # Positive events
    GOOD_SLEEP = "good_sleep"
    EXERCISE = "exercise"
    SOCIAL_CONNECTION = "social_connection"
    THERAPY_SESSION = "therapy_session"
    ACCOMPLISHMENT = "accomplishment"
    RELAXATION = "relaxation"
    
    # Negative events
    POOR_SLEEP = "poor_sleep"
    WORK_STRESS = "work_stress"
    ACADEMIC_PRESSURE = "academic_pressure"
    CONFLICT = "conflict"
    ISOLATION = "isolation"
    FINANCIAL_STRESS = "financial_stress"
    HEALTH_ISSUE = "health_issue"
    
    # Neutral events
    ROUTINE_DAY = "routine_day"
    COMMUTE = "commute"


@dataclass
class DailyLifeAction:
    """Represents a daily life action translated to OASIS action"""
    oasis_action: str  # The OASIS ActionType to use
    content_template: str  # Template for generating post content
    mental_health_impact: Dict[str, float]  # Impact on mental health metrics
    # Example: {"anxiety": -0.1, "stress": -0.05, "wellbeing": +0.1}


class DailyLifeContentGenerator:
    """Generates realistic daily life content for agents"""
    
    # Content templates for different mental health states and activities
    CONTENT_TEMPLATES = {
        # Expressing feelings (CREATE_POST)
        "express_anxiety": [
            "Feeling really anxious about {stressor} today",
            "Can't stop worrying about {stressor}",
            "Anxiety is through the roof, {stressor} is overwhelming",
            "Having a panic attack thinking about {stressor}",
        ],
        "express_depression": [
            "Everything feels pointless today",
            "Can't find motivation to do anything",
            "Feeling really low, don't want to get out of bed",
            "The darkness is back, struggling to see hope",
        ],
        "express_stress": [
            "{stressor} is killing me right now",
            "So overwhelmed with {stressor}, can't breathe",
            "Stress levels are insane, {stressor} won't stop",
            "Drowning in {stressor}, need a break",
        ],
        "express_positive": [
            "Had a great {activity} today, feeling good!",
            "Finally feeling better after {activity}",
            "{activity} really helped, feeling hopeful",
            "Small win today: {activity}. Progress!",
        ],
        
        # Seeking help (QUOTE_POST)
        "seek_help": [
            "Has anyone dealt with {stressor}? Need advice",
            "Struggling with {stressor}, what helped you?",
            "How do you cope with {stressor}?",
            "Feeling lost with {stressor}, any suggestions?",
        ],
        
        # Offering support (LIKE_POST, QUOTE_POST)
        "offer_support": [
            "I've been there, it gets better",
            "You're not alone in this",
            "Sending you strength and support",
            "Have you tried {coping_mechanism}? It helped me",
        ],
        
        # Isolation (DO_NOTHING)
        "isolate": [
            "Just want to be alone today",
            "Can't deal with people right now",
            "Staying in bed all day",
            "Too exhausted to interact with anyone",
        ],
    }
    
    STRESSORS = [
        "work deadlines", "exams", "financial problems", "relationship issues",
        "health concerns", "family drama", "job insecurity", "loneliness",
        "academic pressure", "social anxiety", "sleep problems"
    ]
    
    ACTIVITIES = [
        "therapy session", "workout", "meditation", "walk in nature",
        "coffee with a friend", "journaling", "good night's sleep",
        "productive work day", "creative project"
    ]
    
    COPING_MECHANISMS = [
        "therapy", "meditation", "exercise", "talking to friends",
        "journaling", "deep breathing", "taking breaks", "setting boundaries"
    ]
    
    @classmethod
    def generate_content(
        cls,
        agent_profile: Dict[str, Any],
        action_type: str,
        mental_health_state: MentalHealthState
    ) -> str:
        """
        Generate realistic content based on agent's state and action
        
        Args:
            agent_profile: Agent's profile with mental health state
            action_type: Type of action (express_anxiety, seek_help, etc.)
            mental_health_state: Current mental health state
            
        Returns:
            Generated content string
        """
        templates = cls.CONTENT_TEMPLATES.get(action_type, ["Thinking about life..."])
        template = random.choice(templates)
        
        # Fill in template variables
        content = template.format(
            stressor=random.choice(agent_profile.get("stressors", cls.STRESSORS)),
            activity=random.choice(cls.ACTIVITIES),
            coping_mechanism=random.choice(cls.COPING_MECHANISMS)
        )
        
        return content
    
    @classmethod
    def determine_action_type(
        cls,
        agent_profile: Dict[str, Any],
        current_hour: int
    ) -> str:
        """
        Determine what type of action an agent should take based on their state
        
        Args:
            agent_profile: Agent's profile with mental health state
            current_hour: Current hour of day (0-23)
            
        Returns:
            Action type string (express_anxiety, seek_help, etc.)
        """
        mental_health = agent_profile.get("mental_health", {})
        anxiety = mental_health.get("anxiety", 0.3)
        depression = mental_health.get("depression", 0.3)
        stress = mental_health.get("stress", 0.3)
        wellbeing = mental_health.get("wellbeing", 0.7)
        
        # Calculate overall distress
        distress = (anxiety + depression + stress) / 3
        
        # Determine mental health state
        if distress < 0.2:
            state = MentalHealthState.THRIVING
        elif distress < 0.4:
            state = MentalHealthState.COPING
        elif distress < 0.6:
            state = MentalHealthState.STRUGGLING
        else:
            state = MentalHealthState.CRISIS
        
        # Sleep hours - more likely to isolate
        if current_hour in agent_profile.get("sleep_hours", []):
            return "isolate"
        
        # Work hours - express stress
        if current_hour in agent_profile.get("work_hours", []):
            if stress > 0.6:
                return "express_stress"
            elif random.random() < 0.3:
                return "express_positive"
        
        # Decision tree based on mental health state
        if state == MentalHealthState.CRISIS:
            # Crisis: 60% seek help, 30% express distress, 10% isolate
            return random.choices(
                ["seek_help", "express_anxiety", "express_depression", "isolate"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        
        elif state == MentalHealthState.STRUGGLING:
            # Struggling: mix of expressing and seeking help
            return random.choices(
                ["express_anxiety", "express_stress", "seek_help", "express_positive"],
                weights=[0.3, 0.3, 0.3, 0.1]
            )[0]
        
        elif state == MentalHealthState.COPING:
            # Coping: more balanced
            return random.choices(
                ["express_positive", "offer_support", "express_stress", "seek_help"],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
        
        else:  # THRIVING
            # Thriving: mostly positive and supportive
            return random.choices(
                ["express_positive", "offer_support", "express_positive"],
                weights=[0.5, 0.4, 0.1]
            )[0]


class DailyLifeActionMapper:
    """Maps daily life actions to OASIS Twitter actions"""
    
    ACTION_MAPPING = {
        # Expressing feelings
        "express_anxiety": DailyLifeAction(
            oasis_action="CREATE_POST",
            content_template="anxiety",
            mental_health_impact={"anxiety": -0.05, "stress": -0.02}  # Venting helps a bit
        ),
        "express_depression": DailyLifeAction(
            oasis_action="CREATE_POST",
            content_template="depression",
            mental_health_impact={"depression": -0.03}
        ),
        "express_stress": DailyLifeAction(
            oasis_action="CREATE_POST",
            content_template="stress",
            mental_health_impact={"stress": -0.05}
        ),
        "express_positive": DailyLifeAction(
            oasis_action="CREATE_POST",
            content_template="positive",
            mental_health_impact={"wellbeing": +0.05, "anxiety": -0.02}
        ),
        
        # Seeking help
        "seek_help": DailyLifeAction(
            oasis_action="QUOTE_POST",  # Quote someone else's post to ask for advice
            content_template="seek_help",
            mental_health_impact={"anxiety": -0.1, "wellbeing": +0.05}  # Asking helps
        ),
        
        # Offering support
        "offer_support": DailyLifeAction(
            oasis_action="LIKE_POST",  # Like = show support
            content_template="offer_support",
            mental_health_impact={"wellbeing": +0.08, "depression": -0.05}  # Helping others helps you
        ),
        
        # Social connection
        "connect": DailyLifeAction(
            oasis_action="FOLLOW",  # Follow = form relationship
            content_template="connect",
            mental_health_impact={"wellbeing": +0.1, "depression": -0.08}
        ),
        
        # Isolation
        "isolate": DailyLifeAction(
            oasis_action="DO_NOTHING",
            content_template="isolate",
            mental_health_impact={"depression": +0.05, "anxiety": +0.03, "wellbeing": -0.05}
        ),
    }
    
    @classmethod
    def get_oasis_action(cls, daily_life_action: str) -> DailyLifeAction:
        """Get the OASIS action mapping for a daily life action"""
        return cls.ACTION_MAPPING.get(
            daily_life_action,
            cls.ACTION_MAPPING["express_positive"]  # Default
        )


class MentalHealthSimulator:
    """Simulates mental health changes over time"""
    
    @staticmethod
    def update_mental_health(
        current_state: Dict[str, float],
        action_impact: Dict[str, float],
        life_events: List[LifeEvent],
        time_decay: float = 0.01
    ) -> Dict[str, float]:
        """
        Update mental health state based on actions and events
        
        Args:
            current_state: Current mental health metrics
            action_impact: Impact from the action taken
            life_events: Life events that occurred this round
            time_decay: Natural decay/recovery rate per round
            
        Returns:
            Updated mental health state
        """
        new_state = current_state.copy()
        
        # Apply action impact
        for metric, impact in action_impact.items():
            new_state[metric] = new_state.get(metric, 0.5) + impact
        
        # Apply life events
        event_impacts = {
            # Positive events
            LifeEvent.GOOD_SLEEP: {"anxiety": -0.05, "stress": -0.05, "wellbeing": +0.05},
            LifeEvent.EXERCISE: {"depression": -0.08, "anxiety": -0.06, "wellbeing": +0.1},
            LifeEvent.SOCIAL_CONNECTION: {"depression": -0.1, "wellbeing": +0.12},
            LifeEvent.THERAPY_SESSION: {"anxiety": -0.15, "depression": -0.12, "wellbeing": +0.15},
            LifeEvent.ACCOMPLISHMENT: {"wellbeing": +0.1, "stress": -0.05},
            LifeEvent.RELAXATION: {"stress": -0.1, "anxiety": -0.08},
            
            # Negative events
            LifeEvent.POOR_SLEEP: {"anxiety": +0.08, "stress": +0.06, "wellbeing": -0.05},
            LifeEvent.WORK_STRESS: {"stress": +0.12, "anxiety": +0.08},
            LifeEvent.ACADEMIC_PRESSURE: {"stress": +0.15, "anxiety": +0.12},
            LifeEvent.CONFLICT: {"stress": +0.1, "anxiety": +0.08, "depression": +0.05},
            LifeEvent.ISOLATION: {"depression": +0.12, "wellbeing": -0.1},
            LifeEvent.FINANCIAL_STRESS: {"stress": +0.15, "anxiety": +0.12, "wellbeing": -0.08},
            LifeEvent.HEALTH_ISSUE: {"anxiety": +0.15, "stress": +0.1, "wellbeing": -0.12},
        }
        
        for event in life_events:
            impact = event_impacts.get(event, {})
            for metric, change in impact.items():
                new_state[metric] = new_state.get(metric, 0.5) + change
        
        # Natural recovery/decay (things slowly get better or worse)
        # High distress slowly decreases, low distress slowly increases (regression to mean)
        for metric in ["anxiety", "depression", "stress"]:
            current_val = new_state.get(metric, 0.5)
            if current_val > 0.5:
                new_state[metric] = current_val - time_decay  # Recovery
            else:
                new_state[metric] = current_val + time_decay * 0.5  # Slow increase
        
        # Wellbeing regresses to mean
        wellbeing = new_state.get("wellbeing", 0.5)
        if wellbeing > 0.5:
            new_state["wellbeing"] = wellbeing - time_decay * 0.5
        else:
            new_state["wellbeing"] = wellbeing + time_decay
        
        # Clamp values between 0 and 1
        for metric in new_state:
            new_state[metric] = max(0.0, min(1.0, new_state[metric]))
        
        return new_state
    
    @staticmethod
    def generate_life_events(
        agent_profile: Dict[str, Any],
        current_hour: int
    ) -> List[LifeEvent]:
        """
        Generate random life events based on agent profile and time
        
        Args:
            agent_profile: Agent's profile
            current_hour: Current hour of day
            
        Returns:
            List of life events that occurred
        """
        events = []
        
        # Sleep quality
        if current_hour in agent_profile.get("sleep_hours", []):
            if random.random() < 0.7:
                events.append(LifeEvent.GOOD_SLEEP)
            else:
                events.append(LifeEvent.POOR_SLEEP)
        
        # Work/school stress
        if current_hour in agent_profile.get("work_hours", []):
            stressors = agent_profile.get("stressors", [])
            if "work_stress" in stressors or "work_pressure" in stressors:
                if random.random() < 0.4:
                    events.append(LifeEvent.WORK_STRESS)
            if "academic_pressure" in stressors:
                if random.random() < 0.5:
                    events.append(LifeEvent.ACADEMIC_PRESSURE)
        
        # Random events
        if random.random() < 0.1:
            events.append(random.choice([
                LifeEvent.SOCIAL_CONNECTION,
                LifeEvent.CONFLICT,
                LifeEvent.ACCOMPLISHMENT,
                LifeEvent.RELAXATION
            ]))
        
        # Therapy (if agent has access and willingness)
        if agent_profile.get("therapy_access") and random.random() < agent_profile.get("therapy_willingness", 0.3) * 0.1:
            events.append(LifeEvent.THERAPY_SESSION)
        
        return events


def main():
    """Example usage"""
    print("="*60)
    print("🧠 SYNESTHESIA DAILY LIFE ADAPTER")
    print("="*60)
    print()
    
    # Example agent profile
    agent_profile = {
        "agent_id": 42,
        "name": "Sarah Chen",
        "role": "student",
        "mental_health": {
            "anxiety": 0.65,
            "depression": 0.35,
            "stress": 0.75,
            "wellbeing": 0.40
        },
        "stressors": ["academic_pressure", "financial_stress", "social_anxiety"],
        "work_hours": list(range(9, 17)),
        "sleep_hours": list(range(0, 7)),
        "therapy_access": True,
        "therapy_willingness": 0.6
    }
    
    print(f"👤 Agent: {agent_profile['name']}")
    print(f"   Role: {agent_profile['role']}")
    print(f"   Mental Health:")
    for metric, value in agent_profile["mental_health"].items():
        print(f"     {metric}: {value:.2f}")
    print()
    
    # Simulate a day
    print("📅 Simulating 24 hours...")
    print()
    
    for hour in range(24):
        # Determine action
        action_type = DailyLifeContentGenerator.determine_action_type(
            agent_profile, hour
        )
        
        # Generate content
        content = DailyLifeContentGenerator.generate_content(
            agent_profile, action_type, MentalHealthState.STRUGGLING
        )
        
        # Get OASIS action mapping
        daily_action = DailyLifeActionMapper.get_oasis_action(action_type)
        
        # Generate life events
        life_events = MentalHealthSimulator.generate_life_events(
            agent_profile, hour
        )
        
        # Update mental health
        agent_profile["mental_health"] = MentalHealthSimulator.update_mental_health(
            agent_profile["mental_health"],
            daily_action.mental_health_impact,
            life_events
        )
        
        # Print activity
        if hour % 4 == 0:  # Print every 4 hours
            print(f"⏰ Hour {hour:02d}:00")
            print(f"   Action: {action_type} → {daily_action.oasis_action}")
            print(f"   Content: \"{content}\"")
            if life_events:
                print(f"   Events: {', '.join([e.value for e in life_events])}")
            print(f"   Mental Health: Anxiety={agent_profile['mental_health']['anxiety']:.2f}, "
                  f"Depression={agent_profile['mental_health']['depression']:.2f}")
            print()
    
    print("="*60)
    print("✅ Daily simulation complete!")
    print()
    print("Final Mental Health State:")
    for metric, value in agent_profile["mental_health"].items():
        print(f"  {metric}: {value:.2f}")


if __name__ == "__main__":
    main()
