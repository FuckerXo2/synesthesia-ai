"""
Oracle AI - Natural language interface to query simulation data
Ask questions, get insights about the population
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class OracleAI:
    """
    AI that analyzes simulation data and answers questions
    """
    
    def __init__(self, llm_client, amd_client=None):
        """
        Initialize Oracle AI
        
        Args:
            llm_client: OpenAI client for LLM queries (NVIDIA)
            amd_client: Optional AMD client for Oracle queries
        """
        self.llm = llm_client
        self.amd_llm = amd_client  # AMD client for Oracle AI
        
        # AMD models (if available)
        self.amd_models = [
            "meta-llama/Llama-3.3-70B-Instruct",
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3"
        ]
        
        # NVIDIA models (fallback)
        self.nvidia_models = [
            "qwen/qwen3.5-122b-a10b",
            "meta/llama-3.3-70b-instruct",
            "mistralai/mistral-large-2411",
            "nvidia/llama-3.1-nemotron-70b-instruct"
        ]
        
        self.current_model_index = 0
        self.using_amd = amd_client is not None
    
    def query(self, question: str, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask a question about the simulation
        
        Args:
            question: Natural language question
            simulation_state: Current simulation state
            
        Returns:
            Dict with answer and supporting data
        """
        # Prepare simulation data for LLM
        context = self._prepare_context(simulation_state)
        
        prompt = f"""You are the Oracle AI analyzing a mental health population simulation.

CURRENT SIMULATION STATE:
{context}

USER QUESTION: {question}

Analyze the simulation data and provide:
1. A clear, direct answer to the question
2. Supporting statistics and evidence
3. Key insights or patterns you notice
4. Recommendations if relevant

Return as JSON:
{{
  "answer": "direct answer to the question",
  "statistics": {{"key": "value"}},
  "insights": ["insight 1", "insight 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "agents_of_interest": [
    {{"name": "agent name", "reason": "why they're relevant"}}
  ]
}}

Be specific, use numbers, and reference actual agents by name when relevant."""

        # Try multiple models with fallback
        max_retries = len(self.amd_models) if self.using_amd else len(self.nvidia_models)
        
        for attempt in range(max_retries):
            # Try AMD first if available
            if self.using_amd and attempt < len(self.amd_models):
                model = self.amd_models[attempt]
                client = self.amd_llm
                provider = "AMD"
            else:
                # Fallback to NVIDIA
                model = self.nvidia_models[self.current_model_index]
                client = self.llm
                provider = "NVIDIA"
            
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert mental health analyst and data scientist. Provide clear, actionable insights."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,  # Lower temperature for more factual responses
                    response_format={"type": "json_object"} if provider == "NVIDIA" else None,
                    timeout=60  # Increased timeout
                )
                
                result = json.loads(response.choices[0].message.content)
                result['_provider'] = provider  # Track which provider was used
                result['_model'] = model
                return result
                
            except Exception as e:
                error_msg = str(e)
                print(f"Oracle AI error with {provider} {model}: {error_msg}")
                
                # Try next model
                self.current_model_index = (self.current_model_index + 1) % len(self.nvidia_models)
                
                # If last attempt, return error
                if attempt == max_retries - 1:
                    return {
                        "answer": f"Unable to analyze simulation at this time. The AI service is experiencing issues. Please try again in a moment.",
                        "statistics": {},
                        "insights": ["AI service temporarily unavailable"],
                        "recommendations": ["Try again in a few moments", "Check your internet connection"],
                        "agents_of_interest": [],
                        "_provider": "ERROR",
                        "_model": "none"
                    }
    
    def _prepare_context(self, simulation_state: Dict[str, Any]) -> str:
        """Prepare simulation data as context for LLM"""
        
        agents = simulation_state.get('agents', [])
        stats = simulation_state.get('stats', {})
        time = simulation_state.get('time', 'unknown')
        
        # Calculate additional statistics
        total = sum(stats.values())
        
        # Group agents by mental health category
        agents_by_category = {
            'thriving': [],
            'coping': [],
            'struggling': [],
            'crisis': []
        }
        
        for agent in agents:
            category = agent['mental_health']['category']
            agents_by_category[category].append(agent)
        
        # Calculate averages
        if agents:
            avg_anxiety = sum(a['mental_health']['anxiety'] for a in agents) / len(agents)
            avg_depression = sum(a['mental_health']['depression'] for a in agents) / len(agents)
            avg_stress = sum(a['mental_health']['stress'] for a in agents) / len(agents)
            avg_wellbeing = sum(a['mental_health']['wellbeing'] for a in agents) / len(agents)
        else:
            avg_anxiety = avg_depression = avg_stress = avg_wellbeing = 0
        
        # Group by role
        agents_by_role = {}
        for agent in agents:
            role = agent['role']
            if role not in agents_by_role:
                agents_by_role[role] = []
            agents_by_role[role].append(agent)
        
        # Build context
        context = f"""
TIME: {time}
POPULATION: {len(agents)} agents

MENTAL HEALTH DISTRIBUTION:
- Thriving: {stats.get('thriving', 0)} ({stats.get('thriving', 0)/total*100:.1f}%)
- Coping: {stats.get('coping', 0)} ({stats.get('coping', 0)/total*100:.1f}%)
- Struggling: {stats.get('struggling', 0)} ({stats.get('struggling', 0)/total*100:.1f}%)
- Crisis: {stats.get('crisis', 0)} ({stats.get('crisis', 0)/total*100:.1f}%)

AVERAGE METRICS:
- Anxiety: {avg_anxiety:.2f}
- Depression: {avg_depression:.2f}
- Stress: {avg_stress:.2f}
- Wellbeing: {avg_wellbeing:.2f}

AGENTS BY ROLE:
"""
        
        for role, role_agents in agents_by_role.items():
            role_avg_stress = sum(a['mental_health']['stress'] for a in role_agents) / len(role_agents)
            crisis_count = sum(1 for a in role_agents if a['mental_health']['category'] == 'crisis')
            context += f"- {role}: {len(role_agents)} agents, avg stress: {role_avg_stress:.2f}, crisis: {crisis_count}\n"
        
        # Add details about agents in crisis
        if agents_by_category['crisis']:
            context += "\nAGENTS IN CRISIS:\n"
            for agent in agents_by_category['crisis'][:10]:  # Top 10
                mh = agent['mental_health']
                context += f"- {agent['name']} ({agent['role']}): anxiety={mh['anxiety']:.2f}, stress={mh['stress']:.2f}, wellbeing={mh['wellbeing']:.2f}\n"
        
        # Add details about struggling agents
        if agents_by_category['struggling']:
            context += "\nAGENTS STRUGGLING:\n"
            # Sort by stress level
            struggling_sorted = sorted(
                agents_by_category['struggling'],
                key=lambda a: a['mental_health']['stress'],
                reverse=True
            )[:5]  # Top 5 most stressed
            
            for agent in struggling_sorted:
                mh = agent['mental_health']
                context += f"- {agent['name']} ({agent['role']}): anxiety={mh['anxiety']:.2f}, stress={mh['stress']:.2f}\n"
        
        return context.strip()
    
    def get_insights(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get automatic insights without a specific question
        
        Args:
            simulation_state: Current simulation state
            
        Returns:
            Dict with insights
        """
        return self.query(
            "What are the key insights about this population's mental health right now? What patterns do you see?",
            simulation_state
        )
    
    def find_at_risk(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Find agents at risk of crisis"""
        return self.query(
            "Who is most at risk of a mental health crisis? List the top 5 agents and explain why.",
            simulation_state
        )
    
    def analyze_trends(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mental health trends"""
        return self.query(
            "What trends do you see in the mental health data? Is it getting better or worse? Why?",
            simulation_state
        )
    
    def recommend_interventions(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend interventions"""
        return self.query(
            "What interventions would you recommend to improve mental health in this population?",
            simulation_state
        )
