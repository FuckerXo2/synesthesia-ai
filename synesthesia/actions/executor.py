"""
Action executor - handles action execution and effects
"""

import random
from typing import Dict, Any, Optional
from datetime import datetime

from synesthesia.agent.agent import Agent
from synesthesia.actions.types import ActionType, get_action_effect, get_available_actions


class ActionExecutor:
    """Executes actions and applies their effects"""
    
    def __init__(self, db=None):
        """
        Initialize action executor
        
        Args:
            db: Database instance for logging
        """
        self.db = db
    
    def execute_action(
        self,
        agent: Agent,
        action_type: ActionType,
        current_hour: int,
        simulated_time: str,
        action_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute an action and apply its effects
        
        Args:
            agent: Agent performing the action
            action_type: Type of action to perform
            current_hour: Current hour of day
            simulated_time: Human-readable simulated time
            action_details: Additional action-specific details
            
        Returns:
            Dict with action result and effects
        """
        # Get action effect
        effect = get_action_effect(action_type)
        
        # Apply mental health changes
        agent.update_mental_health(effect.to_dict())
        
        # Add to agent's recent actions
        agent.add_recent_action(f"{action_type.value} at {simulated_time}")
        
        # Generate action description
        description = self._generate_action_description(agent, action_type, action_details)
        
        # Log to database if available
        if self.db:
            self.db.insert_action({
                "agent_id": agent.agent_id,
                "timestamp": datetime.now(),
                "simulated_time": simulated_time,
                "action_type": action_type.value,
                "action_details": action_details or {},
                "mental_health_impact": effect.to_dict(),
                "success": True
            })
            
            # Log mental health state
            self.db.insert_mental_health_state({
                "agent_id": agent.agent_id,
                "timestamp": datetime.now(),
                "simulated_time": simulated_time,
                **agent.mental_health.to_dict()
            })
        
        # Check for crisis intervention
        crisis_triggered = False
        if action_type == ActionType.SELF_HARM or agent.is_in_crisis:
            crisis_triggered = True
            self._trigger_crisis_intervention(agent, simulated_time)
        
        return {
            "success": True,
            "action_type": action_type.value,
            "description": description,
            "mental_health_impact": effect.to_dict(),
            "new_mental_health": agent.mental_health.to_dict(),
            "crisis_triggered": crisis_triggered
        }
    
    def _generate_action_description(
        self,
        agent: Agent,
        action_type: ActionType,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a human-readable description of the action"""
        
        descriptions = {
            ActionType.WAKE_UP: f"{agent.name} wakes up",
            ActionType.MORNING_ROUTINE: f"{agent.name} goes through their morning routine",
            ActionType.BREAKFAST: f"{agent.name} has breakfast",
            ActionType.GO_TO_WORK: f"{agent.name} heads to work",
            ActionType.GO_TO_SCHOOL: f"{agent.name} goes to school",
            ActionType.WORK: f"{agent.name} is working",
            ActionType.STUDY: f"{agent.name} is studying",
            ActionType.ATTEND_CLASS: f"{agent.name} attends class",
            ActionType.TAKE_BREAK: f"{agent.name} takes a break",
            ActionType.SKIP_WORK: f"{agent.name} skips work (feeling overwhelmed)",
            ActionType.SKIP_CLASS: f"{agent.name} skips class (too anxious)",
            ActionType.SOCIALIZE: f"{agent.name} socializes with friends",
            ActionType.CALL_FRIEND: f"{agent.name} calls a friend",
            ActionType.CALL_FAMILY: f"{agent.name} calls family",
            ActionType.FAMILY_TIME: f"{agent.name} spends time with family",
            ActionType.ATTEND_EVENT: f"{agent.name} attends a social event",
            ActionType.MAKE_NEW_FRIEND: f"{agent.name} makes a new friend",
            ActionType.EXERCISE: f"{agent.name} exercises",
            ActionType.MEDITATE: f"{agent.name} meditates",
            ActionType.HOBBY: f"{agent.name} works on a hobby",
            ActionType.RELAX: f"{agent.name} relaxes",
            ActionType.TAKE_WALK: f"{agent.name} takes a walk",
            ActionType.LISTEN_MUSIC: f"{agent.name} listens to music",
            ActionType.READ_BOOK: f"{agent.name} reads a book",
            ActionType.SEEK_THERAPY: f"{agent.name} seeks therapy",
            ActionType.ATTEND_THERAPY: f"{agent.name} attends therapy session",
            ActionType.TAKE_MEDICATION: f"{agent.name} takes medication",
            ActionType.JOURNAL: f"{agent.name} writes in journal",
            ActionType.REACH_OUT_FOR_HELP: f"{agent.name} reaches out for help",
            ActionType.JOIN_SUPPORT_GROUP: f"{agent.name} joins a support group",
            ActionType.ISOLATE: f"{agent.name} isolates themselves",
            ActionType.SUBSTANCE_USE: f"{agent.name} uses substances to cope",
            ActionType.AVOID_RESPONSIBILITIES: f"{agent.name} avoids responsibilities",
            ActionType.RUMINATE: f"{agent.name} ruminates on negative thoughts",
            ActionType.SELF_HARM: f"{agent.name} engages in self-harm (CRISIS)",
            ActionType.ARGUMENT: f"{agent.name} has an argument",
            ActionType.CONFLICT_AT_WORK: f"{agent.name} has conflict at work",
            ActionType.CONFLICT_AT_HOME: f"{agent.name} has conflict at home",
            ActionType.RECEIVE_BAD_NEWS: f"{agent.name} receives bad news",
            ActionType.DINNER: f"{agent.name} has dinner",
            ActionType.EVENING_ROUTINE: f"{agent.name} does evening routine",
            ActionType.PREPARE_FOR_BED: f"{agent.name} prepares for bed",
            ActionType.SLEEP: f"{agent.name} sleeps",
            ActionType.DO_NOTHING: f"{agent.name} does nothing",
            ActionType.SCROLL_SOCIAL_MEDIA: f"{agent.name} scrolls social media",
            ActionType.WATCH_TV: f"{agent.name} watches TV",
        }
        
        return descriptions.get(action_type, f"{agent.name} performs {action_type.value}")
    
    def _trigger_crisis_intervention(self, agent: Agent, simulated_time: str):
        """Trigger crisis intervention for agent"""
        if self.db:
            # Log crisis event
            self.db.insert_life_event({
                "agent_id": agent.agent_id,
                "timestamp": datetime.now(),
                "simulated_time": simulated_time,
                "event_type": "crisis_intervention",
                "event_details": {
                    "reason": "Mental health crisis detected",
                    "mental_health": agent.mental_health.to_dict()
                },
                "mental_health_impact": {}
            })
        
        # In a real system, this would trigger:
        # - Emergency services notification
        # - Therapist contact
        # - Family notification
        # - Crisis hotline information
        print(f"⚠️  CRISIS INTERVENTION: {agent.name} needs immediate help!")
    
    def choose_action(
        self,
        agent: Agent,
        current_hour: int,
        use_llm: bool = False,
        llm_client = None
    ) -> ActionType:
        """
        Choose an action for the agent to take
        
        Args:
            agent: Agent making the decision
            current_hour: Current hour of day
            use_llm: Whether to use LLM for decision-making
            llm_client: LLM client instance (if use_llm=True)
            
        Returns:
            Chosen ActionType
        """
        # Get available actions
        available = get_available_actions(
            current_hour,
            agent.mental_health.category.value
        )
        
        if use_llm and llm_client:
            # Use LLM to make intelligent decision
            return self._choose_action_with_llm(agent, available, current_hour, llm_client)
        else:
            # Use rule-based decision making
            return self._choose_action_rule_based(agent, available, current_hour)
    
    def _choose_action_rule_based(
        self,
        agent: Agent,
        available_actions: list[ActionType],
        current_hour: int
    ) -> ActionType:
        """
        Rule-based action selection (fast, no LLM needed)
        
        Uses heuristics based on:
        - Time of day
        - Mental health state
        - Agent schedule
        - Personality traits
        """
        state = agent.mental_health.category.value
        
        # Sleep time
        if current_hour in agent.sleep_hours:
            if ActionType.SLEEP in available_actions:
                return ActionType.SLEEP
            return ActionType.PREPARE_FOR_BED
        
        # Morning
        if 6 <= current_hour < 9:
            if random.random() < 0.7:
                return random.choice([
                    ActionType.WAKE_UP,
                    ActionType.MORNING_ROUTINE,
                    ActionType.BREAKFAST,
                    ActionType.EXERCISE
                ])
        
        # Work/School hours
        if current_hour in agent.work_hours:
            # Crisis: likely to skip
            if state == "crisis" and random.random() < 0.6:
                return random.choice([ActionType.SKIP_WORK, ActionType.SKIP_CLASS, ActionType.ISOLATE])
            
            # Struggling: might skip
            if state == "struggling" and random.random() < 0.3:
                return random.choice([ActionType.SKIP_WORK, ActionType.SKIP_CLASS])
            
            # Normal work
            if random.random() < 0.8:
                return random.choice([ActionType.WORK, ActionType.STUDY, ActionType.ATTEND_CLASS])
            else:
                return ActionType.TAKE_BREAK
        
        # Free time - depends on mental health state
        if state == "crisis":
            # Crisis: 50% negative coping, 30% seek help, 20% isolate
            weights = {
                "negative": 0.5,
                "help": 0.3,
                "isolate": 0.2
            }
            choice = random.choices(
                ["negative", "help", "isolate"],
                weights=[weights["negative"], weights["help"], weights["isolate"]]
            )[0]
            
            if choice == "negative":
                return random.choice([
                    ActionType.SUBSTANCE_USE,
                    ActionType.RUMINATE,
                    ActionType.AVOID_RESPONSIBILITIES
                ])
            elif choice == "help":
                return random.choice([
                    ActionType.REACH_OUT_FOR_HELP,
                    ActionType.SEEK_THERAPY,
                    ActionType.CALL_FRIEND,
                    ActionType.CALL_FAMILY
                ])
            else:
                return ActionType.ISOLATE
        
        elif state == "struggling":
            # Struggling: mix of coping and some negative
            if random.random() < 0.4:
                # Positive coping
                return random.choice([
                    ActionType.EXERCISE,
                    ActionType.MEDITATE,
                    ActionType.JOURNAL,
                    ActionType.CALL_FRIEND,
                    ActionType.RELAX
                ])
            elif random.random() < 0.7:
                # Neutral
                return random.choice([
                    ActionType.HOBBY,
                    ActionType.WATCH_TV,
                    ActionType.LISTEN_MUSIC,
                    ActionType.DO_NOTHING
                ])
            else:
                # Negative
                return random.choice([
                    ActionType.ISOLATE,
                    ActionType.RUMINATE,
                    ActionType.SCROLL_SOCIAL_MEDIA
                ])
        
        elif state == "coping":
            # Coping: mostly positive with some neutral
            if random.random() < 0.6:
                return random.choice([
                    ActionType.SOCIALIZE,
                    ActionType.EXERCISE,
                    ActionType.HOBBY,
                    ActionType.RELAX,
                    ActionType.FAMILY_TIME
                ])
            else:
                return random.choice([
                    ActionType.WATCH_TV,
                    ActionType.LISTEN_MUSIC,
                    ActionType.READ_BOOK
                ])
        
        else:  # thriving
            # Thriving: mostly positive and social
            return random.choice([
                ActionType.SOCIALIZE,
                ActionType.EXERCISE,
                ActionType.HOBBY,
                ActionType.ATTEND_EVENT,
                ActionType.FAMILY_TIME,
                ActionType.MAKE_NEW_FRIEND
            ])
    
    def _choose_action_with_llm(
        self,
        agent: Agent,
        available_actions: list[ActionType],
        current_hour: int,
        llm_client
    ) -> ActionType:
        """
        Use LLM to choose action (agents think for themselves!)
        """
        # Build agent context for LLM
        agent_context = {
            "name": agent.name,
            "age": agent.age,
            "role": agent.role,
            "personality_traits": agent.personality_traits,
            "mental_health": agent.mental_health.to_dict()
        }
        
        # Get recent actions as context
        recent_events = agent.recent_actions[-10:] if hasattr(agent, 'recent_actions') else []
        
        # Let the agent's brain decide
        return llm_client.decide_action(
            agent_context,
            available_actions,
            current_hour,
            recent_events
        )
