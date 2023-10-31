import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the aircraft."""
        
    def __init__(self, ai_settings, screen, aircraft, direction):
        """Create a bullet object at the aircraft's current position."""
        super().__init__()
        self.screen = screen
        
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, 
                                ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = aircraft.rect.centerx
        self.rect.top = aircraft.rect.top
        
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        
        self.color = aircraft.bullet_color
        self.speed_factor = aircraft.bullet_speed_factor
        self.direction = direction
        
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= (self.speed_factor * self.direction)
        # Update the rect position.
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)