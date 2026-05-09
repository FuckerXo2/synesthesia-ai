"""
Interview System
Talk to individual agents and get realistic responses
"""

from typing import Dict, Any, Optional
from datetime import datetime
from openai import OpenAI


class AgentInterviewer:
    """System for interviewing individual agents"""
    
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client
    
    def interview_agent(
        self,
        agent_data: Dict[str, Any],
        question: str,
        context: Optional[str] = None
    ) -> str:
        """
        Interview an agent with a question
        
        Args:
            agent_data: Agent information (name, role, mental health, memories, etc.)
            question: Question to ask the agent
            context: Optional additional context
            
        Returns:
            Agent's response as a string
        """
        # Build prompt
        prompt = self._build_interview_prompt(agent_data, question, context)
        
        try:
            response = self.llm_client.chat.completions.create(
                model="qwen/qwen3.5-122b-a10b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are roleplaying as an agent in a mental health simulation. Respond authentically based on your current state and experiences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"[Agent unable to respond: {str(e)}]"
    
    def _build_interview_prompt(
        self,
        agent_data: Dict[str, Any],
        question: str,
        context: Optional[str] = None
    ) -> str:
        """Build the interview prompt"""
        name = agent_data.get('name', 'Agent')
        age = agent_data.get('age', 30)
        role = agent_data.get('role', 'person')
        
        # Mental health state
        mental_health = agent_data.get('mental_health', {})
        anxiety = mental_health.get('anxiety', 0.5)
        depression = mental_health.get('depression', 0.5)
        stress = mental_health.get('stress', 0.5)
        wellbeing = mental_health.get('wellbeing', 0.5)
        category = mental_health.get('category', 'coping')
        
        # Recent memories
        memory_summary = agent_data.get('memory_summary', 'No recent significant events.')
        
        # Recent actions
        recent_actions = agent_data.get('recent_actions', [])
        actions_text = ', '.join(recent_actions[-5:]) if recent_actions else 'None'
        
        prompt = f"""You are {name}, a {age}-year-old {role}.

CURRENT MENTAL HEALTH STATE:
- Overall state: {category.upper()}
- Anxiety level: {anxiety:.2f} (0=calm, 1=severe anxiety)
- Depression level: {depression:.2f} (0=happy, 1=severe depression)
- Stress level: {stress:.2f} (0=relaxed, 1=overwhelmed)
- Wellbeing: {wellbeing:.2f} (0=poor, 1=excellent)

RECENT EXPERIENCES:
{memory_summary}

RECENT ACTIVITIES:
{actions_text}
"""
        
        if context:
            prompt += f"\n\nADDITIONAL CONTEXT:\n{context}"
        
        prompt += f"\n\nQUESTION: {question}\n\nRespond as {name} would, based on your current mental state and recent experiences. Be authentic and honest. If you're struggling, show it. If you're doing well, express that too."
        
        return prompt
    
    def conduct_mental_health_check(self, agent_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Conduct a structured mental health check-in
        
        Returns:
            Dictionary with responses to standard questions
        """
        questions = [
            "How are you feeling today?",
            "What's been on your mind lately?",
            "How would you rate your stress level?",
            "Is there anything you're worried about?",
            "What's been helping you cope?"
        ]
        
        responses = {}
        for question in questions:
            response = self.interview_agent(agent_data, question)
            responses[question] = response
        
        return responses
    
    def get_agent_perspective(
        self,
        agent_data: Dict[str, Any],
        topic: str
    ) -> str:
        """
        Get agent's perspective on a specific topic
        
        Args:
            agent_data: Agent information
            topic: Topic to ask about (e.g., "work", "relationships", "future")
            
        Returns:
            Agent's perspective
        """
        question = f"What are your thoughts on {topic}?"
        return self.interview_agent(agent_data, question)
