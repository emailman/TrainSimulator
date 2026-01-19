"""
Simulation of a train running between New York City and Miami
A multi-function button handles to train's movement
"""

from enum import Enum

import pgzrun
import pygame
from pygame import Rect
from pgzero.screen import Screen
from pgzero.loaders import sounds


class State(Enum):
    STOPPED = "stopped"           # At station, will reverse on GO
    ACCELERATING = "accelerating"
    CRUISING = "cruising"
    DECELERATING = "decelerating"  # Approaching station
    BRAKING = "braking"           # User-initiated stop
    PAUSED = "paused"             # Stopped mid-journey


class Destination(Enum):
    NYC = "New York City"
    MIAMI = "Miami"

screen: Screen

# Window settings
TITLE = "Amtrak Silver Meteor"
WIDTH = 900
HEIGHT = 450

# Station positions
STATION_NYC_X = 100
STATION_MIAMI_X = 800
TRACK_Y = 320

# Distance scale: 1400 miles between NYC and Miami
MILES_PER_PIXEL = 1400 / (STATION_MIAMI_X - STATION_NYC_X)
MPH_SCALE = 30  # Convert pixel speed to mph (MAX_SPEED of 4 = 120 mph)

# Train properties
train_x = STATION_NYC_X
train_speed = 0
MAX_SPEED = 4
ACCELERATION = 0.05

# Initial conditions
state = State.STOPPED
target_station = Destination.MIAMI  # Train starts at NYC, heads to Miami

# GO button
button = Rect(400, 380, 100, 50)


def draw():
    # Background (sky)
    screen.fill((135, 206, 235))

    # Ground
    screen.draw.filled_rect(Rect(0, TRACK_Y, WIDTH, HEIGHT - TRACK_Y),
                            (210, 180, 140))

    # Draw tracks (rails and ties)
    for x in range(50, 850, 30):
        screen.draw.filled_rect(Rect(x, TRACK_Y + 6, 20, 8),
                                (101, 67, 33))  # Ties
    screen.draw.filled_rect(Rect(50, TRACK_Y, 800, 5),
                            (80, 80, 80))  # Top rail
    screen.draw.filled_rect(Rect(50, TRACK_Y + 15, 800, 5),
                            (80, 80, 80))  # Bottom rail

    # NYC Station (left) - platform aligned with train stop
    screen.draw.filled_rect(Rect(STATION_NYC_X - 60, TRACK_Y - 55, 120, 55),
                            (160, 160, 160))  # Platform base
    screen.draw.filled_rect(Rect(STATION_NYC_X - 60, TRACK_Y - 5, 120, 5),
                            (255, 200, 0))  # Yellow safety line at bottom
    screen.draw.text("New York City", center=(STATION_NYC_X, TRACK_Y - 70),
                     fontsize=28, color="DarkBlue")

    # Miami Station (right) - platform aligned with train stop
    screen.draw.filled_rect(Rect(STATION_MIAMI_X - 60,
                                 TRACK_Y - 55, 120, 55),
                            (160, 160, 160))  # Platform base
    screen.draw.filled_rect(Rect(STATION_MIAMI_X - 60, TRACK_Y - 5, 120, 5),
                            (255, 200, 0))  # Yellow safety line at bottom
    screen.draw.text("Miami", center=(STATION_MIAMI_X, TRACK_Y - 70),
                     fontsize=28, color="DarkBlue")

    # Draw train
    draw_train(train_x, TRACK_Y)

    # Draw buttons based on state
    if state == State.STOPPED:
        # DEPART button (green) - at station
        screen.draw.filled_rect(button, (0, 180, 0))
        screen.draw.rect(button, (0, 100, 0))
        screen.draw.text("DEPART", center=button.center, fontsize=32,
                         color="white")
    elif state == State.PAUSED:
        # RESUME button (orange) - paused mid-journey
        screen.draw.filled_rect(button, (255, 180, 0))
        screen.draw.rect(button, (180, 120, 0))
        screen.draw.text("RESUME", center=button.center, fontsize=32,
                         color="white")
    elif state in (State.ACCELERATING, State.CRUISING, State.DECELERATING):
        # STOP button (red) - train is moving
        screen.draw.filled_rect(button, (180, 0, 0))
        screen.draw.rect(button, (100, 0, 0))
        screen.draw.text("STOP", center=button.center, fontsize=32,
                         color="white")

    # Status display
    if target_station == Destination.MIAMI:
        route_text = "Silver Meteor - New York City to Miami"
    else:
        route_text = "Silver Meteor - Miami to New York City"
    screen.draw.text(route_text, topleft=(20, 20), fontsize=28, color="black")

    dist_to_nyc = (train_x - STATION_NYC_X) * MILES_PER_PIXEL
    dist_to_miami = (STATION_MIAMI_X - train_x) * MILES_PER_PIXEL
    screen.draw.text(f"Distance to New York City: {dist_to_nyc:.0f} miles",
                     topleft=(20, 45), fontsize=28, color="black")
    screen.draw.text(f"Distance to Miami: {dist_to_miami:.0f} miles",
                     topleft=(20, 70), fontsize=28, color="black")
    screen.draw.text(f"Speed: {train_speed * MPH_SCALE:.0f} mph",
                     topleft=(20, 95), fontsize=28, color="black")


