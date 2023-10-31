from tabnanny import check
import pygame
from pygame.sprite import Sprite
# from bullet import Bullet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.fleet_direction = 1
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.bullet_speed_factor = ai_settings.alien_bullet_speed_factor
        self.bullet_color = ai_settings.alien_bullet_color
        self.bullet_allowed = ai_settings.alien_bullet_allowed
        self.alien_changing_direction_cooldown = ai_settings.alien_changing_direction_cooldown


    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.fleet_direction)
        self.rect.x = self.x
        self.alien_changing_direction_cooldown = self.alien_changing_direction_cooldown - 1 if self.alien_changing_direction_cooldown > 0 else 0

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True