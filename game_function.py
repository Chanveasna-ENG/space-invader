# Description: This file contains the functions that will be used in the game.
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame import mixer

# Initialize game and create a screen object.
pygame.init()


def check_events(ai_settings, screen, stats, sb, play_button, aircraft, aliens, bullets):
    """Respond to keyp  resses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              aircraft, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, aircraft, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, aircraft)
    # fire_bullet(ai_settings, screen, aircraft, bullets)


def update_screen(ai_settings, screen, stats, sb, aircraft, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    # Draw all bullets to the screen
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aircraft.blitme()
    aliens.draw(screen)
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_play_button(ai_settings, screen, stats, sb, play_button, aircraft, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the aircraft.
        create_alien_army(ai_settings, aircraft.screen, aircraft, aliens)
        aircraft.center_aircraft()
        # Hide the mouse cursor.
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)


def check_keydown_events(event, ai_settings, screen, aircraft, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        aircraft.moving_right = True
    elif event.key == pygame.K_LEFT:
        aircraft.moving_left = True
    elif event.key == pygame.K_UP:
        aircraft.moving_up = True
    elif event.key == pygame.K_DOWN:
        aircraft.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, aircraft, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, aircraft):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        aircraft.moving_right = False
    elif event.key == pygame.K_LEFT:
        aircraft.moving_left = False
    elif event.key == pygame.K_UP:
        aircraft.moving_up = False
    elif event.key == pygame.K_DOWN:
        aircraft.moving_down = False


def update_bullets(ai_settings, screen, stats, sb, aircraft, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, aircraft, aliens, bullets)
    if len(aliens) == 0:
        bullets.empty()
        create_alien_army(ai_settings, screen, aircraft, aliens)


def fire_bullet(ai_settings, screen, aircraft, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, aircraft)
        bullets.add(new_bullet)
        # sound back ground
        mixer.music.load('sounds/shoot.wav')
        mixer.music.play()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien_army(ai_settings, screen, aircraft, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, aircraft.rect.height,
                                  alien.rect.height)
    # Create the first row of aliens.
    for number_rows in range(number_rows):
        for alien_number in range(number_alien_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens,
                         alien_number, number_rows)


def create_alien(ai_settings, screen, aliens, alien_number, number_rows):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
    aliens.add(alien)


def get_number_rows(ai_settings, aircraft_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - aircraft_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_army_edge(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_army_direction(ai_settings, aliens)
            break


def change_army_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, aircraft, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the positions of all aliens in the fleet.
    """
    check_army_edge(ai_settings, aliens)
    aliens.update()

    check_aliens_bottom(ai_settings, stats, screen, aircraft, aliens, bullets)
    # for alien in aliens.copy():
    #     if alien.rect.bottom >= ai_settings.screen_height:
    #         aliens.remove(alien)
    if pygame.sprite.spritecollideany(aircraft, aliens):
        #     # print("Aircraft hit!!!")
        aircraft_hit(ai_settings, stats, screen, aircraft, aliens, bullets)


def aircraft_hit(ai_settings, stats, screen, aircraft, aliens, bullets):
    """Respond to aircraft being hit by alien."""
    if ai_settings.aircraft_left > 0:
        # Decrement ships_left.
        ai_settings.aircraft_left -= 1
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the aircraft.
        create_alien_army(ai_settings, aircraft.screen, aircraft, aliens)
        aircraft.center_aircraft()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()


def check_aliens_bottom(ai_settings, stats, screen, aircraft, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the aircraft got hit.
            aircraft_hit(ai_settings, stats, screen, aircraft, aliens, bullets)
            break


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aircraft, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_alien_army(ai_settings, screen, aircraft, aliens)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
