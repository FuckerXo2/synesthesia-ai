"""
Society Orchestrator - LLM generates society structure and orchestrates events
No hardcoded templates - LLM creates everything from user description
"""

import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class SocietyOrchestrator:
    """
    LLM-powered society orchestrator
    Generates society structure from user description, then orchestrates emergent events
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize orchestrator
        
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
        self.society_structure = None
        self.event_history = []
    
    def generate_society_structure(
        self,
        user_description: str,
        population: int,
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        LLM generates complete society structure from user description
        
        Args:
            user_description: User's description of the society
            population: Total population
            additional_context: Optional additional context
            
        Returns:
            Dict with society structure
        """
        print(f"🧠 Generating society structure for: '{user_description}'")
        print(f"   Population: {population:,}")
        
        prompt = f"""You are designing a realistic society simulation.

User wants to simulate: "{user_description}"
Population: {population} people
{f"Additional context: {additional_context}" if additional_context else ""}

Generate a complete, realistic society structure. Think deeply about:
- What roles/occupations exist in THIS SPECIFIC society?
- What is the daily rhythm? (what happens at different times of day)
- What recurring events happen? (weekly meetings, monthly gatherings, etc.)
- What random events could occur? (crises, celebrations, conflicts)
- What locations are needed FOR THIS SPECIFIC SOCIETY?
- What social structures exist? (hierarchies, groups, relationships)

IMPORTANT FOR LOCATIONS:
- Be SPECIFIC to the society type
- For schools: use "classrooms", "library", "cafeteria", "gym", "dormitories", NOT "workplaces"
- For hospitals: use "emergency_room", "wards", "operating_rooms", NOT "workplaces"
- For offices: use "offices", "meeting_rooms", "break_rooms"
- For medieval: use "taverns", "markets", "castle", NOT "restaurants" or "stores"
- Match the location types to the society's time period and context

Be realistic and detailed. Use your knowledge of how real societies work.

Return as JSON with this structure:
{{
  "society_type": "brief name",
  "description": "2-3 sentence description",
  "roles": {{
    "role_name": {{
      "percentage": 0-100,
      "work_hours": [start_hour, end_hour],
      "stress_baseline": 0.0-1.0,
      "description": "what they do"
    }}
  }},
  "daily_rhythms": {{
    "hour": "what typically happens"
  }},
  "recurring_events": [
    {{
      "name": "event name",
      "frequency": "daily/weekly/monthly",
      "day": "monday/tuesday/etc or day_of_month",
      "time": "hour",
      "description": "what happens",
      "affects": ["role1", "role2"],
      "mental_health_impact": {{"anxiety": 0.0, "stress": 0.0}}
    }}
  ],
  "random_events": [
    {{
      "name": "event name",
      "probability": 0.0-1.0,
      "description": "what happens",
      "triggers": ["condition1", "condition2"],
      "affects": "all/specific_roles",
      "mental_health_impact": {{"anxiety": 0.0, "depression": 0.0, "stress": 0.0}},
      "cascading_effects": ["effect1", "effect2"]
    }}
  ],
  "locations": {{
    "location_type": {{
      "count": number,
      "capacity": number,
      "description": "what it's for"
    }}
  }},
  "social_structures": {{
    "hierarchies": ["top to bottom"],
    "groups": ["group types"],
    "interaction_patterns": "how people interact"
  }},
  "stressors": ["main sources of stress"],
  "support_systems": ["what helps mental health"]
}}

Make it realistic and detailed!"""

        try:
            # Try multiple models with retry
            models_to_try = [
                self.model,
                "meta/llama-3.3-70b-instruct",
                "mistralai/mistral-large-2411",
                "nvidia/llama-3.1-nemotron-70b-instruct"
            ]
            
            last_error = None
            for model in models_to_try:
                try:
                    print(f"   Trying model: {model}...")
                    response = self.llm.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a sociologist and simulation designer. Create realistic, detailed society structures. Return only valid JSON."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        response_format={"type": "json_object"},
                        timeout=45
                    )
                    
                    self.society_structure = json.loads(response.choices[0].message.content)
                    
                    print(f"✅ Society structure generated with {model}!")
                    print(f"   Type: {self.society_structure.get('society_type', 'unknown')}")
                    print(f"   Roles: {len(self.society_structure.get('roles', {}))}")
                    print(f"   Locations: {list(self.society_structure.get('locations', {}).keys())}")
                    
                    return self.society_structure
                    
                except Exception as e:
                    last_error = e
                    print(f"   ❌ {model} failed: {str(e)[:80]}")
                    continue
            
            # All models failed
            print(f"❌ All models failed. Using smart fallback.")
            return self._generate_smart_fallback(user_description, population)
            
        except Exception as e:
            print(f"❌ Error generating society structure: {e}")
            return self._generate_smart_fallback(user_description, population)
    
    def _generate_smart_fallback(self, description: str, population: int) -> Dict[str, Any]:
        """Smart fallback that detects society type and generates appropriate locations/roles"""
        desc_lower = description.lower()
        
        # Detect society type from description
        if any(w in desc_lower for w in ['school', 'university', 'college', 'campus', 'student', 'finals', 'exam']):
            return {
                "society_type": "educational_institution",
                "description": description,
                "roles": {
                    "students": {"percentage": 70, "work_hours": [8, 17], "stress_baseline": 0.6},
                    "teachers": {"percentage": 15, "work_hours": [7, 16], "stress_baseline": 0.55},
                    "staff": {"percentage": 10, "work_hours": [8, 17], "stress_baseline": 0.4},
                    "administrators": {"percentage": 5, "work_hours": [8, 17], "stress_baseline": 0.5}
                },
                "daily_rhythms": {"8": "classes_start", "12": "lunch", "15": "classes_end", "22": "study_time"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "classrooms": {"count": 8, "capacity": 30},
                    "library": {"count": 1, "capacity": 80},
                    "cafeteria": {"count": 2, "capacity": 100},
                    "dormitories": {"count": 6, "capacity": 20},
                    "gym": {"count": 1, "capacity": 50},
                    "student_center": {"count": 1, "capacity": 60},
                    "labs": {"count": 3, "capacity": 25}
                },
                "stressors": ["exams", "assignments", "grades", "social pressure"],
                "support_systems": ["study groups", "counseling", "friends", "professors"]
            }
        
        elif any(w in desc_lower for w in ['hospital', 'clinic', 'medical', 'healthcare', 'nurse', 'doctor', 'er', 'emergency']):
            return {
                "society_type": "hospital",
                "description": description,
                "roles": {
                    "doctors": {"percentage": 20, "work_hours": [7, 19], "stress_baseline": 0.7},
                    "nurses": {"percentage": 35, "work_hours": [7, 19], "stress_baseline": 0.75},
                    "patients": {"percentage": 30, "work_hours": [], "stress_baseline": 0.8},
                    "admin_staff": {"percentage": 10, "work_hours": [8, 17], "stress_baseline": 0.45},
                    "support_staff": {"percentage": 5, "work_hours": [8, 17], "stress_baseline": 0.4}
                },
                "daily_rhythms": {"7": "shift_change", "12": "rounds", "19": "evening_shift"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "emergency_room": {"count": 1, "capacity": 40},
                    "wards": {"count": 5, "capacity": 30},
                    "operating_rooms": {"count": 3, "capacity": 10},
                    "cafeteria": {"count": 1, "capacity": 60},
                    "staff_rooms": {"count": 3, "capacity": 20},
                    "waiting_areas": {"count": 3, "capacity": 40},
                    "pharmacy": {"count": 1, "capacity": 15}
                },
                "stressors": ["patient load", "emergencies", "long shifts", "life-or-death decisions"],
                "support_systems": ["colleagues", "counseling", "breaks", "team support"]
            }
        
        elif any(w in desc_lower for w in ['startup', 'tech', 'office', 'company', 'corporate', 'work']):
            return {
                "society_type": "tech_company",
                "description": description,
                "roles": {
                    "engineers": {"percentage": 40, "work_hours": [9, 20], "stress_baseline": 0.65},
                    "managers": {"percentage": 15, "work_hours": [8, 19], "stress_baseline": 0.7},
                    "designers": {"percentage": 15, "work_hours": [9, 18], "stress_baseline": 0.55},
                    "sales": {"percentage": 15, "work_hours": [8, 18], "stress_baseline": 0.6},
                    "support": {"percentage": 15, "work_hours": [9, 17], "stress_baseline": 0.5}
                },
                "daily_rhythms": {"9": "standup", "12": "lunch", "14": "meetings", "18": "wind_down"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "open_office": {"count": 3, "capacity": 40},
                    "meeting_rooms": {"count": 5, "capacity": 10},
                    "cafeteria": {"count": 1, "capacity": 60},
                    "break_room": {"count": 2, "capacity": 20},
                    "apartments": {"count": 8, "capacity": 5},
                    "gym": {"count": 1, "capacity": 30},
                    "rooftop": {"count": 1, "capacity": 40}
                },
                "stressors": ["deadlines", "meetings", "performance reviews", "burnout"],
                "support_systems": ["team lunches", "therapy benefits", "remote work", "bonuses"]
            }
        
        elif any(w in desc_lower for w in ['prison', 'jail', 'correctional', 'inmates']):
            return {
                "society_type": "prison",
                "description": description,
                "roles": {
                    "inmates": {"percentage": 70, "work_hours": [6, 20], "stress_baseline": 0.85},
                    "guards": {"percentage": 20, "work_hours": [6, 18], "stress_baseline": 0.75},
                    "staff": {"percentage": 10, "work_hours": [8, 17], "stress_baseline": 0.55}
                },
                "daily_rhythms": {"6": "wake_up", "8": "work_detail", "12": "lunch", "20": "lockdown"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "cells": {"count": 10, "capacity": 8},
                    "yard": {"count": 1, "capacity": 80},
                    "cafeteria": {"count": 1, "capacity": 60},
                    "workshop": {"count": 2, "capacity": 20},
                    "visitation": {"count": 1, "capacity": 20},
                    "medical": {"count": 1, "capacity": 15},
                    "guard_station": {"count": 3, "capacity": 5}
                },
                "stressors": ["confinement", "violence", "isolation", "uncertainty"],
                "support_systems": ["counseling", "education programs", "family visits"]
            }
        
        elif any(w in desc_lower for w in ['space', 'station', 'mars', 'astronaut', 'spacecraft']):
            return {
                "society_type": "space_station",
                "description": description,
                "roles": {
                    "astronauts": {"percentage": 50, "work_hours": [6, 20], "stress_baseline": 0.65},
                    "scientists": {"percentage": 30, "work_hours": [8, 18], "stress_baseline": 0.6},
                    "engineers": {"percentage": 20, "work_hours": [8, 20], "stress_baseline": 0.7}
                },
                "daily_rhythms": {"6": "wake_up", "8": "mission_briefing", "12": "lunch", "20": "rest"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "command_module": {"count": 1, "capacity": 10},
                    "lab": {"count": 3, "capacity": 8},
                    "sleeping_quarters": {"count": 4, "capacity": 5},
                    "cafeteria": {"count": 1, "capacity": 20},
                    "exercise_bay": {"count": 1, "capacity": 10},
                    "observation_deck": {"count": 1, "capacity": 15},
                    "engineering_bay": {"count": 2, "capacity": 8}
                },
                "stressors": ["isolation", "danger", "confined space", "mission pressure"],
                "support_systems": ["team bonding", "earth contact", "exercise", "routine"]
            }
        
        else:
            # Generic city/town fallback
            return {
                "society_type": "modern_city",
                "description": description,
                "roles": {
                    "workers": {"percentage": 50, "work_hours": [9, 17], "stress_baseline": 0.5},
                    "students": {"percentage": 20, "work_hours": [8, 15], "stress_baseline": 0.45},
                    "retirees": {"percentage": 15, "work_hours": [], "stress_baseline": 0.3},
                    "unemployed": {"percentage": 15, "work_hours": [], "stress_baseline": 0.65}
                },
                "daily_rhythms": {"8": "morning", "12": "lunch", "17": "evening", "22": "night"},
                "recurring_events": [],
                "random_events": [],
                "locations": {
                    "houses": {"count": 10, "capacity": 5},
                    "offices": {"count": 5, "capacity": 30},
                    "park": {"count": 2, "capacity": 50},
                    "restaurant": {"count": 3, "capacity": 40},
                    "gym": {"count": 1, "capacity": 30},
                    "store": {"count": 3, "capacity": 40},
                    "hospital": {"count": 1, "capacity": 30}
                },
                "stressors": ["work", "finances", "relationships", "health"],
                "support_systems": ["family", "friends", "therapy", "community"]
            }

    def _generate_fallback_structure(self, description: str, population: int) -> Dict[str, Any]:
        """Legacy fallback - redirects to smart fallback"""
        return self._generate_smart_fallback(description, population)
    
    def orchestrate_events(
        self,
        current_time: datetime,
        population_state: Dict[str, Any],
        recent_events: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate events that should happen right now
        
        Args:
            current_time: Current simulation time
            population_state: Summary of population (mental health, locations, etc.)
            recent_events: Recent events that happened
            
        Returns:
            List of events to execute
        """
        if not self.society_structure:
            return []
        
        events = []
        
        # Check recurring events
        events.extend(self._check_recurring_events(current_time))
        
        # Check random events
        events.extend(self._check_random_events(population_state))
        
        # Generate emergent events (LLM creativity)
        events.extend(self._generate_emergent_events(current_time, population_state, recent_events or []))
        
        # Store in history
        self.event_history.extend(events)
        
        return events
    
    def _check_recurring_events(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Check if any recurring events should happen now"""
        events = []
        
        recurring = self.society_structure.get('recurring_events', [])
        
        for event in recurring:
            should_trigger = False
            
            # Check frequency
            if event['frequency'] == 'daily':
                should_trigger = True
            elif event['frequency'] == 'weekly':
                day_name = current_time.strftime('%A').lower()
                should_trigger = (event.get('day', '').lower() == day_name)
            elif event['frequency'] == 'monthly':
                should_trigger = (current_time.day == 1)  # First of month
            
            # Check time
            if should_trigger and 'time' in event:
                event_hour = int(event['time'].replace('am', '').replace('pm', '').split(':')[0])
                if 'pm' in event['time'] and event_hour != 12:
                    event_hour += 12
                should_trigger = (current_time.hour == event_hour)
            
            if should_trigger:
                events.append({
                    'type': 'recurring',
                    'name': event['name'],
                    'description': event.get('description', ''),
                    'affects': event.get('affects', []),
                    'mental_health_impact': event.get('mental_health_impact', {}),
                    'time': current_time
                })
        
        return events
    
    def _check_random_events(self, population_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if any random events should happen"""
        events = []
        
        random_events = self.society_structure.get('random_events', [])
        
        for event in random_events:
            probability = event.get('probability', 0.01)
            
            # Check triggers
            triggers_met = True
            if 'triggers' in event:
                # Check if conditions are met (e.g., high stress, low wellbeing)
                triggers_met = self._check_triggers(event['triggers'], population_state)
            
            # Roll for event
            if triggers_met and random.random() < probability:
                events.append({
                    'type': 'random',
                    'name': event['name'],
                    'description': event.get('description', ''),
                    'affects': event.get('affects', 'all'),
                    'mental_health_impact': event.get('mental_health_impact', {}),
                    'cascading_effects': event.get('cascading_effects', [])
                })
        
        return events
    
    def _check_triggers(self, triggers: List[str], population_state: Dict[str, Any]) -> bool:
        """Check if event triggers are met"""
        # Simple trigger checking
        for trigger in triggers:
            if 'high_stress' in trigger.lower():
                avg_stress = population_state.get('avg_stress', 0.5)
                if avg_stress < 0.7:
                    return False
            elif 'low_wellbeing' in trigger.lower():
                avg_wellbeing = population_state.get('avg_wellbeing', 0.5)
                if avg_wellbeing > 0.3:
                    return False
            elif 'crisis' in trigger.lower():
                crisis_count = population_state.get('crisis_count', 0)
                if crisis_count < 5:
                    return False
        
        return True
    
    def _generate_emergent_events(
        self,
        current_time: datetime,
        population_state: Dict[str, Any],
        recent_events: List[str]
    ) -> List[Dict[str, Any]]:
        """
        LLM generates emergent events based on current state
        This is where the magic happens - unexpected, realistic events
        """
        # Only generate emergent events occasionally (every ~10 sim hours)
        if random.random() > 0.1:
            return []
        
        prompt = f"""You are orchestrating a living society simulation.

Society: {self.society_structure.get('society_type', 'unknown')}
Current time: {current_time.strftime('%A %I:%M %p')}

Population state:
- Average stress: {population_state.get('avg_stress', 0.5):.2f}
- Average anxiety: {population_state.get('avg_anxiety', 0.5):.2f}
- Average depression: {population_state.get('avg_depression', 0.5):.2f}
- Average wellbeing: {population_state.get('avg_wellbeing', 0.5):.2f}
- Agents in crisis: {population_state.get('crisis_count', 0)}

Recent events:
{chr(10).join(f"- {e}" for e in recent_events[-10:])}

Based on the society type, current state, and recent events, what 1-2 realistic 
events would naturally happen right now? Think about:
- Daily rhythms of this society
- How stress/mental health affects behavior
- Cascading effects from recent events
- Realistic human responses

Return as JSON array:
[
  {{
    "name": "brief_event_name",
    "description": "what happens",
    "affects": ["role1", "role2"] or "all",
    "mental_health_impact": {{"anxiety": 0.0, "stress": 0.0, "wellbeing": 0.0}},
    "why": "why this event makes sense right now"
  }}
]

Be creative but realistic!"""

        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are orchestrating a realistic society simulation. Generate believable emergent events. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                response_format={"type": "json_object"},
                timeout=30
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Handle both array and object responses
            if isinstance(result, dict) and 'events' in result:
                emergent_events = result['events']
            elif isinstance(result, list):
                emergent_events = result
            else:
                emergent_events = [result]
            
            # Add metadata
            for event in emergent_events:
                event['type'] = 'emergent'
                event['time'] = current_time
            
            return emergent_events
            
        except Exception as e:
            print(f"⚠️  Could not generate emergent events: {e}")
            return []
    
    def get_society_summary(self) -> str:
        """Get a human-readable summary of the society"""
        if not self.society_structure:
            return "No society structure generated yet"
        
        summary = f"""
{'='*60}
SOCIETY: {self.society_structure.get('society_type', 'Unknown').upper()}
{'='*60}

{self.society_structure.get('description', 'No description')}

ROLES:
"""
        for role, details in self.society_structure.get('roles', {}).items():
            summary += f"  • {role}: {details.get('percentage', 0)}% - {details.get('description', '')}\n"
        
        summary += f"\nRECURRING EVENTS: {len(self.society_structure.get('recurring_events', []))}"
        summary += f"\nRANDOM EVENTS: {len(self.society_structure.get('random_events', []))}"
        summary += f"\nSTRESSORS: {', '.join(self.society_structure.get('stressors', []))}"
        summary += f"\n{'='*60}\n"
        
        return summary
