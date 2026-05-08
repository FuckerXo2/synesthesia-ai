"""
Movement System - Pathfinding and navigation for agents
Implements A* pathfinding for realistic movement around obstacles
"""

import heapq
import math
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass

from synesthesia.world.spatial_world import SpatialWorld, SpatialLocation


@dataclass
class PathNode:
    """Node in pathfinding graph"""
    x: float
    y: float
    g_cost: float = float('inf')  # Cost from start
    h_cost: float = 0.0  # Heuristic cost to goal
    parent: Optional['PathNode'] = None
    
    @property
    def f_cost(self) -> float:
        """Total cost (g + h)"""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        if not isinstance(other, PathNode):
            return False
        return abs(self.x - other.x) < 0.1 and abs(self.y - other.y) < 0.1
    
    def __hash__(self):
        return hash((round(self.x, 1), round(self.y, 1)))


class Pathfinder:
    """
    A* pathfinding for agents
    Finds optimal paths around obstacles
    """
    
    def __init__(self, world: SpatialWorld):
        """
        Initialize pathfinder
        
        Args:
            world: Spatial world to navigate
        """
        self.world = world
        self.grid_resolution = 2.0  # Grid cell size for pathfinding (meters)
    
    def find_path(
        self,
        start_x: float,
        start_y: float,
        goal_x: float,
        goal_y: float,
        avoid_agents: bool = True
    ) -> List[Tuple[float, float]]:
        """
        Find path from start to goal using A*
        
        Args:
            start_x, start_y: Start position
            goal_x, goal_y: Goal position
            avoid_agents: Whether to avoid other agents
            
        Returns:
            List of waypoints [(x, y), ...]
        """
        # Check if direct path is possible
        if self._is_direct_path_clear(start_x, start_y, goal_x, goal_y):
            return [(goal_x, goal_y)]
        
        # A* pathfinding
        start_node = PathNode(start_x, start_y, g_cost=0.0)
        goal_node = PathNode(goal_x, goal_y)
        
        start_node.h_cost = self._heuristic(start_node, goal_node)
        
        open_set = [start_node]
        closed_set: Set[PathNode] = set()
        
        max_iterations = 1000
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            
            # Get node with lowest f_cost
            current = heapq.heappop(open_set)
            
            # Check if reached goal
            if self._distance(current.x, current.y, goal_x, goal_y) < self.grid_resolution:
                return self._reconstruct_path(current, goal_x, goal_y)
            
            closed_set.add(current)
            
            # Check neighbors
            for neighbor in self._get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Check if neighbor is walkable
                if not self._is_walkable(neighbor.x, neighbor.y):
                    continue
                
                # Calculate g_cost
                tentative_g = current.g_cost + self._distance(
                    current.x, current.y, neighbor.x, neighbor.y
                )
                
                # Check if this path is better
                if tentative_g < neighbor.g_cost:
                    neighbor.parent = current
                    neighbor.g_cost = tentative_g
                    neighbor.h_cost = self._heuristic(neighbor, goal_node)
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        # No path found - return direct path as fallback
        print(f"⚠️  No path found after {iterations} iterations, using direct path")
        return [(goal_x, goal_y)]
    
    def _is_direct_path_clear(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        """Check if direct path between two points is clear"""
        # Sample points along the line
        distance = self._distance(x1, y1, x2, y2)
        num_samples = int(distance / self.grid_resolution) + 1
        
        for i in range(num_samples + 1):
            t = i / num_samples if num_samples > 0 else 0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            
            if not self._is_walkable(x, y):
                return False
        
        return True
    
    def _is_walkable(self, x: float, y: float) -> bool:
        """Check if a position is walkable (not blocked by obstacles)"""
        # Check world bounds
        if x < 0 or x >= self.world.width or y < 0 or y >= self.world.height:
            return False
        
        # Check location obstacles
        for location in self.world.locations.values():
            for obstacle in location.obstacles:
                ox, oy, ow, oh = obstacle
                if (ox <= x <= ox + ow and oy <= y <= oy + oh):
                    return False
        
        return True
    
    def _get_neighbors(self, node: PathNode) -> List[PathNode]:
        """Get neighboring nodes (8-directional)"""
        neighbors = []
        
        # 8 directions
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for dx, dy in directions:
            x = node.x + dx * self.grid_resolution
            y = node.y + dy * self.grid_resolution
            neighbors.append(PathNode(x, y))
        
        return neighbors
    
    def _heuristic(self, node: PathNode, goal: PathNode) -> float:
        """Heuristic function (Euclidean distance)"""
        return self._distance(node.x, node.y, goal.x, goal.y)
    
    def _distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance"""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)
    
    def _reconstruct_path(self, node: PathNode, goal_x: float, goal_y: float) -> List[Tuple[float, float]]:
        """Reconstruct path from goal to start"""
        path = [(goal_x, goal_y)]
        current = node
        
        while current.parent is not None:
            path.append((current.x, current.y))
            current = current.parent
        
        path.reverse()
        
        # Simplify path (remove unnecessary waypoints)
        return self._simplify_path(path)
    
    def _simplify_path(self, path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Simplify path by removing unnecessary waypoints
        Uses line-of-sight to skip intermediate points
        """
        if len(path) <= 2:
            return path
        
        simplified = [path[0]]
        current_index = 0
        
        while current_index < len(path) - 1:
            # Try to skip as many waypoints as possible
            farthest_visible = current_index + 1
            
            for i in range(current_index + 2, len(path)):
                if self._is_direct_path_clear(
                    path[current_index][0], path[current_index][1],
                    path[i][0], path[i][1]
                ):
                    farthest_visible = i
                else:
                    break
            
            simplified.append(path[farthest_visible])
            current_index = farthest_visible
        
        return simplified


class MovementSystem:
    """
    High-level movement system for agents
    Handles movement requests and coordinates pathfinding
    """
    
    def __init__(self, world: SpatialWorld):
        """
        Initialize movement system
        
        Args:
            world: Spatial world
        """
        self.world = world
        self.pathfinder = Pathfinder(world)
    
    def move_agent_to_position(self, agent_id: int, target_x: float, target_y: float):
        """
        Move agent to a specific position
        Finds path and sets agent on course
        
        Args:
            agent_id: Agent to move
            target_x, target_y: Target position
        """
        spatial_agent = self.world.get_agent(agent_id)
        if not spatial_agent:
            return False
        
        # Find path
        path = self.pathfinder.find_path(
            spatial_agent.x, spatial_agent.y,
            target_x, target_y
        )
        
        # Set agent path
        spatial_agent.set_path(path)
        
        return True
    
    def move_agent_to_location(self, agent_id: int, location_id: int):
        """
        Move agent to a location
        Finds path to location's entry point
        
        Args:
            agent_id: Agent to move
            location_id: Target location
        """
        spatial_agent = self.world.get_agent(agent_id)
        location = self.world.get_location(location_id)
        
        if not spatial_agent or not location:
            return False
        
        # Get entry point
        entry_point = location.get_nearest_entry_point(spatial_agent.x, spatial_agent.y)
        
        # Find path
        path = self.pathfinder.find_path(
            spatial_agent.x, spatial_agent.y,
            entry_point[0], entry_point[1]
        )
        
        # Set agent path
        spatial_agent.set_path(path)
        spatial_agent.current_location_id = location_id
        
        return True
    
    def update(self, delta_time: float):
        """
        Update all agent movement
        
        Args:
            delta_time: Time elapsed (seconds)
        """
        for agent_id in self.world.agents.keys():
            self.world.update_agent(agent_id, delta_time)
    
    def stop_agent(self, agent_id: int):
        """Stop agent movement"""
        spatial_agent = self.world.get_agent(agent_id)
        if spatial_agent:
            spatial_agent.is_moving = False
            spatial_agent.target_x = None
            spatial_agent.target_y = None
            spatial_agent.path = []
            spatial_agent.vx = 0.0
            spatial_agent.vy = 0.0
