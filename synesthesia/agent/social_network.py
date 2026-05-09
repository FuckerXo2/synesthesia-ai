"""
Social Network System
Manages relationships between agents (friends, family, colleagues)
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random


class ConnectionType(Enum):
    """Types of social connections"""
    FAMILY = "family"
    FRIEND = "friend"
    COLLEAGUE = "colleague"
    ROMANTIC_PARTNER = "romantic_partner"
    THERAPIST = "therapist"
    ACQUAINTANCE = "acquaintance"


class SocialConnection:
    """Represents a connection between two agents"""
    
    def __init__(
        self,
        agent_id_1: int,
        agent_id_2: int,
        connection_type: ConnectionType,
        strength: float = 0.5
    ):
        self.agent_id_1 = agent_id_1
        self.agent_id_2 = agent_id_2
        self.connection_type = connection_type
        self.strength = strength  # 0.0 to 1.0
        self.interaction_count = 0
        self.last_interaction = None
    
    def interact(self, quality: float = 0.5):
        """
        Record an interaction between the agents
        
        Args:
            quality: Quality of interaction (0=negative, 0.5=neutral, 1=positive)
        """
        self.interaction_count += 1
        
        # Update strength based on interaction quality
        if quality > 0.6:
            self.strength = min(1.0, self.strength + 0.05)
        elif quality < 0.4:
            self.strength = max(0.0, self.strength - 0.05)
    
    def get_other_agent(self, agent_id: int) -> int:
        """Get the other agent in this connection"""
        return self.agent_id_2 if agent_id == self.agent_id_1 else self.agent_id_1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id_1': self.agent_id_1,
            'agent_id_2': self.agent_id_2,
            'connection_type': self.connection_type.value,
            'strength': self.strength,
            'interaction_count': self.interaction_count
        }


class SocialNetwork:
    """Manages the social network of all agents"""
    
    def __init__(self):
        self.connections: Dict[Tuple[int, int], SocialConnection] = {}
        self.agent_connections: Dict[int, List[SocialConnection]] = {}
    
    def add_connection(
        self,
        agent_id_1: int,
        agent_id_2: int,
        connection_type: ConnectionType,
        strength: float = 0.5
    ):
        """Add a connection between two agents"""
        # Ensure consistent ordering
        if agent_id_1 > agent_id_2:
            agent_id_1, agent_id_2 = agent_id_2, agent_id_1
        
        key = (agent_id_1, agent_id_2)
        
        if key not in self.connections:
            connection = SocialConnection(agent_id_1, agent_id_2, connection_type, strength)
            self.connections[key] = connection
            
            # Update agent connection lists
            if agent_id_1 not in self.agent_connections:
                self.agent_connections[agent_id_1] = []
            if agent_id_2 not in self.agent_connections:
                self.agent_connections[agent_id_2] = []
            
            self.agent_connections[agent_id_1].append(connection)
            self.agent_connections[agent_id_2].append(connection)
    
    def get_connections(
        self,
        agent_id: int,
        connection_type: Optional[ConnectionType] = None
    ) -> List[SocialConnection]:
        """Get all connections for an agent"""
        connections = self.agent_connections.get(agent_id, [])
        
        if connection_type:
            connections = [c for c in connections if c.connection_type == connection_type]
        
        return connections
    
    def get_connected_agents(
        self,
        agent_id: int,
        connection_type: Optional[ConnectionType] = None
    ) -> List[int]:
        """Get IDs of all agents connected to this agent"""
        connections = self.get_connections(agent_id, connection_type)
        return [c.get_other_agent(agent_id) for c in connections]
    
    def get_connection_strength(self, agent_id_1: int, agent_id_2: int) -> float:
        """Get the strength of connection between two agents"""
        if agent_id_1 > agent_id_2:
            agent_id_1, agent_id_2 = agent_id_2, agent_id_1
        
        key = (agent_id_1, agent_id_2)
        connection = self.connections.get(key)
        
        return connection.strength if connection else 0.0
    
    def record_interaction(
        self,
        agent_id_1: int,
        agent_id_2: int,
        quality: float = 0.5
    ):
        """Record an interaction between two agents"""
        if agent_id_1 > agent_id_2:
            agent_id_1, agent_id_2 = agent_id_2, agent_id_1
        
        key = (agent_id_1, agent_id_2)
        connection = self.connections.get(key)
        
        if connection:
            connection.interact(quality)
    
    def get_social_support_level(self, agent_id: int) -> float:
        """
        Calculate social support level for an agent
        
        Returns:
            Float from 0.0 (no support) to 1.0 (strong support network)
        """
        connections = self.get_connections(agent_id)
        
        if not connections:
            return 0.0
        
        # Weight different connection types
        weights = {
            ConnectionType.FAMILY: 1.5,
            ConnectionType.ROMANTIC_PARTNER: 1.5,
            ConnectionType.FRIEND: 1.0,
            ConnectionType.COLLEAGUE: 0.5,
            ConnectionType.THERAPIST: 2.0,
            ConnectionType.ACQUAINTANCE: 0.3
        }
        
        total_support = 0.0
        for connection in connections:
            weight = weights.get(connection.connection_type, 1.0)
            total_support += connection.strength * weight
        
        # Normalize to 0-1 range (assume 5 strong connections = max support)
        return min(1.0, total_support / 5.0)
    
    def get_network_stats(self, agent_id: int) -> Dict[str, Any]:
        """Get statistics about an agent's social network"""
        connections = self.get_connections(agent_id)
        
        stats = {
            'total_connections': len(connections),
            'by_type': {},
            'avg_strength': 0.0,
            'social_support': self.get_social_support_level(agent_id)
        }
        
        if connections:
            # Count by type
            for conn_type in ConnectionType:
                count = len([c for c in connections if c.connection_type == conn_type])
                if count > 0:
                    stats['by_type'][conn_type.value] = count
            
            # Average strength
            stats['avg_strength'] = sum(c.strength for c in connections) / len(connections)
        
        return stats


