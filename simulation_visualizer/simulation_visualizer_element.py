import pygame
from typing import List
from environment.environment_base import EnvironmentElement  # Import the base class

class SimulationVisualizer:
    def __init__(self):
        pygame.init()

        # Get actual screen size (fullscreen resolution)
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        # Use full screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Lunar Base Environment")
        self.clock = pygame.time.Clock()

        real_width_mm = 1571
        real_height_mm = 874

        scale_x = self.screen_width / real_width_mm
        scale_y = self.screen_height / real_height_mm
        self.scale = min(scale_x, scale_y)  # Preserve aspect ratio

        # === Create a separate surface for static environment ===
        self.env_surface = pygame.Surface((self.screen_width, self.screen_height)).convert()
        self.env_surface.fill((0, 0, 0))  # Dark gray background like Moon

    def transform_coords(self, x_mm, y_mm):
        """Transform mm to pixel coordinates, flip Y for screen space"""
        x_px = int(x_mm * self.scale)
        y_px = int(self.screen_height - y_mm * self.scale)
        return x_px, y_px

    def render_static_environment(self, elements: List[EnvironmentElement]):
        """Render static environment elements ONCE onto env_surface"""
        for element in elements:
            element.render(self.env_surface, self.transform_coords, self.scale)
            print(f"Rendering static element: {element.tag}")
        
        print("Static environment rendered and cached.")

    def render_frame(self, dynamic_elements: List['EnvironmentElement']):
        """Draw dynamic elements like robots onto the main screen"""
        self.clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # === Step 1: Clean background by blitting cached env_surface ===
        self.screen.blit(self.env_surface, (0, 0))

        # === Step 2: Draw robots ===
        for element in dynamic_elements:
            element.render(self.screen, self.transform_coords, self.scale)

        pygame.display.flip()
