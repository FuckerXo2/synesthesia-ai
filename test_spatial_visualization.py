"""
Test Spatial Visualization - See agents moving in 2D space
"""

import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

from synesthesia.world.spatial_world import SpatialWorld, LocationType
from synesthesia.world.movement_system import MovementSystem
from synesthesia.agent.agent import Agent
from synesthesia.agent.state import MentalHealthState
from synesthesia.visualization.visualizer import Visualizer

load_dotenv()


def create_test_world():
    """Create a test world with locations"""
    world = SpatialWorld(width=800, height=600)
    
    # Create a small city layout
    # Residential area (left side)
    for i in range(3):
        for j in range(2):
            world.create_location(
                name=f"Home {i*2 + j + 1}",
                location_type=LocationType.HOME,
                x=50 + i * 80,
                y=50 + j * 100,
                width=60,
                height=80,
                capacity=5
            )
    
    # Office buildings (center)
    for i in range(2):
        world.create_location(
            name=f"Office {i + 1}",
            location_type=LocationType.WORKPLACE,
            x=350 + i * 120,
            y=100,
            width=100,
            height=150,
            capacity=30
        )
    
    # Park (bottom center)
    world.create_location(
        name="Central Park",
        location_type=LocationType.PARK,
        x=300,
        y=400,
        width=200,
        height=150,
        capacity=50
    )
    
    # Stores (right side)
    world.create_location(
        name="Grocery Store",
        location_type=LocationType.STORE,
        x=650,
        y=100,
        width=100,
        height=80,
        capacity=20
    )
    
    world.create_location(
        name="Coffee Shop",
        location_type=LocationType.RESTAURANT,
        x=650,
        y=200,
        width=100,
        height=60,
        capacity=15
    )
    
    # Gym (right bottom)
    world.create_location(
        name="Fitness Center",
        location_type=LocationType.GYM,
        x=650,
        y=400,
        width=100,
        height=100,
        capacity=25
    )
    
    print(f"✅ Created world with {len(world.locations)} locations")
    return world


def create_test_agents(num_agents: int = 30):
    """Create test agents"""
    agents = {}
    
    roles = ["engineer", "designer", "manager", "student", "teacher"]
    names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
        "Iris", "Jack", "Kate", "Leo", "Maya", "Noah", "Olivia", "Peter",
        "Quinn", "Rachel", "Sam", "Tara", "Uma", "Victor", "Wendy", "Xander",
        "Yara", "Zack", "Amy", "Ben", "Cara", "Dan"
    ]
    
    for i in range(num_agents):
        # Random mental health state
        anxiety = random.uniform(0.2, 0.8)
        depression = random.uniform(0.1, 0.6)
        stress = random.uniform(0.3, 0.9)
        wellbeing = random.uniform(0.3, 0.8)
        
        agent = Agent(
            agent_id=i,
            name=names[i % len(names)] + f" {i // len(names) + 1}" if i >= len(names) else names[i],
            age=random.randint(22, 55),
            role=random.choice(roles),
            personality_traits=["friendly", "hardworking"],
            mental_health=MentalHealthState(
                anxiety=anxiety,
                depression=depression,
                stress=stress,
                wellbeing=wellbeing
            ),
            work_hours=list(range(9, 17)),
            sleep_hours=list(range(23, 24)) + list(range(0, 7))
        )
        
        agents[i] = agent
    
    print(f"✅ Created {num_agents} agents")
    return agents


def main():
    """Run spatial visualization test"""
    print("="*60)
    print("SPATIAL VISUALIZATION TEST")
    print("="*60)
    
    # Create world
    spatial_world = create_test_world()
    
    # Create agents
    agents = create_test_agents(30)
    
    # Add agents to spatial world at random positions
    homes = [loc for loc in spatial_world.locations.values() if loc.location_type == LocationType.HOME]
    
    for agent_id, agent in agents.items():
        # Start at a random home
        home = random.choice(homes)
        x, y = home.get_random_point_inside()
        
        spatial_world.add_agent(agent_id, x, y, speed=random.uniform(1.5, 2.5))
    
    # Create movement system
    movement_system = MovementSystem(spatial_world)
    
    # Give agents random destinations
    all_locations = list(spatial_world.locations.values())
    for agent_id in agents.keys():
        target_location = random.choice(all_locations)
        movement_system.move_agent_to_location(agent_id, target_location.location_id)
    
    # Create visualizer
    visualizer = Visualizer(
        spatial_world=spatial_world,
        agents=agents,
        width=1200,
        height=800,
        title="Synesthesia - Spatial Test"
    )
    
    # Simulation loop
    sim_time = datetime.now()
    time_scale = 60.0  # 1 real second = 60 sim seconds
    running = True
    
    print("\n🎮 Starting visualization...")
    print("   Controls:")
    print("   - WASD/Arrows: Move camera")
    print("   - Mouse wheel: Zoom")
    print("   - Click: Select agent")
    print("   - SPACE: Pause")
    print("   - L: Toggle labels")
    print("   - P: Toggle paths")
    print("   - ESC: Quit")
    print()
    
    frame_count = 0
    
    while running:
        # Handle events
        running = visualizer.handle_events()
        
        # Get delta time
        delta_time_real = visualizer.tick(60)  # 60 FPS
        
        if not visualizer.paused:
            # Update simulation time
            delta_time_sim = delta_time_real * time_scale
            sim_time += timedelta(seconds=delta_time_sim)
            
            # Update movement
            movement_system.update(delta_time_sim)
            
            # Give new destinations to agents who reached their target
            for agent_id, spatial_agent in spatial_world.agents.items():
                if not spatial_agent.is_moving:
                    # Pick random destination
                    target_location = random.choice(all_locations)
                    movement_system.move_agent_to_location(agent_id, target_location.location_id)
        
        # Render
        visualizer.render(sim_time, visualizer.clock.get_fps())
        
        frame_count += 1
    
    # Cleanup
    visualizer.quit()
    
    print("\n✅ Visualization test complete!")
    print(f"   Rendered {frame_count} frames")


if __name__ == "__main__":
    main()
