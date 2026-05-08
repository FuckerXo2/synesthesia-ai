"""
Identity Generator - LLM creates unique backstories and identities for agents
"""

import json
from typing import Dict, Any, List
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

from synesthesia.agent.identity import AgentIdentity

load_dotenv()


class IdentityGenerator:
    """
    Generates unique identities for agents using LLM
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize identity generator
        
        Args:
            llm_client: OpenAI client (or creates new one)
        """
        if llm_client:
            self.llm = llm_client
        else:
            self.llm = OpenAI(
                api_key=os.getenv("LLM_API_KEY"),
                base_url=os.getenv("LLM_BASE_URL")
            )
        
        self.model = os.getenv("LLM_MODEL_NAME", "qwen/qwen3.5-122b-a10b")
    
    def generate_identity(
        self,
        agent_id: int,
        name: str,
        age: int,
        role: str,
        personality_traits: List[str],
        society_context: str = ""
    ) -> AgentIdentity:
        """
        Generate a unique identity for an agent
        
        Args:
            agent_id: Agent ID
            name: Agent's name
            age: Agent's age
            role: Agent's role in society
            personality_traits: Existing personality traits
            society_context: Context about the society they live in
            
        Returns:
            AgentIdentity with backstory, values, fears, goals, etc.
        """
        
        prompt = f"""You are creating a unique individual for a life simulation.

**Person:**
- Name: {name}
- Age: {age}
- Role: {role}
- Personality: {', '.join(personality_traits)}

**Society Context:**
{society_context if society_context else "Modern society"}

Create a deep, realistic identity for this person. Think about:
- What shaped them? (backstory)
- What matters most to them? (values)
- What keeps them up at night? (fears)
- What do they want? (goals)
- How do they handle stress? (coping mechanisms)
- What makes them memorable? (quirks)

Make them feel REAL. Give them depth, contradictions, struggles.

Return as JSON:
{{
  "backstory": "2-3 sentences about their past that shaped who they are",
  "values": ["value1", "value2", "value3"],
  "fears": ["fear1", "fear2", "fear3"],
  "goals": ["goal1", "goal2", "goal3"],
  "coping_mechanisms": ["coping1", "coping2", "coping3"],
  "quirks": ["quirk1", "quirk2", "quirk3"]
}}

Be specific and realistic!"""

        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a character designer creating deep, realistic individuals. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Higher temp for creativity
                response_format={"type": "json_object"},
                timeout=30
            )
            
            identity_data = json.loads(response.choices[0].message.content)
            
            # Create AgentIdentity
            identity = AgentIdentity(
                agent_id=agent_id,
                backstory=identity_data.get('backstory', ''),
                values=identity_data.get('values', []),
                fears=identity_data.get('fears', []),
                goals=identity_data.get('goals', []),
                coping_mechanisms=identity_data.get('coping_mechanisms', []),
                quirks=identity_data.get('quirks', []),
                generated_at=datetime.now()
            )
            
            return identity
            
        except Exception as e:
            print(f"⚠️  Could not generate identity for {name}: {e}")
            # Fallback to generic identity
            return self._generate_fallback_identity(agent_id, name, age, role, personality_traits)
    
    def _generate_fallback_identity(
        self,
        agent_id: int,
        name: str,
        age: int,
        role: str,
        personality_traits: List[str]
    ) -> AgentIdentity:
        """Generate a basic identity if LLM fails"""
        
        # Generic backstory based on role
        backstory_templates = {
            "engineer": f"{name} has been working in tech for {max(1, age - 22)} years. Passionate about solving problems but struggles with work-life balance.",
            "student": f"{name} is studying hard to build a better future. Feels pressure to succeed but also wants to enjoy life.",
            "parent": f"{name} is dedicated to their family. Balances work and parenting, often putting others' needs before their own.",
            "worker": f"{name} works hard to make ends meet. Dreams of a better life but faces daily challenges.",
        }
        
        backstory = backstory_templates.get(role.lower(), f"{name} is a {age}-year-old {role} navigating life's challenges.")
        
        # Generic values, fears, goals based on personality
        values = ["family", "stability", "honesty"]
        fears = ["failure", "loneliness", "uncertainty"]
        goals = ["be_happy", "help_others", "find_purpose"]
        coping = ["talk_to_friends", "exercise", "take_breaks"]
        quirks = ["morning_person", "coffee_lover", "organized"]
        
        if "introverted" in personality_traits:
            coping = ["spend_time_alone", "read", "journal"]
            quirks = ["quiet", "observant", "thoughtful"]
        
        if "perfectionist" in personality_traits:
            fears = ["making_mistakes", "disappointing_others", "not_being_good_enough"]
            coping = ["work_harder", "double_check_everything", "seek_validation"]
        
        return AgentIdentity(
            agent_id=agent_id,
            backstory=backstory,
            values=values,
            fears=fears,
            goals=goals,
            coping_mechanisms=coping,
            quirks=quirks,
            generated_at=datetime.now()
        )
    
    def generate_batch_identities(
        self,
        agents: List[Dict[str, Any]],
        society_context: str = "",
        batch_size: int = 10
    ) -> Dict[int, AgentIdentity]:
        """
        Generate identities for multiple agents
        
        Args:
            agents: List of agent dicts with id, name, age, role, personality
            society_context: Context about the society
            batch_size: How many to generate at once (for progress tracking)
            
        Returns:
            Dict mapping agent_id to AgentIdentity
        """
        identities = {}
        total = len(agents)
        
        print(f"🎭 Generating identities for {total} agents...")
        
        for i, agent in enumerate(agents):
            if (i + 1) % batch_size == 0 or (i + 1) == total:
                print(f"   Progress: {i + 1}/{total}")
            
            identity = self.generate_identity(
                agent_id=agent['agent_id'],
                name=agent['name'],
                age=agent['age'],
                role=agent['role'],
                personality_traits=agent.get('personality_traits', []),
                society_context=society_context
            )
            
            identities[agent['agent_id']] = identity
        
        print(f"✅ Generated {len(identities)} identities!")
        return identities
