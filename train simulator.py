import pgzrun
import pygame
from pygame import Rect
from pgzero.screen import Screen
from pgzero.loaders import sounds
screen: Screen

# Window settings
TITLE = "Silver Meteor"
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

# State: "stopped", "accelerating", "cruising", "decelerating"
state = "stopped"
target_station = "miami"  # Train starts at NYC, heads to Miami

# GO button
button = Rect(400, 380, 100, 50)


def draw():
    # Sky background
    screen.fill((135, 206, 235))

    # Ground
    screen.draw.rect(Rect(0, TRACK_Y + 20, WIDTH, HEIGHT - TRACK_Y - 20), (34, 139, 34))

    # Draw tracks (rails and sleepers)
    for x in range(50, 850, 30):
        screen.draw.filled_rect(Rect(x, TRACK_Y + 5, 20, 8), (101, 67, 33))  # Sleepers
    screen.draw.filled_rect(Rect(50, TRACK_Y, 800, 5), (80, 80, 80))  # Top rail
    screen.draw.filled_rect(Rect(50, TRACK_Y + 15, 800, 5), (80, 80, 80))  # Bottom rail

    # NYC Station (left) - platform aligned with train stop
    screen.draw.filled_rect(Rect(STATION_NYC_X - 60, TRACK_Y - 55, 120, 55), (160, 160, 160))  # Platform base
    screen.draw.filled_rect(Rect(STATION_NYC_X - 60, TRACK_Y - 5, 120, 5), (255, 200, 0))  # Yellow safety line at bottom
    screen.draw.text("New York City", center=(STATION_NYC_X, TRACK_Y - 70), fontsize=20, color="darkblue")

    # Miami Station (right) - platform aligned with train stop
    screen.draw.filled_rect(Rect(STATION_MIAMI_X - 60, TRACK_Y - 55, 120, 55), (160, 160, 160))  # Platform base
    screen.draw.filled_rect(Rect(STATION_MIAMI_X - 60, TRACK_Y - 5, 120, 5), (255, 200, 0))  # Yellow safety line at bottom
    screen.draw.text("Miami", center=(STATION_MIAMI_X, TRACK_Y - 70), fontsize=20, color="darkblue")

    # Draw train
    draw_train(train_x, TRACK_Y)

    # Draw GO button when stopped
    if state == "stopped":
        screen.draw.filled_rect(button, (0, 180, 0))
        screen.draw.rect(button, (0, 100, 0))
        screen.draw.text("GO", center=button.center, fontsize=32, color="white")

    # Status display - distances
    dist_to_nyc = (train_x - STATION_NYC_X) * MILES_PER_PIXEL
    dist_to_miami = (STATION_MIAMI_X - train_x) * MILES_PER_PIXEL
    screen.draw.text(f"Distance to New York City: {dist_to_nyc:.0f} miles", topleft=(20, 20), fontsize=20, color="black")
    screen.draw.text(f"Distance to Miami: {dist_to_miami:.0f} miles", topleft=(20, 45), fontsize=20, color="black")
    screen.draw.text(f"Speed: {train_speed * MPH_SCALE:.0f} mph", topleft=(20, 70), fontsize=20, color="black")


def draw_train(x, track_y):
    # Modern train with tapered front and back
    body_top = track_y - 45
    body_bottom = track_y - 10
    body_height = body_bottom - body_top

    # Main rectangular body (center section)
    screen.draw.filled_rect(Rect(x - 35, body_top, 70, body_height), (180, 0, 0))

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
    screen.draw.filled_rect(Rect(x - 25, body_top + 5, 12, 12), (200, 230, 255))
    screen.draw.filled_rect(Rect(x - 5, body_top + 5, 12, 12), (200, 230, 255))
    screen.draw.filled_rect(Rect(x + 13, body_top + 5, 12, 12), (200, 230, 255))

    # Stripe along the body
    screen.draw.filled_rect(Rect(x - 35, body_top + body_height // 2 - 2, 70, 4), (255, 255, 255))

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

    if state == "stopped":
        return

    if state == "accelerating":
        train_speed += ACCELERATION
        if train_speed >= MAX_SPEED:
            train_speed = MAX_SPEED
            state = "cruising"

    # Calculate stopping distance using physics: d = v^2 / (2*a)
    stopping_distance = (train_speed ** 2) / (2 * ACCELERATION) if ACCELERATION > 0 else 0

    if target_station == "miami":
        train_x += train_speed
        distance_to_target = STATION_MIAMI_X - train_x

        # Start decelerating when we need to
        if distance_to_target <= stopping_distance + 5 and state in ("accelerating", "cruising"):
            sounds.brake.play()
            state = "decelerating"

        if state == "decelerating":
            train_speed -= ACCELERATION
            if train_speed <= 0 or train_x >= STATION_MIAMI_X:
                train_speed = 0
                train_x = STATION_MIAMI_X
                state = "stopped"
                target_station = "nyc"

    else:  # Going to NYC
        train_x -= train_speed
        distance_to_target = train_x - STATION_NYC_X

        # Start decelerating when we need to
        if distance_to_target <= stopping_distance + 5 and state in ("accelerating", "cruising"):
            sounds.brake.play()
            state = "decelerating"

        if state == "decelerating":
            train_speed -= ACCELERATION
            if train_speed <= 0 or train_x <= STATION_NYC_X:
                train_speed = 0
                train_x = STATION_NYC_X
                state = "stopped"
                target_station = "miami"


def on_mouse_down(pos):
    global state
    if state == "stopped" and button.collidepoint(pos):
        sounds.whistle.play()
        state = "accelerating"


pgzrun.go()
