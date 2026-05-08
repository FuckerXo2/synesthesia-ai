"""
Agent Brain - LLM-powered decision making and consciousness
This is what makes agents ALIVE instead of just following rules
"""

import json
import random
import time
from typing import Dict, Any, List, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

from synesthesia.actions.types import ActionType

load_dotenv()


class AgentBrain:
    """
    The consciousness of an agent - uses LLM to make decisions
    based on personality, mental health, memories, and relationships
    
    Supports multiple models for load balancing
    """
    
    # Available models for load balancing
    AVAILABLE_MODELS = [
        "qwen/qwen3.5-122b-a10b",
        "meta/llama-3.3-70b-instruct",
        "mistralai/mistral-large",
        "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    ]
    
    def __init__(
        self, 
        api_key: str = None, 
        base_url: str = None, 
        model: str = None,
        use_load_balancing: bool = True
    ):
        self.client = OpenAI(
            api_key=api_key or os.getenv("LLM_API_KEY"),
            base_url=base_url or os.getenv("LLM_BASE_URL")
        )
        self.default_model = model or os.getenv("LLM_MODEL_NAME", "qwen/qwen3.5-122b-a10b")
        self.use_load_balancing = use_load_balancing
        self.model_index = 0  # For round-robin
    
    def _get_next_model(self) -> str:
        """Get next model for load balancing (round-robin)"""
        if not self.use_load_balancing:
            return self.default_model
        
        model = self.AVAILABLE_MODELS[self.model_index % len(self.AVAILABLE_MODELS)]
        self.model_index += 1
        return model
    
    def _rate_limit(self):
        """Add small delay to avoid rate limits"""
        time.sleep(random.uniform(0.1, 0.3))
    
    def decide_action(
        self,
        agent_context: Dict[str, Any],
        available_actions: List[ActionType],
        current_hour: int,
        recent_events: List[str] = None
    ) -> ActionType:
        """
        Agent decides what to do based on their full context
        
        Args:
            agent_context: Full agent state (personality, mental health, etc.)
            available_actions: List of actions they can take
            current_hour: Current hour of day
            recent_events: Recent things that happened to them
            
        Returns:
            Chosen ActionType
        """
        
        # Build the prompt with full agent context
        prompt = self._build_decision_prompt(
            agent_context,
            available_actions,
            current_hour,
            recent_events or []
        )
        
        try:
            model = self._get_next_model()
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are simulating a person's decision-making process. Think about what this person would realistically do given their personality, mental state, and current situation. Return only the action name."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Higher temp for more varied behavior
                max_tokens=50,
                timeout=30  # 30 second timeout
            )
            
            action_name = response.choices[0].message.content.strip().lower()
            
            # Map response to ActionType
            for action in available_actions:
                if action.value.lower() in action_name or action_name in action.value.lower():
                    return action
            
            # Fallback: return first available action
            return available_actions[0] if available_actions else ActionType.DO_NOTHING
            
        except Exception as e:
            print(f"LLM decision error: {e}")
            # Fallback to first available action
            return available_actions[0] if available_actions else ActionType.DO_NOTHING
    
    def _build_decision_prompt(
        self,
        agent_context: Dict[str, Any],
        available_actions: List[ActionType],
        current_hour: int,
        recent_events: List[str]
    ) -> str:
        """Build a detailed prompt for the agent's decision"""
        
        mental_health = agent_context.get("mental_health", {})
        
        prompt = f"""You are {agent_context['name']}, a {agent_context['age']}-year-old {agent_context['role']}.

**Your Personality:**
{', '.join(agent_context.get('personality_traits', []))}

**Your Current Mental State:**
- Anxiety: {mental_health.get('anxiety', 0):.2f}/1.0 {"(HIGH)" if mental_health.get('anxiety', 0) > 0.7 else ""}
- Depression: {mental_health.get('depression', 0):.2f}/1.0 {"(HIGH)" if mental_health.get('depression', 0) > 0.7 else ""}
- Stress: {mental_health.get('stress', 0):.2f}/1.0 {"(HIGH)" if mental_health.get('stress', 0) > 0.7 else ""}
- Wellbeing: {mental_health.get('wellbeing', 0):.2f}/1.0 {"(LOW)" if mental_health.get('wellbeing', 0) < 0.3 else ""}
- Overall: {mental_health.get('category', 'unknown')}

**Current Situation:**
- Time: {self._format_hour(current_hour)}
- Recent events: {', '.join(recent_events[-5:]) if recent_events else 'Nothing notable'}

**What you can do right now:**
{self._format_actions(available_actions)}

Based on who you are, how you're feeling, and what's happening, what would you do?
Reply with ONLY the action name, nothing else."""

        return prompt
    
    def _format_hour(self, hour: int) -> str:
        """Format hour as human-readable time"""
        if 0 <= hour < 6:
            return f"{hour}:00 AM (late night/early morning)"
        elif 6 <= hour < 12:
            return f"{hour}:00 AM (morning)"
        elif hour == 12:
            return "12:00 PM (noon)"
        elif 12 < hour < 18:
            return f"{hour-12}:00 PM (afternoon)"
        else:
            return f"{hour-12}:00 PM (evening)"
    
    def _format_actions(self, actions: List[ActionType]) -> str:
        """Format available actions as a readable list"""
        return '\n'.join([f"- {action.value}" for action in actions])
    
    def generate_conversation(
        self,
        agent1_context: Dict[str, Any],
        agent2_context: Dict[str, Any],
        relationship: str = "friend",
        topic: str = None
    ) -> Dict[str, Any]:
        """
        Generate a conversation between two agents
        
        Args:
            agent1_context: First agent's context
            agent2_context: Second agent's context
            relationship: Type of relationship (friend, family, colleague)
            topic: Optional conversation topic
            
        Returns:
            Dict with conversation details and mental health impacts
        """
        
        prompt = f"""Generate a realistic conversation between two people:

**Person 1: {agent1_context['name']}**
- Role: {agent1_context['role']}
- Personality: {', '.join(agent1_context.get('personality_traits', []))}
- Mental state: {agent1_context['mental_health'].get('category', 'unknown')}
- Anxiety: {agent1_context['mental_health'].get('anxiety', 0):.2f}
- Depression: {agent1_context['mental_health'].get('depression', 0):.2f}

**Person 2: {agent2_context['name']}**
- Role: {agent2_context['role']}
- Personality: {', '.join(agent2_context.get('personality_traits', []))}
- Mental state: {agent2_context['mental_health'].get('category', 'unknown')}
- Anxiety: {agent2_context['mental_health'].get('anxiety', 0):.2f}
- Depression: {agent2_context['mental_health'].get('depression', 0):.2f}

**Relationship:** {relationship}
{f"**Topic:** {topic}" if topic else ""}

Generate a brief, realistic conversation (3-4 exchanges) that reflects their personalities and mental states.
Then analyze how this conversation affects each person's mental health.

Return as JSON:
{{
  "conversation": [
    {{"speaker": "name", "text": "what they said"}},
    ...
  ],
  "summary": "brief summary of what happened",
  "impact_agent1": {{
    "anxiety_change": -0.1 to 0.1,
    "depression_change": -0.1 to 0.1,
    "stress_change": -0.1 to 0.1,
    "wellbeing_change": -0.1 to 0.1
  }},
  "impact_agent2": {{
    "anxiety_change": -0.1 to 0.1,
    "depression_change": -0.1 to 0.1,
    "stress_change": -0.1 to 0.1,
    "wellbeing_change": -0.1 to 0.1
  }},
  "relationship_change": -0.1 to 0.1
}}"""

        try:
            model = self._get_next_model()
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a psychologist simulating realistic human interactions. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Conversation generation error: {e}")
            # Fallback: generic positive interaction
            return {
                "conversation": [
                    {"speaker": agent1_context['name'], "text": "Hey, how are you doing?"},
                    {"speaker": agent2_context['name'], "text": "I'm okay, thanks for asking."}
                ],
                "summary": "Brief friendly exchange",
                "impact_agent1": {
                    "anxiety_change": -0.02,
                    "depression_change": 0,
                    "stress_change": -0.01,
                    "wellbeing_change": 0.02
                },
                "impact_agent2": {
                    "anxiety_change": -0.02,
                    "depression_change": 0,
                    "stress_change": -0.01,
                    "wellbeing_change": 0.02
                },
                "relationship_change": 0.01
            }
    
    def generate_internal_monologue(
        self,
        agent_context: Dict[str, Any],
        recent_events: List[str]
    ) -> str:
        """
        Generate agent's internal thoughts
        Useful for interviews and understanding their state
        
        Args:
            agent_context: Agent's full context
            recent_events: Recent things that happened
            
        Returns:
            Internal monologue text
        """
        
        prompt = f"""You are {agent_context['name']}, thinking to yourself.

**About you:**
- {agent_context['age']}-year-old {agent_context['role']}
- Personality: {', '.join(agent_context.get('personality_traits', []))}
- Mental state: {agent_context['mental_health'].get('category', 'unknown')}

**What's been happening:**
{chr(10).join(f"- {event}" for event in recent_events[-10:])}

**How you're feeling:**
- Anxiety: {agent_context['mental_health'].get('anxiety', 0):.2f}/1.0
- Depression: {agent_context['mental_health'].get('depression', 0):.2f}/1.0
- Stress: {agent_context['mental_health'].get('stress', 0):.2f}/1.0
- Wellbeing: {agent_context['mental_health'].get('wellbeing', 0):.2f}/1.0

Write a brief internal monologue (2-3 sentences) about how you're feeling and what you're thinking about.
Be authentic to your personality and mental state."""

        try:
            model = self._get_next_model()
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are simulating a person's internal thoughts. Be authentic and realistic."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Monologue generation error: {e}")
            return f"I'm feeling {agent_context['mental_health'].get('category', 'okay')} right now."
