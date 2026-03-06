import pgzrun
import pygame
from pygame import Rect
import math
from pgzero import music
from pgzero.screen import Screen

WIDTH = 600
HEIGHT = 700
TITLE = "Carousel"

GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 8 carriage colors, ordered clockwise from top
COLORS = [
    (255, 0, 255),  # magenta  (top / 12 o'clock)
    (128, 128, 128),  # gray     (upper-right)
    (255, 0, 0),  # red      (right / 3 o'clock)
    (255, 165, 0),  # orange   (lower-right)
    (255, 255, 0),  # yellow   (bottom / 6 o'clock)
    (0, 255, 0),  # green    (lower-left)
    (0, 255, 255),  # cyan     (left / 9 o'clock)
    (0, 0, 200),  # blue     (upper-left)
]

CIRCLE_RADIUS = 220
CARRIAGE_RADIUS = 170  # distance from center to carriage
CARRIAGE_WIDTH = 45
CARRIAGE_HEIGHT = 15
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BUTTON_RECT = Rect(240, 580, 120, 40)

rotation = 270.0  # start with magenta at the top (270° in screen coordinates)
running = False
screen: Screen


def update():
    global rotation
    if running:
        rotation = (rotation + 0.3) % 360


def draw():
    screen.fill(WHITE)

    # Large gray carousel platform
    screen.draw.filled_circle((CENTER_X, CENTER_Y - 80),
                              CIRCLE_RADIUS, GRAY)

    # START/STOP button
    label = "STOP" if running else "START"
    btn_color = (200, 60, 60) if running else (60, 180, 60)
    screen.draw.filled_rect(BUTTON_RECT, btn_color)
    screen.draw.rect(BUTTON_RECT, BLACK)
    screen.draw.text(label, center=BUTTON_RECT.center,
                     fontsize=24, color=WHITE)

    # Center hub: static black circle
    screen.draw.filled_circle((CENTER_X, CENTER_Y - 80), 12, BLACK)

    # Draw each carriage as a rotated rectangle tangent to the circle
    for i, color in enumerate(COLORS):
        angle_deg = rotation + i * 45
        angle_rad = math.radians(angle_deg)

        x = CENTER_X + CARRIAGE_RADIUS * math.cos(angle_rad)
        y = CENTER_Y - 80 + CARRIAGE_RADIUS * math.sin(angle_rad)

        surf = pygame.Surface((CARRIAGE_WIDTH, CARRIAGE_HEIGHT),
                              pygame.SRCALPHA)
        surf.fill(color)

        # Rotate so the long axis lies tangent to the circle
        rotated = pygame.transform.rotate(surf, 90 - angle_deg)
        rect = rotated.get_rect(center=(int(x), int(y)))
        screen.blit(rotated, rect)


def on_mouse_down(pos):
    global running
    if BUTTON_RECT.collidepoint(pos):
        running = not running
        if running:
            music.play('carousel')
        else:
            music.stop()


pgzrun.go()