class SocialNetworkGenerator:
    """Generates social networks for agent populations"""
    
    @staticmethod
    def generate_network(agents: List[Dict[str, Any]]) -> SocialNetwork:
        """
        Generate a social network for a population of agents
        
        Args:
            agents: List of agent data dictionaries
            
        Returns:
            SocialNetwork with connections
        """
        network = SocialNetwork()
        
        # Group agents by role for colleague connections
        agents_by_role = {}
        for agent in agents:
            role = agent.get('role', 'other')
            if role not in agents_by_role:
                agents_by_role[role] = []
            agents_by_role[role].append(agent)
        
        # Create family connections (10% of agents have family in simulation)
        for i, agent in enumerate(agents):
            if random.random() < 0.1 and i < len(agents) - 1:
                other_agent = agents[i + 1]
                network.add_connection(
                    agent['agent_id'],
                    other_agent['agent_id'],
                    ConnectionType.FAMILY,
                    strength=random.uniform(0.6, 1.0)
                )
        
        # Create friend connections (each agent has 2-5 friends)
        for agent in agents:
            num_friends = random.randint(2, 5)
            potential_friends = [a for a in agents if a['agent_id'] != agent['agent_id']]
            friends = random.sample(potential_friends, min(num_friends, len(potential_friends)))
            
            for friend in friends:
                network.add_connection(
                    agent['agent_id'],
                    friend['agent_id'],
                    ConnectionType.FRIEND,
                    strength=random.uniform(0.4, 0.9)
                )
        
        # Create colleague connections (agents with same role)
        for role, role_agents in agents_by_role.items():
            if len(role_agents) > 1:
                for i, agent in enumerate(role_agents):
                    # Connect to 2-3 colleagues
                    num_colleagues = min(random.randint(2, 3), len(role_agents) - 1)
                    colleagues = random.sample(
                        [a for a in role_agents if a['agent_id'] != agent['agent_id']],
                        num_colleagues
                    )
                    
                    for colleague in colleagues:
                        network.add_connection(
                            agent['agent_id'],
                            colleague['agent_id'],
                            ConnectionType.COLLEAGUE,
                            strength=random.uniform(0.3, 0.7)
                        )
        
        # Create romantic partner connections (20% of agents have partners)
        available_agents = agents.copy()
        random.shuffle(available_agents)
        
        while len(available_agents) >= 2:
            if random.random() < 0.2:
                agent1 = available_agents.pop()
                agent2 = available_agents.pop()
                
                network.add_connection(
                    agent1['agent_id'],
                    agent2['agent_id'],
                    ConnectionType.ROMANTIC_PARTNER,
                    strength=random.uniform(0.7, 1.0)
                )
            else:
                available_agents.pop()
        
        return network
