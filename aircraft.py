import pygame

class Aircraft():
    """A class to manage the aircraft."""
    
    def __init__(self, ai_settings, screen):
        """Initialize the aircraft and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the aircraft image and get its rect.
        self.image = pygame.image.load('images/aircraft.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new aircraft at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the aircraft's center.
        self.center = float(self.rect.centerx)
        
        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """Update the aircraft's position based on the movement flag."""
        # Update the aircraft's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.aircraft_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.aircraft_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += self.ai_settings.aircraft_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.top -= self.ai_settings.aircraft_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center
        
    def blitme(self):
        """Draw the aircraft at its current location."""
        self.screen.blit(self.image, self.rect)
        
    def center_aircraft(self):
        """Center the aircraft on the screen."""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom