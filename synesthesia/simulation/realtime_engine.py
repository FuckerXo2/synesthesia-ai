"""
Real-Time Simulation Engine - Continuous world simulation like NPCs in games
"""

import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict

from synesthesia.agent.agent import Agent
from synesthesia.world.location import World, Location, LocationType
from synesthesia.actions.realtime_action import RealtimeAction, ActionState, get_action_duration
from synesthesia.database.models import Database


class RealtimeSimulationEngine:
    """
    Real-time continuous simulation engine
    
    Agents live continuously, not in turns:
    - Actions take real time
    - Agents move between locations
    - Interactions happen when agents are nearby
    - World runs at configurable speed (1x, 10x, 100x real-time)
    """
    
    def __init__(
        self,
        agents: List[Agent],
        world: World,
        db: Database,
        simulation_id: str,
        time_scale: float = 60.0,  # 1 real second = 60 sim seconds (1 minute)
        llm_client = None
    ):
        """
        Initialize real-time simulation
        
        Args:
            agents: List of agents
            world: World with locations
            db: Database
            simulation_id: Unique simulation ID
            time_scale: How fast simulation runs (1.0 = real-time, 60.0 = 1 real sec = 1 sim min)
            llm_client: LLM client for agent decisions
        """
        self.agents = {agent.agent_id: agent for agent in agents}
        self.world = world
        self.db = db
        self.simulation_id = simulation_id
        self.time_scale = time_scale
        self.llm_client = llm_client
        
        # Conversation system
        self.conversation_generator = None
        if llm_client:
            from synesthesia.llm.conversation_generator import ConversationGenerator
            self.conversation_generator = ConversationGenerator(llm_client)
        
        # Conversation tracking
        self.last_conversation_time: Dict[Tuple[int, int], float] = {}  # (agent1_id, agent2_id) -> last_time
        self.conversation_cooldown = 1800.0  # 30 minutes between conversations (sim time)
        
        # Simulation state
        self.is_running = False
        self.is_paused = False
        self.sim_start_time = datetime.now()
        self.real_start_time = time.time()
        
        # Agent state
        self.agent_locations: Dict[int, int] = {}  # agent_id -> location_id
        self.agent_actions: Dict[int, RealtimeAction] = {}  # agent_id -> current action
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0.0
        
        print(f"🌍 Real-Time Simulation Engine Initialized")
        print(f"   Simulation ID: {self.simulation_id}")
        print(f"   Population: {len(self.agents):,} agents")
        print(f"   Locations: {len(self.world.locations):,}")
        print(f"   Time Scale: {self.time_scale}x (1 real sec = {self.time_scale} sim secs)")
    
    def get_simulation_time(self) -> datetime:
        """Get current simulation time"""
        if not self.is_running:
            return self.sim_start_time
        
        real_elapsed = time.time() - self.real_start_time
        sim_elapsed = real_elapsed * self.time_scale
        return self.sim_start_time + timedelta(seconds=sim_elapsed)
    
    def get_agent_location(self, agent_id: int) -> Optional[Location]:
        """Get the location where an agent currently is"""
        location_id = self.agent_locations.get(agent_id)
        if location_id is not None:
            return self.world.get_location(location_id)
        return None
    
    def move_agent_to_location(self, agent_id: int, location_id: int) -> bool:
        """Move an agent to a location"""
        current_location_id = self.agent_locations.get(agent_id)
        success = self.world.move_agent(agent_id, current_location_id, location_id)
        
        if success:
            self.agent_locations[agent_id] = location_id
        
        return success
    
    def get_nearby_agents(self, agent_id: int) -> List[Agent]:
        """Get agents near this agent (same location)"""
        location = self.get_agent_location(agent_id)
        if not location:
            return []
        
        nearby_ids = location.get_nearby_agents(agent_id)
        return [self.agents[aid] for aid in nearby_ids if aid in self.agents]
    
    def assign_agent_action(self, agent_id: int, action: RealtimeAction):
        """Assign a new action to an agent"""
        # Interrupt current action if any
        if agent_id in self.agent_actions:
            self.agent_actions[agent_id].interrupt()
        
        # Start new action
        action.start()
        self.agent_actions[agent_id] = action
        
        # If action has a target location, move agent there
        if action.target_location_id is not None:
            self.move_agent_to_location(agent_id, action.target_location_id)
    
    def update_agent(self, agent_id: int, delta_time: float):
        """
        Update a single agent
        
        Args:
            agent_id: Agent to update
            delta_time: Time elapsed since last update (simulation seconds)
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return
        
        # Update current action
        current_action = self.agent_actions.get(agent_id)
        
        if current_action is None or current_action.is_complete():
            # Agent needs a new action - decide what to do next
            self._decide_next_action(agent_id)
        else:
            # Update ongoing action
            current_action.update(delta_time)
            
            # Check if action just completed
            if current_action.is_complete():
                self._on_action_complete(agent_id, current_action)
    
    def _decide_next_action(self, agent_id: int):
        """Decide what action the agent should do next"""
        agent = self.agents[agent_id]
        current_time = self.get_simulation_time()
        current_hour = current_time.hour
        
        # Get context
        location = self.get_agent_location(agent_id)
        nearby_agents = self.get_nearby_agents(agent_id)
        
        # Use LLM for intelligent decisions if available
        if self.llm_client:
            action_type = self._decide_action_with_llm(agent, current_hour, location, nearby_agents)
        else:
            # Fallback to rule-based decisions
            action_type = self._decide_action_rule_based(agent, current_hour, location, nearby_agents)
        
        # Create and assign the action
        action = self._create_action_from_type(agent, action_type, location, nearby_agents)
        self.assign_agent_action(agent_id, action)
    
    def _decide_action_with_llm(self, agent, current_hour, location, nearby_agents):
        """Use LLM to decide what agent should do"""
        from synesthesia.actions.types import ActionType
        
        # Build agent context
        agent_context = {
            "name": agent.name,
            "age": agent.age,
            "role": agent.role,
            "personality_traits": agent.personality_traits,
            "mental_health": {
                "anxiety": agent.mental_health.anxiety,
                "depression": agent.mental_health.depression,
                "stress": agent.mental_health.stress,
                "wellbeing": agent.mental_health.wellbeing,
                "category": agent.mental_health.category
            }
        }
        
        # Determine available actions based on context
        available_actions = []
        
        # Sleep if it's sleep time
        if current_hour in agent.sleep_hours:
            available_actions = [ActionType.SLEEP]
        # Work if it's work time
        elif current_hour in agent.work_hours:
            available_actions = [ActionType.WORK, ActionType.TAKE_BREAK]
        # Free time
        else:
            available_actions = [
                ActionType.WATCH_TV,
                ActionType.READ_BOOK,
                ActionType.EXERCISE,
                ActionType.RELAX,
                ActionType.TAKE_WALK,
                ActionType.HOBBY
            ]
            
            # Add social actions if others nearby
            if nearby_agents:
                available_actions.extend([
                    ActionType.SOCIALIZE,
                    ActionType.CALL_FRIEND,
                    ActionType.FAMILY_TIME
                ])
        
        # Get LLM decision
        try:
            action_type = self.llm_client.decide_action(
                agent_context,
                available_actions,
                current_hour,
                agent.recent_actions[-5:]  # Last 5 actions
            )
            return action_type
        except Exception as e:
            print(f"LLM decision error for {agent.name}: {e}")
            # Fallback to rule-based
            return self._decide_action_rule_based(agent, current_hour, location, nearby_agents)
    
    def _decide_action_rule_based(self, agent, current_hour, location, nearby_agents):
        """Rule-based decision making (fallback)"""
        from synesthesia.actions.types import ActionType
        
        # Sleep time
        if current_hour in agent.sleep_hours:
            return ActionType.SLEEP
        
        # Work time
        if current_hour in agent.work_hours:
            return ActionType.WORK
        
        # Free time - socialize if others nearby
        if nearby_agents:
            return ActionType.SOCIALIZE
        
        # Default: relax
        return ActionType.WATCH_TV
    
    def _create_action_from_type(self, agent, action_type, location, nearby_agents):
        """Create a RealtimeAction from an ActionType"""
        from synesthesia.actions.types import ActionType
        
        action_name = action_type.value  # Get string value from enum
        
        # Handle work actions - need to move to workplace
        if action_type in [ActionType.WORK, ActionType.GO_TO_WORK]:
            workplaces = self.world.get_locations_by_type(LocationType.WORKPLACE)
            if workplaces:
                workplace = workplaces[agent.agent_id % len(workplaces)]
                return RealtimeAction(
                    action_type="work_session",
                    duration_seconds=get_action_duration("work_session"),
                    target_location_id=workplace.location_id,
                    description=f"{agent.name} is working at {workplace.name}"
                )
        
        # Handle social actions - need target agent
        if action_type in [ActionType.SOCIALIZE, ActionType.CALL_FRIEND, ActionType.FAMILY_TIME]:
            if nearby_agents:
                other_agent = nearby_agents[0]
                return RealtimeAction(
                    action_type="conversation_medium",
                    duration_seconds=get_action_duration("conversation_medium"),
                    target_agent_id=other_agent.agent_id,
                    description=f"{agent.name} is talking with {other_agent.name}"
                )
        
        # Map ActionType to realtime action name
        action_mapping = {
            ActionType.SLEEP: "sleep",
            ActionType.EXERCISE: "exercise",
            ActionType.MEDITATE: "meditate",
            ActionType.WATCH_TV: "watch_tv",
            ActionType.READ_BOOK: "read_book",
            ActionType.TAKE_WALK: "take_walk",
            ActionType.LISTEN_MUSIC: "listen_music",
            ActionType.RELAX: "relax",
            ActionType.HOBBY: "hobby",
            ActionType.TAKE_BREAK: "take_break",
            ActionType.BREAKFAST: "breakfast",
            ActionType.DINNER: "dinner",
        }
        
        realtime_action_name = action_mapping.get(action_type, "relax")
        
        # Default action
        return RealtimeAction(
            action_type=realtime_action_name,
            duration_seconds=get_action_duration(realtime_action_name),
            description=f"{agent.name} is {action_name.replace('_', ' ')}"
        )
    
    def _on_action_complete(self, agent_id: int, action: RealtimeAction):
        """Handle action completion"""
        agent = self.agents[agent_id]
        
        # Log to database
        if self.db:
            self.db.insert_action({
                "agent_id": agent_id,
                "timestamp": datetime.now(),
                "simulated_time": self.get_simulation_time().strftime("%Y-%m-%d %H:%M:%S"),
                "action_type": action.action_type,
                "action_details": action.metadata,
                "mental_health_impact": {},
                "success": True
            })
        
        # Add to agent's recent actions
        agent.add_recent_action(f"{action.action_type} at {self.get_simulation_time().strftime('%H:%M')}")
    
    def update(self, delta_time_real: float):
        """
        Update the simulation by one frame
        
        Args:
            delta_time_real: Real time elapsed since last update (seconds)
        """
        if not self.is_running or self.is_paused:
            return
        
        # Convert real time to simulation time
        delta_time_sim = delta_time_real * self.time_scale
        
        # Update all agents
        for agent_id in self.agents.keys():
            self.update_agent(agent_id, delta_time_sim)
        
        # Check for conversations (every few frames to avoid spam)
        if self.frame_count % 30 == 0 and self.conversation_generator:  # Every 30 frames
            self._check_for_conversations()
        
        # Update FPS counter
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.current_fps = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time
    
    def run(self, target_fps: float = 30.0, duration_hours: Optional[float] = None):
        """
        Run the simulation
        
        Args:
            target_fps: Target frames per second
            duration_hours: How many simulation hours to run (None = infinite)
        """
        self.is_running = True
        self.real_start_time = time.time()
        
        frame_time = 1.0 / target_fps
        last_update = time.time()
        
        print(f"\n{'='*60}")
        print(f"🚀 STARTING REAL-TIME SIMULATION")
        print(f"{'='*60}\n")
        
        try:
            while self.is_running:
                current_time = time.time()
                delta_time = current_time - last_update
                
                # Update simulation
                self.update(delta_time)
                
                # Check if we've reached duration
                if duration_hours:
                    sim_time = self.get_simulation_time()
                    elapsed_hours = (sim_time - self.sim_start_time).total_seconds() / 3600
                    if elapsed_hours >= duration_hours:
                        break
                
                # Print status every 5 seconds
                if int(current_time) % 5 == 0 and int(current_time) != int(last_update):
                    self._print_status()
                
                last_update = current_time
                
                # Sleep to maintain target FPS
                sleep_time = frame_time - (time.time() - current_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print("\n⚠️  Simulation interrupted by user")
        finally:
            self.is_running = False
            self._print_final_status()
    
    def _print_status(self):
        """Print current simulation status"""
        sim_time = self.get_simulation_time()
        
        # Count agents by activity
        activities = defaultdict(int)
        for agent_id, action in self.agent_actions.items():
            if action and action.is_in_progress():
                activities[action.action_type] += 1
        
        print(f"[{sim_time.strftime('%Y-%m-%d %H:%M:%S')}] "
              f"FPS: {self.current_fps:.1f} | "
              f"Active: {len([a for a in self.agent_actions.values() if a and a.is_in_progress()])} agents")
        
        # Show top activities
        if activities:
            top_activities = sorted(activities.items(), key=lambda x: x[1], reverse=True)[:3]
            activity_str = ", ".join([f"{act}: {count}" for act, count in top_activities])
            print(f"   Top activities: {activity_str}")
    
    def _print_final_status(self):
        """Print final simulation status"""
        sim_time = self.get_simulation_time()
        real_elapsed = time.time() - self.real_start_time
        sim_elapsed = (sim_time - self.sim_start_time).total_seconds()
        
        print(f"\n{'='*60}")
        print(f"✅ SIMULATION COMPLETE")
        print(f"{'='*60}")
        print(f"Simulation time: {sim_elapsed / 3600:.2f} hours")
        print(f"Real time: {real_elapsed:.1f} seconds")
        print(f"Time scale: {sim_elapsed / real_elapsed:.1f}x")
        print(f"{'='*60}\n")
    
    def pause(self):
        """Pause the simulation"""
        self.is_paused = True
        print("⏸️  Simulation paused")
    
    def resume(self):
        """Resume the simulation"""
        self.is_paused = False
        print("▶️  Simulation resumed")
    
    def stop(self):
        """Stop the simulation"""
        self.is_running = False
        print("⏹️  Simulation stopped")
    
    def _check_for_conversations(self):
        """Check if any agents should have conversations"""
        current_sim_time = self.get_simulation_time()
        current_sim_seconds = (current_sim_time - self.sim_start_time).total_seconds()
        
        # Group agents by location
        agents_by_location = defaultdict(list)
        for agent_id, location_id in self.agent_locations.items():
            agents_by_location[location_id].append(agent_id)
        
        # Check each location for potential conversations
        for location_id, agent_ids in agents_by_location.items():
            if len(agent_ids) < 2:
                continue
            
            # Try to start conversations between agents
            for i, agent1_id in enumerate(agent_ids):
                for agent2_id in agent_ids[i+1:]:
                    # Check if they should talk
                    if self._should_agents_talk(agent1_id, agent2_id, current_sim_seconds):
                        self._trigger_conversation(agent1_id, agent2_id, location_id, current_sim_time)
    
    def _should_agents_talk(self, agent1_id: int, agent2_id: int, current_sim_seconds: float) -> bool:
        """Check if two agents should have a conversation"""
        # Check cooldown
        pair_key = tuple(sorted([agent1_id, agent2_id]))
        last_time = self.last_conversation_time.get(pair_key, 0)
        
        if current_sim_seconds - last_time < self.conversation_cooldown:
            return False
        
        # Check if both agents are free (not in middle of important action)
        action1 = self.agent_actions.get(agent1_id)
        action2 = self.agent_actions.get(agent2_id)
        
        # Don't interrupt sleep or work
        if action1 and action1.is_in_progress() and action1.action_type in ["sleep", "work_session"]:
            return False
        if action2 and action2.is_in_progress() and action2.action_type in ["sleep", "work_session"]:
            return False
        
        # Check if they have a relationship
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        has_relationship = agent1.relationships.has_relationship(agent2_id)
        
        # Higher chance if they have a relationship
        if has_relationship:
            return random.random() < 0.3  # 30% chance
        else:
            return random.random() < 0.05  # 5% chance for strangers
    
    def _trigger_conversation(self, agent1_id: int, agent2_id: int, location_id: int, current_time: datetime):
        """Trigger a conversation between two agents"""
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        location = self.world.get_location(location_id)
        
        print(f"💬 Conversation: {agent1.name} & {agent2.name} at {location.name if location else 'unknown'}")
        
        try:
            # Generate conversation
            context = {
                "location": location.name if location else "unknown",
                "time": current_time.strftime("%I:%M %p"),
                "situation": self._get_situation_context(agent1, agent2, location)
            }
            
            conversation = self.conversation_generator.generate_conversation(
                agent1,
                agent2,
                context=context
            )
            
            # Apply effects
            self.conversation_generator.apply_conversation_effects(
                agent1,
                agent2,
                conversation,
                location=location.name if location else "unknown",
                timestamp=current_time
            )
            
            # Update cooldown
            pair_key = tuple(sorted([agent1_id, agent2_id]))
            current_sim_seconds = (current_time - self.sim_start_time).total_seconds()
            self.last_conversation_time[pair_key] = current_sim_seconds
            
            # Log conversation summary
            print(f"   Summary: {conversation.get('summary', 'talked')}")
            print(f"   Tone: {conversation.get('emotional_tone', 'casual')}")
            
        except Exception as e:
            print(f"   ⚠️  Conversation error: {e}")
    
    def _get_situation_context(self, agent1: Agent, agent2: Agent, location: Optional[Location]) -> str:
        """Get context about the situation for conversation"""
        # Check mental health states
        if agent1.mental_health.category.value == "crisis" or agent2.mental_health.category.value == "crisis":
            return "One person seems to be struggling"
        
        # Check location type
        if location:
            if location.location_type == LocationType.WORKPLACE:
                return "At work, discussing projects"
            elif location.location_type == LocationType.HOME:
                return "At home, relaxing"
            elif location.location_type == LocationType.RESTAURANT:
                return "Grabbing food together"
            elif location.location_type == LocationType.PARK:
                return "Taking a break outside"
        
        return "Casual encounter"

