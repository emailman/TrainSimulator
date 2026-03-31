"""
A simple game where the alien tries to capture
as many coins as possible by moving into a lane
before the coin arrives
"""

import pgzrun
from pgzero.actor import Actor
from pgzero.animation import animate
from pgzero.loaders import sounds
from pgzero.screen import Screen
from pgzero.keyboard import keyboard
from pygame import Rect

HEIGHT = 300
WIDTH = 500
TITLE = "Get Rich Quick"

ANIMATE_TIME_1 = 6
ANIMATE_TIME_2 = 4
ANIMATE_TIME_3 = 8

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

LANE_1 = Rect((0, 0), (WIDTH, HEIGHT / 3))
LANE_2 = Rect((0, 100), (WIDTH, HEIGHT / 3))
LANE_3 = Rect((0, 200), (WIDTH, HEIGHT / 3))

alien = Actor("alien")
alien.x = WIDTH / 2
alien.y = HEIGHT / 2

screen: Screen

# Create a list of coin objects
coins = []
for i in range(3):
    coin = Actor("gold_coin")
    coins.append(coin)

# Create of list of coin booleans to record collisions
collide_coin = [False, False, False]


def draw():
    screen.clear()
    screen.draw.filled_rect(LANE_1, RED)
    screen.draw.filled_rect(LANE_2, GREEN)
    screen.draw.filled_rect(LANE_3, BLUE)

    alien.draw()

    for _coin in coins:
        _coin.draw()


def on_key_down():
    if keyboard.up and alien.y > 50:
        alien.y -= 100

    elif keyboard.down and alien.y < 250:
        alien.y += 100


def update():
    global collide_coin

    for _i, _coin in enumerate(coins):
        if alien.colliderect(_coin):
            # Only play the sound once per collision
            if not collide_coin[_i]:
                collide_coin[_i] = True
                sounds.coin.play()
        else:
            collide_coin[_i] = False


def animate_1():
    # Animate the first coin in the list
    _coin = coins[0]
    _coin.pos = (600, 50)
    animate(
        _coin,
        tween="linear",
        duration=ANIMATE_TIME_1,
        on_finished=animate_1,
        pos=(-100, 50),
    )


def animate_2():
    # Animate the second coin in the list
    _coin = coins[1]
    _coin.pos = (600, 150)
    animate(
        _coin,
        tween="linear",
        duration=ANIMATE_TIME_2,
        on_finished=animate_2,
        pos=(-100, 150),
    )


def animate_3():
    # Animate the third coin in the list
    _coin = coins[2]
    _coin.pos = (600, 250)
    animate(
        _coin,
        tween="linear",
        duration=ANIMATE_TIME_3,
        on_finished=animate_3,
        pos=(-100, 250),
    )


animate_1()
animate_2()
animate_3()

pgzrun.go()
