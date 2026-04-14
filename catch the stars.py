"""
Catch the Stars
Move the alien left and right to catch falling stars.
"""

import pgzrun
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.screen import Screen
from pgzero.clock import clock
from pgzero.animation import animate

WIDTH = 600
HEIGHT = 400
TITLE = "Catch the Stars"

screen: Screen

alien = Actor("alien")
alien.pos = (WIDTH // 2, HEIGHT - 40)

stars = []   # list of star Actors
score = 0
SPEED = 4
STAR_FALL_DURATION = 3  # seconds to fall from top to bottom
TIME_LIMIT = 15
time_left = TIME_LIMIT
game_over = False


def spawn_star():
    """ Create a new star and start an animation """
    star = Actor("star")
    star.x = random.randint(20, WIDTH - 20)
    star.y = 0
    stars.append(star)

    def remove_star():
        """ Remove the star from the list of stars """
        if star in stars:
            stars.remove(star)


    #  The star will fall down and be removed once it hits the ground
    animate(star, tween="linear", duration=STAR_FALL_DURATION,
            on_finished=remove_star,
            y=HEIGHT + 30)


def draw():
    screen.clear()

    alien.draw()

    for star in stars:
        star.draw()

    screen.draw.text(f"Score: {score}", (10, 10),
                     color="white", fontsize=30)
    screen.draw.text(f"Time: {time_left}", (WIDTH - 120, 10),
                     color="white", fontsize=30)

    if game_over:
        screen.draw.text(f"Game Over! Score: {score}",
                         center=(WIDTH // 2, HEIGHT // 2),
                         color="white", fontsize=48)


def tick():
    """ A countdown timer for the game """
    global time_left, game_over
    if time_left > 0:
        time_left -= 1
    else:
        game_over = True


def update():
    global score

    if game_over:
        return

    # Move alien
    if keyboard.left and alien.left > 0:
        alien.x -= SPEED
    if keyboard.right and alien.right < WIDTH:
        alien.x += SPEED

    # Check catches
    caught = [s for s in stars if alien.colliderect(s)]
    score += len(caught)

    # Remove the caught stars from the list of stars
    for s in caught:
        stars.remove(s)

    # Spawn a new star occasionally
    if random.random() < 0.02:
        spawn_star()

# Run a countdown timer once per second
clock.schedule_interval(tick, 1)

pgzrun.go()
