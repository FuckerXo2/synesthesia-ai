"""
Location System - Physical places in the world where agents can be
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum


class LocationType(Enum):
    """Types of locations in the world"""
    HOME = "home"
    WORKPLACE = "workplace"
    SCHOOL = "school"
    STORE = "store"
    RESTAURANT = "restaurant"
    PARK = "park"
    GYM = "gym"
    HOSPITAL = "hospital"
    THERAPY_OFFICE = "therapy_office"
    COMMUNITY_CENTER = "community_center"
    COURTHOUSE = "courthouse"
    GOVERNMENT_BUILDING = "government_building"
    TRANSIT = "transit"  # Bus, train, car
    STREET = "street"
    OTHER = "other"


@dataclass
class Location:
    """A physical location in the world"""
    location_id: int
    name: str
    location_type: LocationType
    capacity: int = 100  # Max agents that can be here
    
    # Spatial coordinates (for visualization)
    x: float = 0.0
    y: float = 0.0
    
    # Agents currently at this location
    agents_present: Set[int] = field(default_factory=set)
    
    # Metadata
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    def add_agent(self, agent_id: int) -> bool:
        """Add an agent to this location"""
        if len(self.agents_present) >= self.capacity:
            return False
        self.agents_present.add(agent_id)
        return True
    
    def remove_agent(self, agent_id: int):
        """Remove an agent from this location"""
        self.agents_present.discard(agent_id)
    
    def is_full(self) -> bool:
        """Check if location is at capacity"""
        return len(self.agents_present) >= self.capacity
    
    def get_nearby_agents(self, agent_id: int) -> List[int]:
        """Get other agents at this location (excluding the given agent)"""
        return [aid for aid in self.agents_present if aid != agent_id]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "location_id": self.location_id,
            "name": self.name,
            "location_type": self.location_type.value,
            "capacity": self.capacity,
            "x": self.x,
            "y": self.y,
            "agents_present": list(self.agents_present),
            "description": self.description,
            "tags": self.tags
        }


class World:
    """The physical world containing all locations"""
    
    def __init__(self):
        self.locations: Dict[int, Location] = {}
        self.location_id_counter = 0
        
        # Spatial index for fast proximity queries
        self.location_by_type: Dict[LocationType, List[int]] = {}
    
    def create_location(
        self,
        name: str,
        location_type: LocationType,
        x: float = 0.0,
        y: float = 0.0,
        capacity: int = 100,
        description: str = "",
        tags: List[str] = None
    ) -> Location:
        """Create a new location in the world"""
        location = Location(
            location_id=self.location_id_counter,
            name=name,
            location_type=location_type,
            capacity=capacity,
            x=x,
            y=y,
            description=description,
            tags=tags or []
        )
        
        self.locations[location.location_id] = location
        self.location_id_counter += 1
        
        # Add to spatial index
        if location_type not in self.location_by_type:
            self.location_by_type[location_type] = []
        self.location_by_type[location_type].append(location.location_id)
        
        return location
    
    def get_location(self, location_id: int) -> Optional[Location]:
        """Get a location by ID"""
        return self.locations.get(location_id)
    
    def get_locations_by_type(self, location_type: LocationType) -> List[Location]:
        """Get all locations of a specific type"""
        location_ids = self.location_by_type.get(location_type, [])
        return [self.locations[lid] for lid in location_ids if lid in self.locations]
    
    def find_nearest_location(
        self,
        x: float,
        y: float,
        location_type: Optional[LocationType] = None
    ) -> Optional[Location]:
        """Find the nearest location to a point"""
        candidates = self.locations.values()
        if location_type:
            candidates = self.get_locations_by_type(location_type)
        
        if not candidates:
            return None
        
        # Simple distance calculation
        def distance(loc: Location) -> float:
            return ((loc.x - x) ** 2 + (loc.y - y) ** 2) ** 0.5
        
        return min(candidates, key=distance)
    
    def move_agent(
        self,
        agent_id: int,
        from_location_id: Optional[int],
        to_location_id: int
    ) -> bool:
        """Move an agent from one location to another"""
        # Remove from old location
        if from_location_id is not None:
            old_location = self.get_location(from_location_id)
            if old_location:
                old_location.remove_agent(agent_id)
        
        # Add to new location
        new_location = self.get_location(to_location_id)
        if new_location:
            return new_location.add_agent(agent_id)
        
        return False
    
    def get_agents_at_location(self, location_id: int) -> List[int]:
        """Get all agents at a specific location"""
        location = self.get_location(location_id)
        return list(location.agents_present) if location else []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert world to dictionary"""
        return {
            "locations": {lid: loc.to_dict() for lid, loc in self.locations.items()},
            "total_locations": len(self.locations)
        }