def draw_train(x, track_y):
    # Modern train with tapered front and back
    body_top = track_y - 45
    body_bottom = track_y - 10
    body_height = body_bottom - body_top

    # Main rectangular body (center section)
    screen.draw.filled_rect(Rect(x - 35, body_top, 70, body_height),
                            (180, 0, 0))

    # Front taper (right side) - polygon
    front_points = [
        (x + 35, body_top),           # Top left of taper
        (x + 55, body_top + body_height // 2),  # Nose point
        (x + 35, body_bottom)         # Bottom left of taper
    ]
    pygame.draw.polygon(screen.surface, (180, 0, 0), front_points)

    # Back taper (left side) - polygon
    back_points = [
        (x - 35, body_top),           # Top right of taper
        (x - 55, body_top + body_height // 2),  # Nose point
        (x - 35, body_bottom)         # Bottom right of taper
    ]
    pygame.draw.polygon(screen.surface, (180, 0, 0), back_points)

    # Windows (symmetrical)
    screen.draw.filled_rect(Rect(x - 25, body_top + 5, 12, 12),
                            (200, 230, 255))
    screen.draw.filled_rect(Rect(x - 5, body_top + 5, 12, 12),
                            (200, 230, 255))
    screen.draw.filled_rect(Rect(x + 13, body_top + 5, 12, 12),
                            (200, 230, 255))

    # Stripe along the body
    screen.draw.filled_rect(Rect(x - 35,
                                 body_top + body_height // 2 - 2, 70, 4),
                            (255, 255, 255))

    # Wheels
    screen.draw.filled_circle((x - 25, track_y - 5), 10, (40, 40, 40))
    screen.draw.filled_circle((x, track_y - 5), 10, (40, 40, 40))
    screen.draw.filled_circle((x + 25, track_y - 5), 10, (40, 40, 40))

    # Wheel centers
    screen.draw.filled_circle((x - 25, track_y - 5), 4, (100, 100, 100))
    screen.draw.filled_circle((x, track_y - 5), 4, (100, 100, 100))
    screen.draw.filled_circle((x + 25, track_y - 5), 4, (100, 100, 100))


def update():
    global train_x, train_speed, state, target_station

    # Nothing to do this time
    if state in (State.STOPPED, State.PAUSED):
        return

    # Handle user-initiated braking
    if state == State.BRAKING:
        train_speed -= ACCELERATION
        if train_speed <= 0:
            train_speed = 0
            state = State.PAUSED
        else:
            # Continue moving while braking
            if target_station == Destination.MIAMI:
                train_x += train_speed
            else:
                train_x -= train_speed
        return

    if state == State.ACCELERATING:
        train_speed += ACCELERATION
        if train_speed >= MAX_SPEED:
            train_speed = MAX_SPEED
            state = State.CRUISING

    # Calculate stopping distance using physics: d = v^2 / (2*a)
    stopping_distance = (train_speed ** 2) / (2 * ACCELERATION)\
        if ACCELERATION > 0 else 0

    if target_station == Destination.MIAMI:
        train_x += train_speed
        distance_to_target = STATION_MIAMI_X - train_x

        # Start decelerating when we need to
        if (distance_to_target <= stopping_distance + 5 and
                state in (State.ACCELERATING, State.CRUISING)):
            sounds.brake.play()
            state = State.DECELERATING

        if state == State.DECELERATING:
            train_speed -= ACCELERATION
            if train_speed <= 0 or train_x >= STATION_MIAMI_X:
                train_speed = 0
                train_x = STATION_MIAMI_X
                state = State.STOPPED
                target_station = Destination.NYC

    else:  # Going to NYC
        train_x -= train_speed
        distance_to_target = train_x - STATION_NYC_X

        # Start decelerating when we need to
        if (distance_to_target <= stopping_distance + 5 and
                state in (State.ACCELERATING, State.CRUISING)):
            sounds.brake.play()
            state = State.DECELERATING

        if state == State.DECELERATING:
            train_speed -= ACCELERATION
            if train_speed <= 0 or train_x <= STATION_NYC_X:
                train_speed = 0
                train_x = STATION_NYC_X
                state = State.STOPPED
                target_station = Destination.MIAMI


def on_mouse_down(pos):
    global state
    if not button.collidepoint(pos):
        return

    if state == State.STOPPED:
        # GO button - start from station
        sounds.whistle.play()
        state = State.ACCELERATING
    elif state == State.PAUSED:
        # START button - resume from pause
        sounds.whistle.play()
        state = State.ACCELERATING
    elif state in (State.ACCELERATING, State.CRUISING, State.DECELERATING):
        # STOP button - begin braking
        sounds.brake.play()
        state = State.BRAKING


pgzrun.go()
