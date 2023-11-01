class Settings:
    """
    A class to store all settings for Alien Invasion.
    """

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 600
        # self.bg_color = (230, 230, 230)
        self.bg_color = (0, 0, 0)

        # Aircraft settings
        self.aircraft_speed_factor = 1
        self.aircraft_limit = 1
        self.aircraft_left = self.aircraft_limit

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_speed_factor = 1
        self.bullet_color = 250, 208, 0
        self.bullet_allowed = 1

        # Alien settings
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 30
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_changing_direction_cooldown_range = (100, 1000)
        self.alien_bullet_allowed = self.bullet_allowed * 8
        self.alien_bullet_speed_factor = self.bullet_speed_factor - 0.5
        self.alien_bullet_color = 255, 60, 60

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.aircraft_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.aircraft_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
