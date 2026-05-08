"""
SYNESTHESIA LAUNCHER
Complete GUI product - describe society, click GO, watch it live
"""

import pygame
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Initialize
load_dotenv()
pygame.init()

# Colors
BG_COLOR = (20, 20, 30)
PANEL_COLOR = (30, 30, 40)
BUTTON_COLOR = (60, 120, 200)
BUTTON_HOVER = (80, 140, 220)
TEXT_COLOR = (220, 220, 220)
INPUT_BG = (40, 40, 50)
INPUT_ACTIVE = (50, 50, 60)

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
    
    def draw(self, screen):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class InputBox:
    def __init__(self, x, y, width, height, font, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.placeholder = placeholder
        self.active = False
    
    def draw(self, screen):
        color = INPUT_ACTIVE if self.active else INPUT_BG
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        pygame.draw.rect(screen, (100, 100, 120), self.rect, 2, border_radius=4)
        
        display_text = self.text if self.text else self.placeholder
        text_color = TEXT_COLOR if self.text else (120, 120, 130)
        
        text_surface = self.font.render(display_text, True, text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif len(self.text) < 50:
                self.text += event.unicode
        return False

class SetupScreen:
    def __init__(self, width=1000, height=700):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Synesthesia - Setup")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Input boxes
        self.society_input = InputBox(150, 250, 700, 50, self.text_font, 
                                      "e.g., Tech startup city, Medieval village, Space station...")
        self.population_input = InputBox(150, 350, 200, 50, self.text_font, "100")
        
        # Buttons
        self.go_button = Button(350, 550, 300, 60, "🚀 GENERATE & GO", self.subtitle_font)
        
        # Presets
        self.preset_buttons = [
            Button(150, 450, 200, 40, "Tech Startup", self.small_font),
            Button(370, 450, 200, 40, "Small Town", self.small_font),
            Button(590, 450, 200, 40, "University", self.small_font),
        ]
        
        self.config = None
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.title_font.render("SYNESTHESIA", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)
        
        subtitle = self.subtitle_font.render("Mental Health Population Simulator", True, (150, 150, 160))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 130))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Society input
        label1 = self.text_font.render("What society do you want to simulate?", True, TEXT_COLOR)
        self.screen.blit(label1, (150, 220))
        self.society_input.draw(self.screen)
        
        # Population input
        label2 = self.text_font.render("Population size:", True, TEXT_COLOR)
        self.screen.blit(label2, (150, 320))
        self.population_input.draw(self.screen)
        
        # Presets
        preset_label = self.small_font.render("Quick presets:", True, (150, 150, 160))
        self.screen.blit(preset_label, (150, 420))
        for btn in self.preset_buttons:
            btn.draw(self.screen)
        
        # GO button
        self.go_button.draw(self.screen)
        
        # Instructions
        instructions = [
            "1. Describe the society you want to simulate",
            "2. Set population size (recommended: 50-200 for smooth performance)",
            "3. Click GO to generate and watch live!",
        ]
        y = 620
        for instruction in instructions:
            text = self.small_font.render(instruction, True, (120, 120, 130))
            self.screen.blit(text, (150, y))
            y += 25
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # Input boxes
            self.society_input.handle_event(event)
            if self.population_input.handle_event(event):
                # Enter pressed in population box
                return self.start_simulation()
            
            # GO button
            if self.go_button.handle_event(event):
                return self.start_simulation()
            
            # Preset buttons
            for i, btn in enumerate(self.preset_buttons):
                if btn.handle_event(event):
                    presets = [
                        "Tech startup city with burnout culture",
                        "Small rural town with tight-knit community",
                        "University campus during finals week"
                    ]
                    self.society_input.text = presets[i]
        
        return None
    
    def start_simulation(self):
        society = self.society_input.text.strip()
        if not society:
            society = "Modern city"
        
        try:
            population = int(self.population_input.text) if self.population_input.text else 100
            population = max(10, min(500, population))  # Clamp 10-500
        except:
            population = 100
        
        self.config = {
            "society_description": society,
            "population": population
        }
        
        return "start"
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            result = self.handle_events()
            
            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "start":
                return self.config
            
            self.draw()
            clock.tick(60)

def show_loading_screen(screen, message):
    """Show loading message"""
    screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    
    small_font = pygame.font.Font(None, 24)
    hint = small_font.render("This may take 30-60 seconds...", True, (150, 150, 160))
    hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(hint, hint_rect)
    
    pygame.display.flip()

