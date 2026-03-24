"""
Use the up arrow key on the keyboard to make the alien jump
"""

import pgzrun
from pgzero.actor import Actor
from pgzero.screen import Screen
from pgzero.keyboard import keyboard
from pygame import Rect

WIDTH = 800
HEIGHT = 400
TITLE = "Jump the Alien"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (88, 242, 152)
CYAN = (0, 255, 255)

screen: Screen

runner = Actor("alien")
runner.pos = (WIDTH // 2, 300)

GRAVITY = 0.5
GROUND_Y = 300

VY_T0 = -15
vy = 0

def update():
    global vy

    # Set the initial velocity if jumping from the ground
    if keyboard.up and runner.y >= GROUND_Y:
        vy = VY_T0  # initial upward velocity

    # Adjust the velocity for the pull of gravity
    vy += GRAVITY

    # Adjust the position of the alien based on
    # the current velocity
    runner.y += vy

    if runner.y >= GROUND_Y:
        # Stop when the actor reaches the ground
        runner.y = GROUND_Y
        vy = 0

def draw():
    screen.clear()
    screen.draw.filled_rect(Rect(0, 0, 800, 200), CYAN)
    screen.draw.filled_rect(Rect(0, 200, 800, 200), GREEN)
    runner.draw()
    screen.draw.text(f"velocity: {vy:.1f}", (10, 10), color=BLACK)

pgzrun.go()