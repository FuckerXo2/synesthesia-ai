"""
Conversation Generator - LLM creates realistic conversations between agents
Uses identity, memories, relationships, and context
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

from synesthesia.agent.agent import Agent
from synesthesia.agent.identity import Memory
from synesthesia.agent.relationships import RelationshipType

load_dotenv()


class ConversationGenerator:
    """
    Generates realistic conversations between agents
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize conversation generator
        
        Args:
            llm_client: OpenAI client or AgentBrain (or creates new one)
        """
        # Handle both OpenAI client and AgentBrain
        if llm_client:
            if hasattr(llm_client, 'client'):
                # It's an AgentBrain, use its client
                self.llm = llm_client.client
                self.model = llm_client.default_model
            else:
                # It's an OpenAI client
                self.llm = llm_client
                self.model = os.getenv("LLM_MODEL_NAME", "qwen/qwen3.5-122b-a10b")
        else:
            self.llm = OpenAI(
                api_key=os.getenv("LLM_API_KEY"),
                base_url=os.getenv("LLM_BASE_URL")
            )
            self.model = os.getenv("LLM_MODEL_NAME", "qwen/qwen3.5-122b-a10b")
    
    def generate_conversation(
        self,
        agent1: Agent,
        agent2: Agent,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a conversation between two agents
        
        Args:
            agent1: First agent
            agent2: Second agent
            context: Additional context (location, situation, etc.)
            
        Returns:
            Dict with conversation details and impacts
        """
        
        # Get relationship between agents
        relationship = agent1.relationships.get_relationship(agent2.agent_id)
        relationship_type = relationship.relationship_type.value if relationship else "stranger"
        relationship_strength = relationship.strength if relationship else 0.0
        
        # Get shared memories
        shared_memories = []
        if agent1.memory and agent2.agent_id in agent1.memory.significant_relationships:
            shared_memories = agent1.memory.get_memories_with_person(agent2.agent_id, 3)
        
        # Build prompt
        prompt = self._build_conversation_prompt(
            agent1, agent2, relationship_type, relationship_strength, shared_memories, context or {}
        )
        
        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are simulating a realistic conversation between two people. Use their full context to make it authentic. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                response_format={"type": "json_object"},
                timeout=45
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure required fields
            if 'conversation' not in result:
                result['conversation'] = []
            if 'summary' not in result:
                result['summary'] = "Brief conversation"
            if 'impact_agent1' not in result:
                result['impact_agent1'] = {}
            if 'impact_agent2' not in result:
                result['impact_agent2'] = {}
            if 'relationship_change' not in result:
                result['relationship_change'] = 0.0
            
            return result
            
        except Exception as e:
            print(f"⚠️  Conversation generation error: {e}")
            return self._generate_fallback_conversation(agent1, agent2, relationship_type)
    
    def _build_conversation_prompt(
        self,
        agent1: Agent,
        agent2: Agent,
        relationship_type: str,
        relationship_strength: float,
        shared_memories: List[Memory],
        context: Dict[str, Any]
    ) -> str:
        """Build detailed prompt for conversation generation"""
        
        # Get agent contexts
        agent1_context = agent1.get_full_context()
        agent2_context = agent2.get_full_context()
        
        prompt = f"""Generate a realistic conversation between two people.

**Person 1: {agent1.name}**
- Age: {agent1.age}, Role: {agent1.role}
- Personality: {', '.join(agent1.personality_traits)}
- Mental State: {agent1.mental_health.category.value}
  - Anxiety: {agent1.mental_health.anxiety:.2f}
  - Depression: {agent1.mental_health.depression:.2f}
  - Stress: {agent1.mental_health.stress:.2f}
  - Wellbeing: {agent1.mental_health.wellbeing:.2f}
"""
        
        if agent1.identity and agent1.identity.backstory:
            prompt += f"- Backstory: {agent1.identity.backstory}\n"
            if agent1.identity.fears:
                prompt += f"- Fears: {', '.join(agent1.identity.fears[:2])}\n"
        
        if agent1.memory:
            recent = agent1.memory.get_recent_memories(3)
            if recent:
                prompt += f"- Recent experiences:\n"
                for mem in recent:
                    prompt += f"  • {mem.description}\n"
        
        prompt += f"""
**Person 2: {agent2.name}**
- Age: {agent2.age}, Role: {agent2.role}
- Personality: {', '.join(agent2.personality_traits)}
- Mental State: {agent2.mental_health.category.value}
  - Anxiety: {agent2.mental_health.anxiety:.2f}
  - Depression: {agent2.mental_health.depression:.2f}
  - Stress: {agent2.mental_health.stress:.2f}
  - Wellbeing: {agent2.mental_health.wellbeing:.2f}
"""
        
        if agent2.identity and agent2.identity.backstory:
            prompt += f"- Backstory: {agent2.identity.backstory}\n"
            if agent2.identity.fears:
                prompt += f"- Fears: {', '.join(agent2.identity.fears[:2])}\n"
        
        if agent2.memory:
            recent = agent2.memory.get_recent_memories(3)
            if recent:
                prompt += f"- Recent experiences:\n"
                for mem in recent:
                    prompt += f"  • {mem.description}\n"
        
        prompt += f"""
**Relationship:** {relationship_type} (strength: {relationship_strength:.2f})
"""
        
        if shared_memories:
            prompt += f"**Shared history:**\n"
            for mem in shared_memories:
                prompt += f"  • {mem.description}\n"
        
        if context:
            prompt += f"\n**Context:**\n"
            if 'location' in context:
                prompt += f"- Location: {context['location']}\n"
            if 'situation' in context:
                prompt += f"- Situation: {context['situation']}\n"
            if 'time' in context:
                prompt += f"- Time: {context['time']}\n"
        
        prompt += f"""
Generate a realistic conversation (3-6 exchanges) that:
1. Reflects their personalities and mental states
2. References their backstories and recent experiences if relevant
3. Feels authentic to their relationship
4. Has emotional depth and impact

Then analyze how this conversation affects each person's mental health and their relationship.

Return as JSON:
{{
  "conversation": [
    {{"speaker": "{agent1.name}", "text": "what they said", "internal_thought": "optional inner monologue"}},
    {{"speaker": "{agent2.name}", "text": "what they said", "internal_thought": "optional inner monologue"}},
    ...
  ],
  "summary": "brief summary of what happened",
  "emotional_tone": "supportive/tense/casual/deep/etc",
  "impact_agent1": {{
    "anxiety_change": -0.2 to 0.2,
    "depression_change": -0.2 to 0.2,
    "stress_change": -0.2 to 0.2,
    "wellbeing_change": -0.2 to 0.2,
    "emotional_impact": -1.0 to 1.0,
    "why": "brief explanation"
  }},
  "impact_agent2": {{
    "anxiety_change": -0.2 to 0.2,
    "depression_change": -0.2 to 0.2,
    "stress_change": -0.2 to 0.2,
    "wellbeing_change": -0.2 to 0.2,
    "emotional_impact": -1.0 to 1.0,
    "why": "brief explanation"
  }},
  "relationship_change": -0.2 to 0.2,
  "relationship_reason": "why relationship changed"
}}

Be realistic and authentic!"""

        return prompt
    
    def _generate_fallback_conversation(
        self,
        agent1: Agent,
        agent2: Agent,
        relationship_type: str
    ) -> Dict[str, Any]:
        """Generate a basic conversation if LLM fails"""
        
        # Simple conversation based on relationship
        if relationship_type in ["friend", "best_friend"]:
            conversation = [
                {"speaker": agent1.name, "text": "Hey, how are you doing?"},
                {"speaker": agent2.name, "text": "I'm okay, thanks for asking. You?"},
                {"speaker": agent1.name, "text": "Hanging in there. Want to grab coffee sometime?"},
                {"speaker": agent2.name, "text": "Yeah, that sounds good."}
            ]
            impact = {
                "anxiety_change": -0.05,
                "depression_change": -0.05,
                "stress_change": -0.03,
                "wellbeing_change": 0.05,
                "emotional_impact": 0.3,
                "why": "Friendly conversation"
            }
            relationship_change = 0.05
        elif relationship_type in ["coworker"]:
            conversation = [
                {"speaker": agent1.name, "text": "How's the project going?"},
                {"speaker": agent2.name, "text": "It's coming along. Lots of work though."},
                {"speaker": agent1.name, "text": "Yeah, I hear you. Let me know if you need help."},
                {"speaker": agent2.name, "text": "Thanks, I appreciate it."}
            ]
            impact = {
                "anxiety_change": -0.02,
                "depression_change": 0.0,
                "stress_change": -0.01,
                "wellbeing_change": 0.02,
                "emotional_impact": 0.1,
                "why": "Work conversation"
            }
            relationship_change = 0.02
        else:
            conversation = [
                {"speaker": agent1.name, "text": "Hi."},
                {"speaker": agent2.name, "text": "Hello."}
            ]
            impact = {
                "anxiety_change": 0.0,
                "depression_change": 0.0,
                "stress_change": 0.0,
                "wellbeing_change": 0.0,
                "emotional_impact": 0.0,
                "why": "Brief exchange"
            }
            relationship_change = 0.0
        
        return {
            "conversation": conversation,
            "summary": f"Brief {relationship_type} conversation",
            "emotional_tone": "casual",
            "impact_agent1": impact,
            "impact_agent2": impact,
            "relationship_change": relationship_change,
            "relationship_reason": "Casual interaction"
        }
    
    def apply_conversation_effects(
        self,
        agent1: Agent,
        agent2: Agent,
        conversation_result: Dict[str, Any],
        location: str = "unknown",
        timestamp: datetime = None
    ):
        """
        Apply the effects of a conversation to both agents
        
        Args:
            agent1: First agent
            agent2: Second agent
            conversation_result: Result from generate_conversation
            location: Where conversation happened
            timestamp: When it happened
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Apply mental health changes to agent1
        impact1 = conversation_result.get('impact_agent1', {})
        if impact1:
            changes1 = {
                'anxiety': impact1.get('anxiety_change', 0.0),
                'depression': impact1.get('depression_change', 0.0),
                'stress': impact1.get('stress_change', 0.0),
                'wellbeing': impact1.get('wellbeing_change', 0.0)
            }
            agent1.update_mental_health(changes1)
        
        # Apply mental health changes to agent2
        impact2 = conversation_result.get('impact_agent2', {})
        if impact2:
            changes2 = {
                'anxiety': impact2.get('anxiety_change', 0.0),
                'depression': impact2.get('depression_change', 0.0),
                'stress': impact2.get('stress_change', 0.0),
                'wellbeing': impact2.get('wellbeing_change', 0.0)
            }
            agent2.update_mental_health(changes2)
        
        # Update relationship
        relationship_change = conversation_result.get('relationship_change', 0.0)
        if relationship_change != 0.0:
            # Update agent1's view of agent2
            if agent1.relationships.has_relationship(agent2.agent_id):
                agent1.relationships.update_relationship_quality(
                    agent2.agent_id,
                    trust_delta=relationship_change * 0.5,
                    affection_delta=relationship_change * 0.5
                )
            
            # Update agent2's view of agent1
            if agent2.relationships.has_relationship(agent1.agent_id):
                agent2.relationships.update_relationship_quality(
                    agent1.agent_id,
                    trust_delta=relationship_change * 0.5,
                    affection_delta=relationship_change * 0.5
                )
        
        # Create memories for both agents
        conversation_snippet = self._format_conversation_snippet(conversation_result.get('conversation', []))
        
        # Memory for agent1
        memory1 = Memory(
            event_type="conversation",
            description=f"Conversation with {agent2.name}: {conversation_result.get('summary', 'talked')}",
            timestamp=timestamp,
            emotional_impact=impact1.get('emotional_impact', 0.0),
            emotional_tags=[conversation_result.get('emotional_tone', 'casual')],
            people_involved=[agent2.agent_id],
            mental_health_change=changes1 if impact1 else {},
            relationship_changes={agent2.agent_id: relationship_change},
            location=location,
            conversation_snippet=conversation_snippet
        )
        agent1.remember(memory1)
        
        # Memory for agent2
        memory2 = Memory(
            event_type="conversation",
            description=f"Conversation with {agent1.name}: {conversation_result.get('summary', 'talked')}",
            timestamp=timestamp,
            emotional_impact=impact2.get('emotional_impact', 0.0),
            emotional_tags=[conversation_result.get('emotional_tone', 'casual')],
            people_involved=[agent1.agent_id],
            mental_health_change=changes2 if impact2 else {},
            relationship_changes={agent1.agent_id: relationship_change},
            location=location,
            conversation_snippet=conversation_snippet
        )
        agent2.remember(memory2)
    
    def _format_conversation_snippet(self, conversation: List[Dict[str, str]], max_length: int = 200) -> str:
        """Format conversation for memory storage"""
        if not conversation:
            return ""
        
        snippet = ""
        for exchange in conversation[:3]:  # First 3 exchanges
            speaker = exchange.get('speaker', 'Unknown')
            text = exchange.get('text', '')
            snippet += f"{speaker}: \"{text}\"\n"
        
        if len(snippet) > max_length:
            snippet = snippet[:max_length] + "..."
        
        return snippet.strip()