def generate_and_run_simulation(config):
    """Generate society and run simulation"""
    from synesthesia.world.spatial_world import SpatialWorld, LocationType
    from synesthesia.world.movement_system import MovementSystem
    from synesthesia.world.society_orchestrator import SocietyOrchestrator
    from synesthesia.agent.agent import Agent
    from synesthesia.agent.state import MentalHealthState
    from synesthesia.visualization.visualizer import Visualizer
    from openai import OpenAI
    import random
    
    # Setup screen
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Synesthesia - Generating...")
    
    show_loading_screen(screen, "🧠 Generating society structure...")
    pygame.event.pump()
    
    # Initialize LLM
    llm_client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    
    # Generate society structure
    orchestrator = SocietyOrchestrator(llm_client)
    society_structure = orchestrator.generate_society_structure(
        config["society_description"],
        config["population"]
    )
    
    show_loading_screen(screen, "🌍 Creating spatial world...")
    pygame.event.pump()
    
    # Create spatial world
    spatial_world = SpatialWorld(width=1200, height=900)
    
    # Create locations based on society structure
    locations_config = society_structure.get('locations', {})
    location_objects = []
    
    x, y = 50, 50
    for loc_type, details in locations_config.items():
        count = details.get('count', 1)
        capacity = details.get('capacity', 50)
        
        for i in range(min(count, 15)):  # Max 15 locations per type
            try:
                location_type = LocationType[loc_type.upper()]
            except:
                location_type = LocationType.OTHER
            
            loc = spatial_world.create_location(
                name=f"{loc_type.title()} {i+1}",
                location_type=location_type,
                x=x, y=y,
                width=random.randint(60, 100),
                height=random.randint(60, 100),
                capacity=capacity
            )
            location_objects.append(loc)
            
            x += 120
            if x > 1000:
                x = 50
                y += 120
    
    show_loading_screen(screen, "👥 Creating population...")
    pygame.event.pump()
    
    # Create agents
    agents = {}
    roles = society_structure.get('roles', {})
    role_names = list(roles.keys()) if roles else ['worker', 'student', 'retiree']
    
    names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", 
             "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia",
             "Lucas", "Harper", "Henry", "Evelyn", "Alexander", "Abigail", "Michael",
             "Emily", "Daniel", "Elizabeth", "Matthew", "Sofia", "Jackson", "Avery",
             "Sebastian", "Ella", "Jack", "Scarlett", "Aiden", "Grace", "Owen", "Chloe",
             "Samuel", "Victoria", "David", "Riley", "Joseph", "Aria", "Carter", "Lily",
             "Wyatt", "Aubrey", "John", "Zoey", "Luke"]
    
    for i in range(config["population"]):
        role = random.choice(role_names)
        role_info = roles.get(role, {})
        
        work_hours = role_info.get('work_hours', [9, 17])
        if isinstance(work_hours, list) and len(work_hours) == 2:
            work_hours = list(range(work_hours[0], work_hours[1]))
        else:
            work_hours = list(range(9, 17))
        
        agent = Agent(
            agent_id=i,
            name=f"{names[i % len(names)]} {i // len(names) + 1}" if i >= len(names) else names[i],
            age=random.randint(18, 65),
            role=role,
            personality_traits=["friendly", "hardworking"],
            mental_health=MentalHealthState(
                anxiety=random.uniform(0.2, 0.6),
                depression=random.uniform(0.1, 0.4),
                stress=random.uniform(0.3, 0.7),
                wellbeing=random.uniform(0.4, 0.8)
            ),
            work_hours=work_hours,
            sleep_hours=list(range(23, 24)) + list(range(0, 7))
        )
        
        agents[i] = agent
        
        # Add to spatial world
        if location_objects:
            start_loc = random.choice(location_objects)
            x, y = start_loc.get_random_point_inside()
        else:
            x, y = random.uniform(100, 1100), random.uniform(100, 800)
        
        spatial_world.add_agent(i, x, y, speed=random.uniform(1.5, 2.5))
    
    show_loading_screen(screen, "🚀 Starting simulation...")
    pygame.event.pump()
    
    # Create movement system
    movement_system = MovementSystem(spatial_world)
    
    # Give agents initial destinations
    for agent_id in agents.keys():
        if location_objects:
            target_loc = random.choice(location_objects)
            movement_system.move_agent_to_location(agent_id, target_loc.location_id)
    
    # Create visualizer
    visualizer = Visualizer(
        spatial_world=spatial_world,
        agents=agents,
        width=1200,
        height=800,
        title=f"Synesthesia - {config['society_description']}"
    )
    
    # Run simulation
    sim_time = datetime.now()
    time_scale = 60.0
    running = True
    
    print(f"\n{'='*60}")
    print(f"🚀 SIMULATION STARTED")
    print(f"{'='*60}")
    print(f"Society: {config['society_description']}")
    print(f"Population: {config['population']}")
    print(f"Locations: {len(location_objects)}")
    print(f"{'='*60}\n")
    
    while running:
        running = visualizer.handle_events()
        
        delta_time_real = visualizer.tick(60)
        
        if not visualizer.paused:
            delta_time_sim = delta_time_real * time_scale
            from datetime import timedelta
            sim_time += timedelta(seconds=delta_time_sim)
            
            movement_system.update(delta_time_sim)
            
            # Give new destinations to idle agents
            for agent_id, spatial_agent in spatial_world.agents.items():
                if not spatial_agent.is_moving and location_objects:
                    target_loc = random.choice(location_objects)
                    movement_system.move_agent_to_location(agent_id, target_loc.location_id)
        
        visualizer.render(sim_time, visualizer.clock.get_fps())
    
    visualizer.quit()

def main():
    """Main launcher"""
    print("\n" + "="*60)
    print("SYNESTHESIA LAUNCHER")
    print("="*60)
    print("Starting GUI setup...")
    print("="*60 + "\n")
    
    # Check API key
    if not os.getenv("LLM_API_KEY"):
        print("❌ ERROR: LLM_API_KEY not found in .env file")
        print("Please add your NVIDIA API key to .env")
        sys.exit(1)
    
    # Run setup screen
    setup = SetupScreen()
    config = setup.run()
    
    # Generate and run simulation
    generate_and_run_simulation(config)
    
    print("\n✅ Simulation complete!")

if __name__ == "__main__":
    main()
