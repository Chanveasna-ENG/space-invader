"""
This is the main file for the game. 
WE play game in this file.
"""

import sys
import pygame
from settings import Settings
from aircraft import Aircraft
import game_function as gf
from pygame.sprite import Group
from stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame import mixer
import time


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    # sound back ground
    mixer.music.load('sounds/background-track.mp3')
    mixer.music.play(-1)
    ai_settings = Settings()
    screen = pygame.display.set_mode((
        ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a aircraft.
    aircraft = Aircraft(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group()
    aliens = Group()
    # Make an alien.
    # alien = Alien(ai_settings, screen)

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Start the main loop for the game.
    # gf.create_alien_army(ai_settings, screen, aircraft, aliens)
    while True:
        time.sleep(0.001)
        gf.check_events(ai_settings, screen, stats, sb,
                        play_button, aircraft, aliens, bullets)
        if stats.game_active:
            aircraft.update()
            gf.update_bullets(ai_settings, screen, stats,
                              sb, aircraft, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,
                             aircraft, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, aircraft,
                         aliens, bullets, play_button)


run_game()
