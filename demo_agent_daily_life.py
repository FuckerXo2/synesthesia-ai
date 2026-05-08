"""
Demo: Watch Agents Live Their Daily Lives
Shows what agents are doing throughout the day (text-based)
"""

import random
from datetime import datetime, timedelta
from synesthesia.agent.agent import Agent
from synesthesia.agent.state import MentalHealthState
from synesthesia.world.location import World, Location, LocationType

def create_simple_world():
    """Create a simple world"""
    world = World()
    
    # Create locations
    locations = {
        'home': world.create_location("Home", LocationType.HOME, capacity=5),
        'office': world.create_location("Tech Office", LocationType.WORKPLACE, capacity=30),
        'park': world.create_location("Central Park", LocationType.PARK, capacity=50),
        'gym': world.create_location("Fitness Center", LocationType.GYM, capacity=20),
        'cafe': world.create_location("Coffee Shop", LocationType.RESTAURANT, capacity=15),
        'store': world.create_location("Grocery Store", LocationType.STORE, capacity=20)
    }
    
    return world, locations

def create_agents(num_agents=5):
    """Create sample agents"""
    names = ["Sarah", "Alex", "Emma", "Michael", "Olivia"]
    roles = ["Engineer", "Designer", "Manager", "Teacher", "Student"]
    
    agents = []
    for i in range(num_agents):
        agent = Agent(
            agent_id=i,
            name=names[i],
            age=random.randint(24, 45),
            role=roles[i],
            personality_traits=["friendly", "hardworking"],
            mental_health=MentalHealthState(
                anxiety=random.uniform(0.3, 0.7),
                depression=random.uniform(0.2, 0.5),
                stress=random.uniform(0.4, 0.8),
                wellbeing=random.uniform(0.4, 0.7)
            ),
            work_hours=list(range(9, 17)),
            sleep_hours=list(range(23, 24)) + list(range(0, 7))
        )
        agents.append(agent)
    
    return agents

def get_activity(agent, hour, locations):
    """Determine what agent is doing at this hour"""
    
    # Sleep time
    if hour in agent.sleep_hours:
        return "😴 Sleeping at home", locations['home'], "💤"
    
    # Work time
    if hour in agent.work_hours:
        activities = [
            ("💼 Working at desk", locations['office'], "⌨️"),
            ("☕ Coffee break", locations['office'], "☕"),
            ("📊 In meeting", locations['office'], "👥"),
            ("💻 Coding", locations['office'], "🖥️"),
        ]
        return random.choice(activities)
    
    # Free time
    free_activities = [
        ("🏃 Exercising", locations['gym'], "💪"),
        ("🌳 Walking in park", locations['park'], "🚶"),
        ("☕ Getting coffee", locations['cafe'], "☕"),
        ("🛒 Shopping", locations['store'], "🛍️"),
        ("📺 Relaxing at home", locations['home'], "🏠"),
        ("📖 Reading at home", locations['home'], "📚"),
    ]
    return random.choice(free_activities)

def get_mental_health_emoji(agent):
    """Get emoji for mental health state"""
    category = agent.mental_health.category.value
    
    if category == "thriving":
        return "🟢"
    elif category == "stable":
        return "🔵"
    elif category == "struggling":
        return "🟡"
    else:  # crisis
        return "🔴"

def simulate_day(agents, world, locations):
    """Simulate one day"""
    print("\n" + "="*80)
    print("📅 SIMULATING ONE DAY IN THE LIFE")
    print("="*80)
    
    current_time = datetime.now().replace(hour=6, minute=0, second=0)
    
    # Simulate every 2 hours
    for _ in range(10):  # 6am to midnight
        hour = current_time.hour
        
        print(f"\n⏰ {current_time.strftime('%I:%M %p')}")
        print("-" * 80)
        
        for agent in agents:
            activity, location, emoji = get_activity(agent, hour, locations)
            mh_emoji = get_mental_health_emoji(agent)
            
            # Update mental health based on activity
            if "Working" in activity or "meeting" in activity:
                agent.mental_health.stress += 0.02
                agent.mental_health.anxiety += 0.01
            elif "Exercising" in activity or "park" in activity:
                agent.mental_health.stress -= 0.03
                agent.mental_health.wellbeing += 0.02
            elif "Sleeping" in activity:
                agent.mental_health.stress -= 0.05
                agent.mental_health.wellbeing += 0.03
            elif "coffee" in activity.lower() or "Relaxing" in activity:
                agent.mental_health.wellbeing += 0.01
            
            # Clamp values
            agent.mental_health.anxiety = max(0, min(1, agent.mental_health.anxiety))
            agent.mental_health.stress = max(0, min(1, agent.mental_health.stress))
            agent.mental_health.wellbeing = max(0, min(1, agent.mental_health.wellbeing))
            
            print(f"  {emoji} {agent.name:12} {mh_emoji} | {activity:30} | "
                  f"Stress: {agent.mental_health.stress:.2f} | "
                  f"Wellbeing: {agent.mental_health.wellbeing:.2f}")
        
        current_time += timedelta(hours=2)
    
    print("\n" + "="*80)
    print("📊 END OF DAY SUMMARY")
    print("="*80)
    
    for agent in agents:
        mh_emoji = get_mental_health_emoji(agent)
        print(f"{mh_emoji} {agent.name:12} | "
              f"Anxiety: {agent.mental_health.anxiety:.2f} | "
              f"Stress: {agent.mental_health.stress:.2f} | "
              f"Wellbeing: {agent.mental_health.wellbeing:.2f} | "
              f"State: {agent.mental_health.category.value}")

def main():
    """Run the demo"""
    print("\n" + "="*80)
    print("🌍 SYNESTHESIA: DAILY LIFE DEMO")
    print("="*80)
    print("\nWatch 5 agents live their daily lives!")
    print("Mental health is tracked in the background as they:")
    print("  • Go to work")
    print("  • Exercise")
    print("  • Socialize")
    print("  • Relax")
    print("  • Sleep")
    print("\nLegend:")
    print("  🟢 Thriving  🔵 Stable  🟡 Struggling  🔴 Crisis")
    print("="*80)
    
    # Create world and agents
    world, locations = create_simple_world()
    agents = create_agents(5)
    
    # Simulate one day
    simulate_day(agents, world, locations)
    
    print("\n✅ Demo complete!")
    print("\nKey takeaway:")
    print("  Agents live NORMAL LIVES - work, exercise, socialize, sleep.")
    print("  Mental health is just ONE STAT tracked in the background.")
    print("  It's like The Sims, but focused on mental health patterns.")

if __name__ == "__main__":
    main()
