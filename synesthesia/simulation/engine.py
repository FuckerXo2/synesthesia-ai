"""
Simulation engine - the main loop that runs the world
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import uuid

from synesthesia.agent.agent import Agent
from synesthesia.actions.executor import ActionExecutor
from synesthesia.actions.types import ActionType
from synesthesia.database.models import Database


class SimulationEngine:
    """Main simulation engine that runs the Synesthesia world"""
    
    def __init__(
        self,
        agents: List[Agent],
        db: Database,
        simulation_id: Optional[str] = None,
        total_hours: int = 72,
        minutes_per_round: int = 60,
        use_llm: bool = False,
        llm_client = None,
        max_workers: int = 10,
        llm_semaphore: int = 10  # Limit concurrent LLM calls
    ):
        """
        Initialize simulation engine
        
        Args:
            agents: List of agents in the simulation
            db: Database instance
            simulation_id: Unique simulation ID
            total_hours: Total simulated hours to run
            minutes_per_round: Minutes represented by each round
            use_llm: Whether to use LLM for agent decisions
            llm_client: LLM client instance
            max_workers: Max parallel workers for agent processing
        """
        self.agents = {agent.agent_id: agent for agent in agents}
        self.db = db
        self.simulation_id = simulation_id or str(uuid.uuid4())
        self.total_hours = total_hours
        self.minutes_per_round = minutes_per_round
        self.use_llm = use_llm
        self.llm_client = llm_client
        self.max_workers = max_workers
        self.llm_semaphore = llm_semaphore
        
        self.action_executor = ActionExecutor(db)
        
        # Simulation state
        self.current_round = 0
        self.total_rounds = (total_hours * 60) // minutes_per_round
        self.is_running = False
        self.is_paused = False
        
        # Statistics
        self.stats = {
            "total_actions": 0,
            "crisis_interventions": 0,
            "therapy_sessions": 0,
            "social_interactions": 0
        }
        
        print(f"🌍 Simulation Engine Initialized")
        print(f"   Simulation ID: {self.simulation_id}")
        print(f"   Population: {len(self.agents):,} agents")
        print(f"   Duration: {total_hours} hours ({self.total_rounds} rounds)")
        print(f"   Time scale: {minutes_per_round} minutes per round")
    
    def get_simulated_time(self, round_num: int) -> tuple[int, int, str]:
        """
        Get simulated time for a given round
        
        Returns:
            (day, hour, formatted_string)
        """
        total_minutes = round_num * self.minutes_per_round
        day = (total_minutes // (60 * 24)) + 1
        hour = (total_minutes // 60) % 24
        formatted = f"Day {day}, {hour:02d}:00"
        return day, hour, formatted
    
    def get_active_agents(self, current_hour: int) -> List[Agent]:
        """
        Get agents who should be active this hour
        
        Args:
            current_hour: Current hour (0-23)
            
        Returns:
            List of active agents
        """
        active = []
        for agent in self.agents.values():
            # Agents are active if they're awake
            if agent.is_awake(current_hour):
                active.append(agent)
        
        return active
    
    def process_agent_round(
        self,
        agent: Agent,
        current_hour: int,
        simulated_time: str
    ) -> Dict[str, Any]:
        """
        Process one round for a single agent
        
        Args:
            agent: Agent to process
            current_hour: Current hour
            simulated_time: Formatted simulated time
            
        Returns:
            Dict with round results
        """
        try:
            # Choose action
            action = self.action_executor.choose_action(
                agent,
                current_hour,
                use_llm=self.use_llm,
                llm_client=self.llm_client
            )
            
            # Execute action
            result = self.action_executor.execute_action(
                agent,
                action,
                current_hour,
                simulated_time
            )
            
            # Update stats
            self.stats["total_actions"] += 1
            if result.get("crisis_triggered"):
                self.stats["crisis_interventions"] += 1
            if action == ActionType.ATTEND_THERAPY:
                self.stats["therapy_sessions"] += 1
            if action in [ActionType.SOCIALIZE, ActionType.CALL_FRIEND, 
                         ActionType.CALL_FAMILY, ActionType.FAMILY_TIME]:
                self.stats["social_interactions"] += 1
            
            return {
                "success": True,
                "agent_id": agent.agent_id,
                "action": action.value,
                "result": result
            }
            
        except Exception as e:
            print(f"❌ Error processing agent {agent.agent_id}: {e}")
            return {
                "success": False,
                "agent_id": agent.agent_id,
                "error": str(e)
            }
    
    async def run_round_async(self, round_num: int):
        """
        Run a single round asynchronously with parallel agent processing
        
        Args:
            round_num: Current round number
        """
        day, hour, simulated_time = self.get_simulated_time(round_num)
        
        # Get active agents
        active_agents = self.get_active_agents(hour)
        
        if not active_agents:
            return
        
        # Process agents in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self.process_agent_round,
                    agent,
                    hour,
                    simulated_time
                )
                for agent in active_agents
            ]
            
            # Wait for all to complete
            results = [future.result() for future in futures]
        
        # Calculate and store population statistics
        self._calculate_population_stats(simulated_time)
        
        return results
    
    def run_round(self, round_num: int):
        """
        Run a single round synchronously
        
        Args:
            round_num: Current round number
        """
        day, hour, simulated_time = self.get_simulated_time(round_num)
        
        # Get active agents
        active_agents = self.get_active_agents(hour)
        
        if not active_agents:
            return []
        
        # Process each agent
        results = []
        for agent in active_agents:
            result = self.process_agent_round(agent, hour, simulated_time)
            results.append(result)
        
        # Calculate and store population statistics
        self._calculate_population_stats(simulated_time)
        
        return results
    
    def _calculate_population_stats(self, simulated_time: str):
        """Calculate and store population-level statistics"""
        # Overall stats
        total_agents = len(self.agents)
        total_anxiety = sum(a.mental_health.anxiety for a in self.agents.values())
        total_depression = sum(a.mental_health.depression for a in self.agents.values())
        total_stress = sum(a.mental_health.stress for a in self.agents.values())
        total_wellbeing = sum(a.mental_health.wellbeing for a in self.agents.values())
        
        agents_in_crisis = sum(1 for a in self.agents.values() if a.is_in_crisis)
        agents_thriving = sum(1 for a in self.agents.values() if a.is_thriving)
        
        self.db.insert_population_stats({
            "simulation_id": self.simulation_id,
            "timestamp": datetime.now(),
            "simulated_time": simulated_time,
            "role": None,  # Overall stats
            "total_agents": total_agents,
            "avg_anxiety": total_anxiety / total_agents,
            "avg_depression": total_depression / total_agents,
            "avg_stress": total_stress / total_agents,
            "avg_wellbeing": total_wellbeing / total_agents,
            "agents_in_crisis": agents_in_crisis,
            "agents_thriving": agents_thriving
        })
        
        # Per-role stats
        roles = set(agent.role for agent in self.agents.values())
        for role in roles:
            role_agents = [a for a in self.agents.values() if a.role == role]
            if not role_agents:
                continue
            
            role_count = len(role_agents)
            role_anxiety = sum(a.mental_health.anxiety for a in role_agents)
            role_depression = sum(a.mental_health.depression for a in role_agents)
            role_stress = sum(a.mental_health.stress for a in role_agents)
            role_wellbeing = sum(a.mental_health.wellbeing for a in role_agents)
            
            role_crisis = sum(1 for a in role_agents if a.is_in_crisis)
            role_thriving = sum(1 for a in role_agents if a.is_thriving)
            
            self.db.insert_population_stats({
                "simulation_id": self.simulation_id,
                "timestamp": datetime.now(),
                "simulated_time": simulated_time,
                "role": role,
                "total_agents": role_count,
                "avg_anxiety": role_anxiety / role_count,
                "avg_depression": role_depression / role_count,
                "avg_stress": role_stress / role_count,
                "avg_wellbeing": role_wellbeing / role_count,
                "agents_in_crisis": role_crisis,
                "agents_thriving": role_thriving
            })
    
    def run(self, progress_callback=None):
        """
        Run the full simulation
        
        Args:
            progress_callback: Optional callback function(round, total, message)
        """
        self.is_running = True
        start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"🚀 STARTING SIMULATION")
        print(f"{'='*60}\n")
        
        # Create simulation record
        self.db.create_simulation({
            "simulation_id": self.simulation_id,
            "society_description": "Generated population",
            "total_population": len(self.agents),
            "total_simulated_hours": self.total_hours,
            "status": "running",
            "config": {
                "total_hours": self.total_hours,
                "minutes_per_round": self.minutes_per_round,
                "use_llm": self.use_llm
            }
        })
        
        try:
            for round_num in range(self.total_rounds):
                if not self.is_running:
                    break
                
                while self.is_paused:
                    import time
                    time.sleep(0.1)
                
                self.current_round = round_num
                day, hour, simulated_time = self.get_simulated_time(round_num)
                
                # Run the round
                results = self.run_round(round_num)
                
                # Progress reporting
                if (round_num + 1) % 10 == 0 or round_num == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    progress = (round_num + 1) / self.total_rounds * 100
                    active_count = len([r for r in results if r.get("success")])
                    
                    # Get current stats
                    crisis_count = sum(1 for a in self.agents.values() if a.is_in_crisis)
                    avg_distress = sum(a.mental_health.overall_distress for a in self.agents.values()) / len(self.agents)
                    
                    message = (
                        f"[{simulated_time}] Round {round_num + 1}/{self.total_rounds} "
                        f"({progress:.1f}%) - {active_count} agents active - "
                        f"Crisis: {crisis_count} - Avg Distress: {avg_distress:.2f} - "
                        f"Elapsed: {elapsed:.1f}s"
                    )
                    print(message)
                    
                    if progress_callback:
                        progress_callback(round_num + 1, self.total_rounds, message)
            
            # Simulation complete
            total_elapsed = (datetime.now() - start_time).total_seconds()
            self.db.update_simulation_status(self.simulation_id, "completed")
            
            print(f"\n{'='*60}")
            print(f"✅ SIMULATION COMPLETE")
            print(f"{'='*60}")
            print(f"Total time: {total_elapsed:.1f}s")
            print(f"Total actions: {self.stats['total_actions']:,}")
            print(f"Crisis interventions: {self.stats['crisis_interventions']}")
            print(f"Therapy sessions: {self.stats['therapy_sessions']}")
            print(f"Social interactions: {self.stats['social_interactions']:,}")
            print(f"\nDatabase: {self.db.db_path}")
            print(f"{'='*60}\n")
            
        except KeyboardInterrupt:
            print("\n⚠️  Simulation interrupted by user")
            self.db.update_simulation_status(self.simulation_id, "interrupted")
        except Exception as e:
            print(f"\n❌ Simulation error: {e}")
            self.db.update_simulation_status(self.simulation_id, "error")
            raise
        finally:
            self.is_running = False
    
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
        self.db.update_simulation_status(self.simulation_id, "stopped")
        print("⏹️  Simulation stopped")
    
    def get_agent(self, agent_id: int) -> Optional[Agent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_agents_by_role(self, role: str) -> List[Agent]:
        """Get all agents with a specific role"""
        return [a for a in self.agents.values() if a.role == role]
    
    def get_agents_in_crisis(self) -> List[Agent]:
        """Get all agents currently in crisis"""
        return [a for a in self.agents.values() if a.is_in_crisis]
    
    def get_simulation_summary(self) -> Dict[str, Any]:
        """Get summary of current simulation state"""
        total = len(self.agents)
        crisis = len(self.get_agents_in_crisis())
        thriving = sum(1 for a in self.agents.values() if a.is_thriving)
        
        avg_anxiety = sum(a.mental_health.anxiety for a in self.agents.values()) / total
        avg_depression = sum(a.mental_health.depression for a in self.agents.values()) / total
        avg_stress = sum(a.mental_health.stress for a in self.agents.values()) / total
        avg_wellbeing = sum(a.mental_health.wellbeing for a in self.agents.values()) / total
        
        return {
            "simulation_id": self.simulation_id,
            "current_round": self.current_round,
            "total_rounds": self.total_rounds,
            "progress": (self.current_round / self.total_rounds * 100) if self.total_rounds > 0 else 0,
            "population": {
                "total": total,
                "in_crisis": crisis,
                "thriving": thriving,
                "crisis_rate": crisis / total if total > 0 else 0,
                "thriving_rate": thriving / total if total > 0 else 0
            },
            "mental_health": {
                "avg_anxiety": avg_anxiety,
                "avg_depression": avg_depression,
                "avg_stress": avg_stress,
                "avg_wellbeing": avg_wellbeing,
                "avg_distress": (avg_anxiety + avg_depression + avg_stress) / 3
            },
            "stats": self.stats
        }
