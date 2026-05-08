"""
Spatial World System - 2D continuous space for GTA-style movement
Agents have positions and move through 2D space, not teleporting
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum

from synesthesia.world.location import Location, LocationType


@dataclass
class SpatialLocation(Location):
    """
    Location with spatial properties for 2D world
    Extends base Location with spatial boundaries
    """
    # Spatial boundaries (rectangle)
    width: float = 50.0
    height: float = 50.0
    
    # Entry points (where agents spawn when entering)
    entry_points: List[Tuple[float, float]] = field(default_factory=list)
    
    # Obstacles within location (for pathfinding)
    obstacles: List[Tuple[float, float, float, float]] = field(default_factory=list)  # (x, y, width, height)
    
    def __post_init__(self):
        """Initialize entry points if not provided"""
        if not self.entry_points:
            # Default: center of location
            self.entry_points = [(self.x + self.width / 2, self.y + self.height / 2)]
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is inside this location"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
    
    def get_random_point_inside(self) -> Tuple[float, float]:
        """Get a random point inside this location"""
        import random
        return (
            self.x + random.uniform(0, self.width),
            self.y + random.uniform(0, self.height)
        )
    
    def get_nearest_entry_point(self, x: float, y: float) -> Tuple[float, float]:
        """Get the nearest entry point to a position"""
        if not self.entry_points:
            return (self.x + self.width / 2, self.y + self.height / 2)
        
        def distance(point):
            return math.sqrt((point[0] - x) ** 2 + (point[1] - y) ** 2)
        
        return min(self.entry_points, key=distance)
    
    def distance_to(self, x: float, y: float) -> float:
        """Get distance from a point to this location (to nearest edge)"""
        # Clamp point to location bounds
        closest_x = max(self.x, min(x, self.x + self.width))
        closest_y = max(self.y, min(y, self.y + self.height))
        
        # Calculate distance
        dx = x - closest_x
        dy = y - closest_y
        return math.sqrt(dx * dx + dy * dy)


@dataclass
class SpatialAgent:
    """
    Agent with spatial properties for 2D movement
    """
    agent_id: int
    
    # Position
    x: float = 0.0
    y: float = 0.0
    
    # Velocity (for smooth movement)
    vx: float = 0.0
    vy: float = 0.0
    
    # Movement
    speed: float = 2.0  # meters per second
    target_x: Optional[float] = None
    target_y: Optional[float] = None
    
    # Path (for pathfinding)
    path: List[Tuple[float, float]] = field(default_factory=list)
    path_index: int = 0
    
    # State
    is_moving: bool = False
    current_location_id: Optional[int] = None
    
    def set_target(self, x: float, y: float):
        """Set movement target"""
        self.target_x = x
        self.target_y = y
        self.is_moving = True
    
    def set_path(self, path: List[Tuple[float, float]]):
        """Set path to follow"""
        self.path = path
        self.path_index = 0
        if path:
            self.set_target(path[0][0], path[0][1])
    
    def update_movement(self, delta_time: float) -> bool:
        """
        Update agent movement
        
        Args:
            delta_time: Time elapsed (seconds)
            
        Returns:
            True if reached target, False otherwise
        """
        if not self.is_moving or self.target_x is None or self.target_y is None:
            return False
        
        # Calculate direction to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Check if reached target
        if distance < 0.5:  # Within 0.5 meters
            self.x = self.target_x
            self.y = self.target_y
            self.vx = 0.0
            self.vy = 0.0
            
            # Move to next waypoint if following path
            if self.path and self.path_index < len(self.path) - 1:
                self.path_index += 1
                next_point = self.path[self.path_index]
                self.set_target(next_point[0], next_point[1])
                return False
            else:
                # Reached final destination
                self.is_moving = False
                self.target_x = None
                self.target_y = None
                self.path = []
                self.path_index = 0
                return True
        
        # Move towards target
        # Normalize direction
        dx /= distance
        dy /= distance
        
        # Set velocity
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        
        # Update position
        move_distance = self.speed * delta_time
        if move_distance > distance:
            # Don't overshoot
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += self.vx * delta_time
            self.y += self.vy * delta_time
        
        return False
    
    def distance_to(self, x: float, y: float) -> float:
        """Calculate distance to a point"""
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx * dx + dy * dy)
    
    def distance_to_agent(self, other: 'SpatialAgent') -> float:
        """Calculate distance to another agent"""
        return self.distance_to(other.x, other.y)


class SpatialWorld:
    """
    2D spatial world with continuous movement
    Manages spatial locations and agent positions
    """
    
    def __init__(self, width: float = 1000.0, height: float = 1000.0):
        """
        Initialize spatial world
        
        Args:
            width: World width in meters
            height: World height in meters
        """
        self.width = width
        self.height = height
        
        # Locations
        self.locations: Dict[int, SpatialLocation] = {}
        self.location_id_counter = 0
        
        # Agents
        self.agents: Dict[int, SpatialAgent] = {}
        
        # Spatial index for fast proximity queries
        self.grid_size = 50.0  # Grid cell size
        self.agent_grid: Dict[Tuple[int, int], Set[int]] = {}
        
        print(f"🌍 Spatial World Created: {width}m x {height}m")
    
    def create_location(
        self,
        name: str,
        location_type: LocationType,
        x: float,
        y: float,
        width: float = 50.0,
        height: float = 50.0,
        capacity: int = 100,
        description: str = "",
        tags: List[str] = None
    ) -> SpatialLocation:
        """Create a spatial location"""
        location = SpatialLocation(
            location_id=self.location_id_counter,
            name=name,
            location_type=location_type,
            x=x,
            y=y,
            width=width,
            height=height,
            capacity=capacity,
            description=description,
            tags=tags or []
        )
        
        self.locations[location.location_id] = location
        self.location_id_counter += 1
        
        return location
    
    def add_agent(self, agent_id: int, x: float = 0.0, y: float = 0.0, speed: float = 2.0) -> SpatialAgent:
        """Add an agent to the spatial world"""
        spatial_agent = SpatialAgent(
            agent_id=agent_id,
            x=x,
            y=y,
            speed=speed
        )
        
        self.agents[agent_id] = spatial_agent
        self._update_agent_grid(agent_id)
        
        return spatial_agent
    
    def get_agent(self, agent_id: int) -> Optional[SpatialAgent]:
        """Get spatial agent by ID"""
        return self.agents.get(agent_id)
    
    def get_location(self, location_id: int) -> Optional[SpatialLocation]:
        """Get location by ID"""
        return self.locations.get(location_id)
    
    def get_agent_location(self, agent_id: int) -> Optional[SpatialLocation]:
        """Get the location an agent is currently in"""
        spatial_agent = self.agents.get(agent_id)
        if not spatial_agent or spatial_agent.current_location_id is None:
            return None
        
        return self.locations.get(spatial_agent.current_location_id)
    
    def move_agent_to_location(self, agent_id: int, location_id: int):
        """
        Start moving agent to a location
        Sets up path to location's entry point
        """
        spatial_agent = self.agents.get(agent_id)
        location = self.locations.get(location_id)
        
        if not spatial_agent or not location:
            return False
        
        # Get entry point
        entry_point = location.get_nearest_entry_point(spatial_agent.x, spatial_agent.y)
        
        # For now, simple direct path (will add A* pathfinding later)
        spatial_agent.set_path([entry_point])
        spatial_agent.current_location_id = location_id
        
        return True
    
    def update_agent(self, agent_id: int, delta_time: float) -> bool:
        """
        Update agent movement
        
        Returns:
            True if agent reached destination
        """
        spatial_agent = self.agents.get(agent_id)
        if not spatial_agent:
            return False
        
        # Update movement
        reached = spatial_agent.update_movement(delta_time)
        
        # Update spatial grid
        self._update_agent_grid(agent_id)
        
        return reached
    
    def get_nearby_agents(self, agent_id: int, radius: float = 5.0) -> List[int]:
        """
        Get agents within radius of an agent
        
        Args:
            agent_id: Agent to check around
            radius: Search radius in meters
            
        Returns:
            List of nearby agent IDs
        """
        spatial_agent = self.agents.get(agent_id)
        if not spatial_agent:
            return []
        
        nearby = []
        
        # Check grid cells around agent
        grid_x = int(spatial_agent.x / self.grid_size)
        grid_y = int(spatial_agent.y / self.grid_size)
        
        # Check 3x3 grid around agent
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = (grid_x + dx, grid_y + dy)
                if cell in self.agent_grid:
                    for other_id in self.agent_grid[cell]:
                        if other_id != agent_id:
                            other_agent = self.agents[other_id]
                            if spatial_agent.distance_to_agent(other_agent) <= radius:
                                nearby.append(other_id)
        
        return nearby
    
    def get_agents_at_location(self, location_id: int) -> List[int]:
        """Get all agents at a specific location"""
        location = self.locations.get(location_id)
        if not location:
            return []
        
        agents_at_location = []
        for agent_id, spatial_agent in self.agents.items():
            if location.contains_point(spatial_agent.x, spatial_agent.y):
                agents_at_location.append(agent_id)
        
        return agents_at_location
    
    def _update_agent_grid(self, agent_id: int):
        """Update agent's position in spatial grid"""
        spatial_agent = self.agents.get(agent_id)
        if not spatial_agent:
            return
        
        # Remove from old cell
        for cell_agents in self.agent_grid.values():
            cell_agents.discard(agent_id)
        
        # Add to new cell
        grid_x = int(spatial_agent.x / self.grid_size)
        grid_y = int(spatial_agent.y / self.grid_size)
        cell = (grid_x, grid_y)
        
        if cell not in self.agent_grid:
            self.agent_grid[cell] = set()
        
        self.agent_grid[cell].add(agent_id)
    
    def get_world_bounds(self) -> Tuple[float, float, float, float]:
        """Get world boundaries (x, y, width, height)"""
        return (0, 0, self.width, self.height)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert world to dictionary"""
        return {
            "width": self.width,
            "height": self.height,
            "locations": {lid: {
                "id": loc.location_id,
                "name": loc.name,
                "type": loc.location_type.value,
                "x": loc.x,
                "y": loc.y,
                "width": loc.width,
                "height": loc.height,
                "agents": len([a for a in self.agents.values() if loc.contains_point(a.x, a.y)])
            } for lid, loc in self.locations.items()},
            "agents": {aid: {
                "id": agent.agent_id,
                "x": agent.x,
                "y": agent.y,
                "is_moving": agent.is_moving,
                "location": agent.current_location_id
            } for aid, agent in self.agents.items()}
        }
