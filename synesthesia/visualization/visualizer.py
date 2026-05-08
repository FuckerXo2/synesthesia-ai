"""
2D Visualization - Pygame renderer for spatial world
GTA-style top-down view with agents moving through space
"""

import pygame
import math
from typing import Dict, Optional, Tuple, List
from datetime import datetime

from synesthesia.world.spatial_world import SpatialWorld, SpatialLocation, LocationType
from synesthesia.agent.agent import Agent
from synesthesia.agent.state import MentalHealthCategory


# Colors
COLOR_BACKGROUND = (20, 20, 30)
COLOR_GRID = (40, 40, 50)
COLOR_TEXT = (200, 200, 200)
COLOR_TEXT_DARK = (100, 100, 100)

# Mental health colors
COLOR_THRIVING = (50, 200, 50)      # Green
COLOR_STABLE = (100, 150, 255)      # Blue
COLOR_STRUGGLING = (255, 200, 50)   # Yellow
COLOR_CRISIS = (255, 50, 50)        # Red

# Location colors by type
LOCATION_COLORS = {
    LocationType.HOME: (100, 80, 60),
    LocationType.WORKPLACE: (80, 80, 120),
    LocationType.SCHOOL: (120, 100, 80),
    LocationType.PARK: (60, 120, 60),
    LocationType.RESTAURANT: (140, 100, 60),
    LocationType.HOSPITAL: (200, 80, 80),
    LocationType.GYM: (100, 140, 100),
    LocationType.STORE: (120, 120, 80),
    LocationType.OTHER: (80, 80, 80)
}


class Camera:
    """Camera for panning and zooming"""
    
    def __init__(self, width: int, height: int):
        self.x = 0.0
        self.y = 0.0
        self.zoom = 1.0
        self.width = width
        self.height = height
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = int((world_x - self.x) * self.zoom)
        screen_y = int((world_y - self.y) * self.zoom)
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x / self.zoom + self.x
        world_y = screen_y / self.zoom + self.y
        return (world_x, world_y)
    
    def move(self, dx: float, dy: float):
        """Move camera"""
        self.x += dx / self.zoom
        self.y += dy / self.zoom
    
    def zoom_at(self, screen_x: int, screen_y: int, zoom_delta: float):
        """Zoom camera at a specific screen position"""
        # Get world position before zoom
        world_x, world_y = self.screen_to_world(screen_x, screen_y)
        
        # Apply zoom
        self.zoom *= zoom_delta
        self.zoom = max(0.1, min(5.0, self.zoom))  # Clamp zoom
        
        # Adjust camera to keep world position under cursor
        new_world_x, new_world_y = self.screen_to_world(screen_x, screen_y)
        self.x += world_x - new_world_x
        self.y += world_y - new_world_y


