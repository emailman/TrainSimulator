import pgzrun
from pgzero.screen import Screen
from pygame import Rect
from pygame.locals import K_SPACE
import random
from enum import Enum

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors (using pgzero color names where possible)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_RED = (128, 0, 0)
DARK_GREEN = (0, 128, 0)
DARK_BLUE = (0, 0, 128)
DARK_YELLOW = (128, 128, 0)
GRAY = (128, 128, 128)

screen: Screen

class GameState(Enum):
    WAITING = 1
    SHOWING = 2
    LISTENING = 3
    GAME_OVER = 4


# Game state variables
game_state = GameState.WAITING
sequence = []
player_sequence = []
current_step = 0
score = 0
flash_timer = 0
flash_duration = 60  # frames
pause_duration = 20  # frames between flashes
current_flash = -1
message = "Press SPACE to start!"

# Button definitions (x, y, width, height, normal_color, flash_color)
buttons = {
    0: (200, 150, 150, 150, DARK_RED, RED),  # Top-left (Red)
    1: (450, 150, 150, 150, DARK_GREEN, GREEN),  # Top-right (Green)
    2: (200, 350, 150, 150, DARK_BLUE, BLUE),  # Bottom-left (Blue)
    3: (450, 350, 150, 150, DARK_YELLOW, YELLOW)  # Bottom-right (Yellow)
}

# Button rectangles for collision detection (using pgzero Rect)
button_rects = {}
for button_id, (x, y, w, h, _, _) in buttons.items():
    button_rects[button_id] = Rect(x, y, w, h)


def add_to_sequence():
    """Add a random button to the sequence"""
    global sequence
    sequence.append(random.randint(0, 3))


def start_game():
    """Start a new game"""
    global game_state, sequence, player_sequence, current_step, score, message
    game_state = GameState.SHOWING
    sequence = []
    player_sequence = []
    current_step = 0
    score = 0
    add_to_sequence()
    start_showing_sequence()
    message = f"Round {len(sequence)}"


def start_showing_sequence():
    """Start showing the sequence to the player"""
    global game_state, current_step, flash_timer, current_flash
    game_state = GameState.SHOWING
    current_step = 0
    flash_timer = 0
    current_flash = -1


def update_showing():
    """Update the sequence showing state"""
    global flash_timer, current_flash, current_step, game_state, player_sequence, message

    flash_timer += 1

    if current_flash == -1:
        # Pause before showing next button
        if flash_timer >= pause_duration:
            if current_step < len(sequence):
                current_flash = sequence[current_step]
                flash_timer = 0
            else:
                # Done showing sequence, start listening
                game_state = GameState.LISTENING
                player_sequence = []
                message = "Your turn!"
    else:
        # Currently flashing a button
        if flash_timer >= flash_duration:
            current_flash = -1
            flash_timer = 0
            current_step += 1


def handle_player_input(button_id_):
    """Handle player button press"""
    global player_sequence, game_state, message, score

    if game_state != GameState.LISTENING:
        return

    player_sequence.append(button_id_)

    # Check if the input matches the sequence so far
    if player_sequence[-1] != sequence[len(player_sequence) - 1]:
        # Wrong button pressed
        game_state = GameState.GAME_OVER
        message = f"Game Over! Final Score: {score}"
        return

    # Check if player completed the current sequence
    if len(player_sequence) == len(sequence):
        # Player got it right!
        score += 1
        add_to_sequence()
        start_showing_sequence()
        message = f"Round {len(sequence)} - Score: {score}"


def update():
    """Pygame Zero update function"""
    if game_state == GameState.SHOWING:
        update_showing()


def draw():
    """Pygame Zero draw function"""
    screen.fill(BLACK)

    # Draw buttons
    for button_id_, (x_, y_, w_, h_, normal_color, flash_color) in buttons.items():
        color = flash_color if button_id_ == current_flash else normal_color
        screen.draw.filled_rect(Rect(x_, y_, w_, h_), color)
        screen.draw.rect(Rect(x_, y_, w_, h_), WHITE)

    # Draw center circle
    screen.draw.filled_circle((WIDTH // 2, HEIGHT // 2), 80, GRAY)
    screen.draw.circle((WIDTH // 2, HEIGHT // 2), 80, WHITE)

    # Draw text
    screen.draw.text(message, centerx=WIDTH // 2, centery=HEIGHT // 2,
                     fontsize=24, color=WHITE)

    if game_state == GameState.GAME_OVER:
        screen.draw.text("Press SPACE to play again", centerx=WIDTH // 2,
                         centery=HEIGHT // 2 + 40, fontsize=20, color=WHITE)


def on_key_down(key):
    """Handle key presses"""
    if key == K_SPACE:
        if game_state == GameState.WAITING or game_state == GameState.GAME_OVER:
            start_game()


def on_mouse_down(pos):
    """Handle mouse clicks"""
    if game_state != GameState.LISTENING:
        return

    # Check which button was clicked
    for button_id_, rect in button_rects.items():
        if rect.collidepoint(pos):
            handle_player_input(button_id_)
            break


# Run the game
pgzrun.go()