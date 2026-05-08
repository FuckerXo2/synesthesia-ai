"""
Database models and ORM for Synesthesia
Handles all database operations
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from synesthesia.database.schema import get_schema


class Database:
    """Database manager for Synesthesia simulation"""
    
    def __init__(self, db_path: str = "synesthesia_simulation.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._initialize_schema()
    
    def _connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()
        
        # Performance optimizations
        self.cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        self.cursor.execute("PRAGMA synchronous=NORMAL")  # Faster writes
        self.cursor.execute("PRAGMA cache_size=10000")  # Larger cache
        self.cursor.execute("PRAGMA temp_store=MEMORY")  # Temp tables in memory
    
    def _initialize_schema(self):
        """Create database schema if it doesn't exist"""
        schema_sql = get_schema()
        self.cursor.executescript(schema_sql)
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    # ==================== Agent Operations ====================
    
    def insert_agent(self, agent_data: Dict[str, Any]) -> int:
        """
        Insert a new agent into the database
        
        Args:
            agent_data: Dictionary with agent information
            
        Returns:
            agent_id of the inserted agent
        """
        # Convert lists to JSON strings
        for field in ['personality_traits', 'work_hours', 'sleep_hours', 
                      'active_hours', 'stressors', 'coping_mechanisms']:
            if field in agent_data and isinstance(agent_data[field], list):
                agent_data[field] = json.dumps(agent_data[field])
        
        columns = ', '.join(agent_data.keys())
        placeholders = ', '.join(['?' for _ in agent_data])
        
        query = f"INSERT INTO agents ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(agent_data.values()))
        self.conn.commit()
        
        return self.cursor.lastrowid
    
    def get_agent(self, agent_id: int) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        self.cursor.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
        row = self.cursor.fetchone()
        
        if row:
            agent = dict(row)
            # Parse JSON fields
            for field in ['personality_traits', 'work_hours', 'sleep_hours',
                          'active_hours', 'stressors', 'coping_mechanisms']:
                if agent.get(field):
                    agent[field] = json.loads(agent[field])
            return agent
        return None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents"""
        self.cursor.execute("SELECT * FROM agents")
        rows = self.cursor.fetchall()
        
        agents = []
        for row in rows:
            agent = dict(row)
            # Parse JSON fields
            for field in ['personality_traits', 'work_hours', 'sleep_hours',
                          'active_hours', 'stressors', 'coping_mechanisms']:
                if agent.get(field):
                    agent[field] = json.loads(agent[field])
            agents.append(agent)
        
        return agents
    
    def get_agents_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all agents with a specific role"""
        self.cursor.execute("SELECT * FROM agents WHERE role = ?", (role,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== Mental Health Operations ====================
    
    def insert_mental_health_state(self, state_data: Dict[str, Any]):
        """Insert a mental health state snapshot"""
        # Calculate overall distress
        if 'overall_distress' not in state_data:
            state_data['overall_distress'] = (
                state_data['anxiety'] + 
                state_data['depression'] + 
                state_data['stress']
            ) / 3
        
        # Determine mental health state category
        if 'mental_health_state' not in state_data:
            distress = state_data['overall_distress']
            if distress < 0.2:
                state_data['mental_health_state'] = 'thriving'
            elif distress < 0.4:
                state_data['mental_health_state'] = 'coping'
            elif distress < 0.6:
                state_data['mental_health_state'] = 'struggling'
            else:
                state_data['mental_health_state'] = 'crisis'
        
        columns = ', '.join(state_data.keys())
        placeholders = ', '.join(['?' for _ in state_data])
        
        query = f"INSERT INTO mental_health_states ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(state_data.values()))
        self.conn.commit()
    
    def get_latest_mental_health(self, agent_id: int) -> Optional[Dict[str, Any]]:
        """Get the most recent mental health state for an agent"""
        query = """
            SELECT * FROM mental_health_states 
            WHERE agent_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """
        self.cursor.execute(query, (agent_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_mental_health_history(
        self, 
        agent_id: int, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get mental health history for an agent"""
        query = """
            SELECT * FROM mental_health_states 
            WHERE agent_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        self.cursor.execute(query, (agent_id, limit))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== Action Operations ====================
    
    def insert_action(self, action_data: Dict[str, Any]):
        """Log an action taken by an agent"""
        # Convert dicts to JSON strings
        if 'action_details' in action_data and isinstance(action_data['action_details'], dict):
            action_data['action_details'] = json.dumps(action_data['action_details'])
        if 'mental_health_impact' in action_data and isinstance(action_data['mental_health_impact'], dict):
            action_data['mental_health_impact'] = json.dumps(action_data['mental_health_impact'])
        
        columns = ', '.join(action_data.keys())
        placeholders = ', '.join(['?' for _ in action_data])
        
        query = f"INSERT INTO actions ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(action_data.values()))
        self.conn.commit()
    
    def get_agent_actions(
        self, 
        agent_id: int, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get action history for an agent"""
        query = """
            SELECT * FROM actions 
            WHERE agent_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        self.cursor.execute(query, (agent_id, limit))
        rows = self.cursor.fetchall()
        
        actions = []
        for row in rows:
            action = dict(row)
            # Parse JSON fields
            if action.get('action_details'):
                action['action_details'] = json.loads(action['action_details'])
            if action.get('mental_health_impact'):
                action['mental_health_impact'] = json.loads(action['mental_health_impact'])
            actions.append(action)
        
        return actions
    
    # ==================== Connection Operations ====================
    
    def insert_connection(self, connection_data: Dict[str, Any]):
        """Create a connection between two agents"""
        columns = ', '.join(connection_data.keys())
        placeholders = ', '.join(['?' for _ in connection_data])
        
        query = f"INSERT OR IGNORE INTO connections ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(connection_data.values()))
        self.conn.commit()
    
    def get_agent_connections(
        self, 
        agent_id: int, 
        connection_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all connections for an agent"""
        if connection_type:
            query = """
                SELECT * FROM connections 
                WHERE (agent_id_1 = ? OR agent_id_2 = ?) 
                AND connection_type = ?
            """
            self.cursor.execute(query, (agent_id, agent_id, connection_type))
        else:
            query = """
                SELECT * FROM connections 
                WHERE agent_id_1 = ? OR agent_id_2 = ?
            """
            self.cursor.execute(query, (agent_id, agent_id))
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== Life Event Operations ====================
    
    def insert_life_event(self, event_data: Dict[str, Any]):
        """Log a life event for an agent"""
        if 'event_details' in event_data and isinstance(event_data['event_details'], dict):
            event_data['event_details'] = json.dumps(event_data['event_details'])
        if 'mental_health_impact' in event_data and isinstance(event_data['mental_health_impact'], dict):
            event_data['mental_health_impact'] = json.dumps(event_data['mental_health_impact'])
        
        columns = ', '.join(event_data.keys())
        placeholders = ', '.join(['?' for _ in event_data])
        
        query = f"INSERT INTO life_events ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(event_data.values()))
        self.conn.commit()
    
    # ==================== Interview Operations ====================
    
    def insert_interview(self, interview_data: Dict[str, Any]):
        """Log an interview with an agent"""
        columns = ', '.join(interview_data.keys())
        placeholders = ', '.join(['?' for _ in interview_data])
        
        query = f"INSERT INTO interviews ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(interview_data.values()))
        self.conn.commit()
    
    def get_agent_interviews(self, agent_id: int) -> List[Dict[str, Any]]:
        """Get interview history for an agent"""
        query = """
            SELECT * FROM interviews 
            WHERE agent_id = ? 
            ORDER BY timestamp DESC
        """
        self.cursor.execute(query, (agent_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== Simulation Operations ====================
    
    def create_simulation(self, simulation_data: Dict[str, Any]) -> str:
        """Create a new simulation record"""
        if 'config' in simulation_data and isinstance(simulation_data['config'], dict):
            simulation_data['config'] = json.dumps(simulation_data['config'])
        
        columns = ', '.join(simulation_data.keys())
        placeholders = ', '.join(['?' for _ in simulation_data])
        
        query = f"INSERT INTO simulations ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(simulation_data.values()))
        self.conn.commit()
        
        return simulation_data['simulation_id']
    
    def update_simulation_status(self, simulation_id: str, status: str):
        """Update simulation status"""
        query = "UPDATE simulations SET status = ? WHERE simulation_id = ?"
        self.cursor.execute(query, (status, simulation_id))
        self.conn.commit()
    
    # ==================== Analytics Operations ====================
    
    def insert_population_stats(self, stats_data: Dict[str, Any]):
        """Insert population statistics"""
        columns = ', '.join(stats_data.keys())
        placeholders = ', '.join(['?' for _ in stats_data])
        
        query = f"INSERT INTO population_stats ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(stats_data.values()))
        self.conn.commit()
    
    def get_population_stats(
        self, 
        simulation_id: str, 
        role: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get population statistics"""
        if role:
            query = """
                SELECT * FROM population_stats 
                WHERE simulation_id = ? AND role = ? 
                ORDER BY timestamp
            """
            self.cursor.execute(query, (simulation_id, role))
        else:
            query = """
                SELECT * FROM population_stats 
                WHERE simulation_id = ? AND role IS NULL 
                ORDER BY timestamp
            """
            self.cursor.execute(query, (simulation_id,))
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_agents_in_crisis(self) -> List[Dict[str, Any]]:
        """Get all agents currently in crisis"""
        query = """
            SELECT a.*, mh.anxiety, mh.depression, mh.stress, mh.wellbeing
            FROM agents a
            JOIN mental_health_states mh ON a.agent_id = mh.agent_id
            WHERE mh.mental_health_state = 'crisis'
            AND mh.id IN (
                SELECT MAX(id) FROM mental_health_states GROUP BY agent_id
            )
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ==================== Batch Operations ====================
    
    def batch_insert_agents(self, agents: List[Dict[str, Any]]):
        """Batch insert multiple agents for performance"""
        if not agents:
            return
        
        # Convert lists to JSON
        for agent in agents:
            for field in ['personality_traits', 'work_hours', 'sleep_hours',
                          'active_hours', 'stressors', 'coping_mechanisms']:
                if field in agent and isinstance(agent[field], list):
                    agent[field] = json.dumps(agent[field])
        
        columns = ', '.join(agents[0].keys())
        placeholders = ', '.join(['?' for _ in agents[0]])
        query = f"INSERT INTO agents ({columns}) VALUES ({placeholders})"
        
        self.cursor.executemany(query, [list(agent.values()) for agent in agents])
        self.conn.commit()
    
    def batch_insert_mental_health_states(self, states: List[Dict[str, Any]]):
        """Batch insert mental health states"""
        if not states:
            return
        
        # Calculate derived fields
        for state in states:
            if 'overall_distress' not in state:
                state['overall_distress'] = (
                    state['anxiety'] + state['depression'] + state['stress']
                ) / 3
            
            if 'mental_health_state' not in state:
                distress = state['overall_distress']
                if distress < 0.2:
                    state['mental_health_state'] = 'thriving'
                elif distress < 0.4:
                    state['mental_health_state'] = 'coping'
                elif distress < 0.6:
                    state['mental_health_state'] = 'struggling'
                else:
                    state['mental_health_state'] = 'crisis'
        
        columns = ', '.join(states[0].keys())
        placeholders = ', '.join(['?' for _ in states[0]])
        query = f"INSERT INTO mental_health_states ({columns}) VALUES ({placeholders})"
        
        self.cursor.executemany(query, [list(state.values()) for state in states])
        self.conn.commit()
