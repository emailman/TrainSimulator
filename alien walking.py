"""
Move the alien with the left and right arrow keys,
keeping it on the screen
"""

import pgzrun
from pgzero.actor import Actor
from pgzero.screen import Screen
from pgzero.keyboard import keyboard
from pygame import Rect

WIDTH = 800
HEIGHT = 400
TITLE = "Move the Alien"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (88, 242, 152)
CYAN = (0, 255, 255)

screen: Screen

runner = Actor("alien")
runner.pos = (WIDTH // 2, 300)

SPEED = 5

def update():
    """ Move the alien with the left and right arrow keys """
    if keyboard.left:
        runner.x -= SPEED
    if keyboard.right:
        runner.x += SPEED

    # Keep the alien on the screen
    if runner.x > WIDTH - runner.width // 2:
        runner.x = WIDTH - runner.width // 2
    elif runner.x < runner.width // 2:
        runner.x = runner.width // 2

def draw():
    screen.clear()
    screen.draw.filled_rect(Rect(0, 0, 800, 200), CYAN)
    screen.draw.filled_rect(Rect(0, 200, 800, 200), GREEN)
    runner.draw()

pgzrun.go()