class Visualizer:
    """
    2D visualization of spatial world using Pygame
    """
    
    def __init__(
        self,
        spatial_world: SpatialWorld,
        agents: Dict[int, Agent],
        width: int = 1200,
        height: int = 800,
        title: str = "Synesthesia - Mental Health Simulation"
    ):
        """
        Initialize visualizer
        
        Args:
            spatial_world: Spatial world to visualize
            agents: Dictionary of agents (agent_id -> Agent)
            width: Window width
            height: Window height
            title: Window title
        """
        self.spatial_world = spatial_world
        self.agents = agents
        self.width = width
        self.height = height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        # Camera
        self.camera = Camera(width, height)
        
        # Center camera on world
        self.camera.x = -width / 2 / self.camera.zoom
        self.camera.y = -height / 2 / self.camera.zoom
        
        # Font
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        # UI state
        self.selected_agent_id: Optional[int] = None
        self.show_labels = True
        self.show_paths = True
        self.paused = False
        
        # Camera control
        self.camera_drag = False
        self.last_mouse_pos = (0, 0)
        
        print(f"🎮 Visualizer initialized: {width}x{height}")
    
    def handle_events(self) -> bool:
        """
        Handle pygame events
        
        Returns:
            False if should quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_l:
                    self.show_labels = not self.show_labels
                elif event.key == pygame.K_p:
                    self.show_paths = not self.show_paths
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_left_click(event.pos)
                elif event.button == 2:  # Middle click
                    self.camera_drag = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:  # Scroll up
                    self.camera.zoom_at(event.pos[0], event.pos[1], 1.1)
                elif event.button == 5:  # Scroll down
                    self.camera.zoom_at(event.pos[0], event.pos[1], 0.9)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:  # Middle click
                    self.camera_drag = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.camera_drag:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.camera.move(-dx, -dy)
                    self.last_mouse_pos = event.pos
        
        # Keyboard camera control
        keys = pygame.key.get_pressed()
        camera_speed = 5.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera.move(-camera_speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera.move(camera_speed, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera.move(0, -camera_speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera.move(0, camera_speed)
        
        return True
    
    def _handle_left_click(self, pos: Tuple[int, int]):
        """Handle left click - select agent"""
        world_x, world_y = self.camera.screen_to_world(pos[0], pos[1])
        
        # Find closest agent
        closest_agent_id = None
        closest_distance = 10.0  # Max click distance
        
        for agent_id, spatial_agent in self.spatial_world.agents.items():
            distance = math.sqrt(
                (spatial_agent.x - world_x) ** 2 +
                (spatial_agent.y - world_y) ** 2
            )
            if distance < closest_distance:
                closest_distance = distance
                closest_agent_id = agent_id
        
        self.selected_agent_id = closest_agent_id
    
    def render(self, current_time: datetime, fps: float):
        """
        Render the world
        
        Args:
            current_time: Current simulation time
            fps: Current FPS
        """
        # Clear screen
        self.screen.fill(COLOR_BACKGROUND)
        
        # Draw grid
        self._draw_grid()
        
        # Draw locations
        self._draw_locations()
        
        # Draw agent paths
        if self.show_paths:
            self._draw_paths()
        
        # Draw agents
        self._draw_agents()
        
        # Draw UI
        self._draw_ui(current_time, fps)
        
        # Draw selected agent details
        if self.selected_agent_id is not None:
            self._draw_agent_details()
        
        # Update display
        pygame.display.flip()
    
    def _draw_grid(self):
        """Draw background grid"""
        grid_size = 50.0
        
        # Calculate visible grid range
        start_x = int(self.camera.x / grid_size) * grid_size
        end_x = start_x + self.width / self.camera.zoom + grid_size
        start_y = int(self.camera.y / grid_size) * grid_size
        end_y = start_y + self.height / self.camera.zoom + grid_size
        
        # Draw vertical lines
        x = start_x
        while x <= end_x:
            screen_x, _ = self.camera.world_to_screen(x, 0)
            if 0 <= screen_x <= self.width:
                pygame.draw.line(self.screen, COLOR_GRID, (screen_x, 0), (screen_x, self.height), 1)
            x += grid_size
        
        # Draw horizontal lines
        y = start_y
        while y <= end_y:
            _, screen_y = self.camera.world_to_screen(0, y)
            if 0 <= screen_y <= self.height:
                pygame.draw.line(self.screen, COLOR_GRID, (0, screen_y), (self.width, screen_y), 1)
            y += grid_size
    
    def _draw_locations(self):
        """Draw all locations"""
        for location in self.spatial_world.locations.values():
            # Get screen coordinates
            x1, y1 = self.camera.world_to_screen(location.x, location.y)
            x2, y2 = self.camera.world_to_screen(
                location.x + location.width,
                location.y + location.height
            )
            
            # Skip if off-screen
            if x2 < 0 or x1 > self.width or y2 < 0 or y1 > self.height:
                continue
            
            # Get color
            color = LOCATION_COLORS.get(location.location_type, COLOR_GRID)
            
            # Draw rectangle
            rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (color[0] + 40, color[1] + 40, color[2] + 40), rect, 2)
            
            # Draw label
            if self.show_labels and self.camera.zoom > 0.5:
                label = self.font_small.render(location.name, True, COLOR_TEXT)
                label_rect = label.get_rect(center=((x1 + x2) // 2, (y1 + y2) // 2))
                self.screen.blit(label, label_rect)
    
    def _draw_agents(self):
        """Draw all agents"""
        for agent_id, spatial_agent in self.spatial_world.agents.items():
            # Get screen position
            screen_x, screen_y = self.camera.world_to_screen(spatial_agent.x, spatial_agent.y)
            
            # Skip if off-screen
            if screen_x < -20 or screen_x > self.width + 20 or screen_y < -20 or screen_y > self.height + 20:
                continue
            
            # Get agent
            agent = self.agents.get(agent_id)
            if not agent:
                continue
            
            # Get color based on mental health
            color = self._get_mental_health_color(agent)
            
            # Draw agent circle
            radius = max(3, int(5 * self.camera.zoom))
            pygame.draw.circle(self.screen, color, (screen_x, screen_y), radius)
            
            # Draw selection indicator
            if agent_id == self.selected_agent_id:
                pygame.draw.circle(self.screen, (255, 255, 255), (screen_x, screen_y), radius + 3, 2)
            
            # Draw name label
            if self.show_labels and self.camera.zoom > 1.0:
                label = self.font_small.render(agent.name, True, COLOR_TEXT)
                label_rect = label.get_rect(center=(screen_x, screen_y - radius - 10))
                self.screen.blit(label, label_rect)
    
    def _draw_paths(self):
        """Draw agent paths"""
        for agent_id, spatial_agent in self.spatial_world.agents.items():
            if not spatial_agent.path or not spatial_agent.is_moving:
                continue
            
            # Draw path
            points = [(spatial_agent.x, spatial_agent.y)]
            points.extend(spatial_agent.path)
            
            screen_points = [self.camera.world_to_screen(x, y) for x, y in points]
            
            if len(screen_points) >= 2:
                pygame.draw.lines(self.screen, (100, 100, 150), False, screen_points, 1)
    
    def _get_mental_health_color(self, agent: Agent) -> Tuple[int, int, int]:
        """Get color based on agent's mental health"""
        category = agent.mental_health.category
        
        if category == MentalHealthCategory.THRIVING:
            return COLOR_THRIVING
        elif category == MentalHealthCategory.STABLE:
            return COLOR_STABLE
        elif category == MentalHealthCategory.STRUGGLING:
            return COLOR_STRUGGLING
        else:  # CRISIS
            return COLOR_CRISIS
    
    def _draw_ui(self, current_time: datetime, fps: float):
        """Draw UI overlay"""
        y_offset = 10
        
        # Time
        time_text = current_time.strftime("%A, %I:%M %p")
        time_surface = self.font_medium.render(time_text, True, COLOR_TEXT)
        self.screen.blit(time_surface, (10, y_offset))
        y_offset += 30
        
        # FPS
        fps_text = f"FPS: {fps:.1f}"
        fps_surface = self.font_small.render(fps_text, True, COLOR_TEXT)
        self.screen.blit(fps_surface, (10, y_offset))
        y_offset += 25
        
        # Agent count
        agent_text = f"Agents: {len(self.agents)}"
        agent_surface = self.font_small.render(agent_text, True, COLOR_TEXT)
        self.screen.blit(agent_surface, (10, y_offset))
        y_offset += 25
        
        # Mental health summary
        categories = {cat: 0 for cat in MentalHealthCategory}
        for agent in self.agents.values():
            categories[agent.mental_health.category] += 1
        
        for category, count in categories.items():
            color = self._get_mental_health_color_by_category(category)
            text = f"{category.value.capitalize()}: {count}"
            surface = self.font_small.render(text, True, color)
            self.screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Controls
        y_offset = self.height - 100
        controls = [
            "SPACE: Pause",
            "L: Toggle labels",
            "P: Toggle paths",
            "Click: Select agent",
            "WASD/Arrows: Move camera",
            "Scroll: Zoom"
        ]
        for control in controls:
            surface = self.font_small.render(control, True, COLOR_TEXT_DARK)
            self.screen.blit(surface, (10, y_offset))
            y_offset += 20
    
    def _get_mental_health_color_by_category(self, category: MentalHealthCategory) -> Tuple[int, int, int]:
        """Get color for mental health category"""
        if category == MentalHealthCategory.THRIVING:
            return COLOR_THRIVING
        elif category == MentalHealthCategory.STABLE:
            return COLOR_STABLE
        elif category == MentalHealthCategory.STRUGGLING:
            return COLOR_STRUGGLING
        else:
            return COLOR_CRISIS
    
    def _draw_agent_details(self):
        """Draw selected agent details panel"""
        if self.selected_agent_id not in self.agents:
            return
        
        agent = self.agents[self.selected_agent_id]
        spatial_agent = self.spatial_world.get_agent(self.selected_agent_id)
        
        # Panel background
        panel_width = 300
        panel_height = 400
        panel_x = self.width - panel_width - 10
        panel_y = 10
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (30, 30, 40), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 120), panel_rect, 2)
        
        # Agent info
        y = panel_y + 10
        
        # Name
        name_surface = self.font_medium.render(agent.name, True, COLOR_TEXT)
        self.screen.blit(name_surface, (panel_x + 10, y))
        y += 30
        
        # Role
        role_text = f"{agent.role}, {agent.age}"
        role_surface = self.font_small.render(role_text, True, COLOR_TEXT_DARK)
        self.screen.blit(role_surface, (panel_x + 10, y))
        y += 25
        
        # Mental health
        mh = agent.mental_health
        mh_texts = [
            f"State: {mh.category.value}",
            f"Anxiety: {mh.anxiety:.2f}",
            f"Depression: {mh.depression:.2f}",
            f"Stress: {mh.stress:.2f}",
            f"Wellbeing: {mh.wellbeing:.2f}"
        ]
        
        for text in mh_texts:
            surface = self.font_small.render(text, True, COLOR_TEXT)
            self.screen.blit(surface, (panel_x + 10, y))
            y += 20
        
        y += 10
        
        # Position
        if spatial_agent:
            pos_text = f"Position: ({spatial_agent.x:.1f}, {spatial_agent.y:.1f})"
            pos_surface = self.font_small.render(pos_text, True, COLOR_TEXT_DARK)
            self.screen.blit(pos_surface, (panel_x + 10, y))
            y += 20
            
            # Moving status
            if spatial_agent.is_moving:
                moving_text = "Moving..."
                moving_surface = self.font_small.render(moving_text, True, (100, 200, 100))
                self.screen.blit(moving_surface, (panel_x + 10, y))
            y += 25
        
        # Recent actions
        if agent.recent_actions:
            actions_title = self.font_small.render("Recent Actions:", True, COLOR_TEXT)
            self.screen.blit(actions_title, (panel_x + 10, y))
            y += 20
            
            for action in agent.recent_actions[-5:]:
                action_text = f"• {action[:30]}"
                action_surface = self.font_small.render(action_text, True, COLOR_TEXT_DARK)
                self.screen.blit(action_surface, (panel_x + 15, y))
                y += 18
    
    def tick(self, target_fps: int = 60) -> float:
        """
        Tick the visualizer clock
        
        Args:
            target_fps: Target frames per second
            
        Returns:
            Delta time in seconds
        """
        return self.clock.tick(target_fps) / 1000.0
    
    def quit(self):
        """Quit pygame"""
        pygame.quit()
