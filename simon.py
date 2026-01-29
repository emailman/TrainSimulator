import pgzrun
import pygame
from pgzero.screen import Screen
import random
from enum import Enum

screen: Screen

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
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


class GameState(Enum):
    WAITING = 1
    SHOWING = 2
    LISTENING = 3
    GAME_OVER = 4


class SimonGame:
    def __init__(self):
        self.state = GameState.WAITING
        self.sequence = []
        self.player_sequence = []
        self.current_step = 0
        self.score = 0
        self.flash_timer = 0
        self.flash_duration = 60  # frames
        self.pause_duration = 20  # frames between flashes
        self.current_flash = -1
        self.message = "Press SPACE to start!"

        # Button definitions (x, y, width, height, normal_color, flash_color)
        self.buttons = {
            0: (200, 150, 150, 150, DARK_RED, RED),  # Top-left (Red)
            1: (450, 150, 150, 150, DARK_GREEN, GREEN),  # Top-right (Green)
            2: (200, 350, 150, 150, DARK_BLUE, BLUE),  # Bottom-left (Blue)
            3: (450, 350, 150, 150, DARK_YELLOW, YELLOW)  # Bottom-right (Yellow)
        }

        # Button rectangles for collision detection
        self.button_rects = {}
        for button_id, (x, y, w, h, _, _) in self.buttons.items():
            self.button_rects[button_id] = pygame.Rect(x, y, w, h)

    def add_to_sequence(self):
        """Add a random button to the sequence"""
        self.sequence.append(random.randint(0, 3))

    def start_game(self):
        """Start a new game"""
        self.state = GameState.SHOWING
        self.sequence = []
        self.player_sequence = []
        self.current_step = 0
        self.score = 0
        self.add_to_sequence()
        self.start_showing_sequence()
        self.message = f"Round {len(self.sequence)}"

    def start_showing_sequence(self):
        """Start showing the sequence to the player"""
        self.state = GameState.SHOWING
        self.current_step = 0
        self.flash_timer = 0
        self.current_flash = -1

    def update_showing(self):
        """Update the sequence showing state"""
        self.flash_timer += 1

        if self.current_flash == -1:
            # Pause before showing next button
            if self.flash_timer >= self.pause_duration:
                if self.current_step < len(self.sequence):
                    self.current_flash = self.sequence[self.current_step]
                    self.flash_timer = 0
                else:
                    # Done showing sequence, start listening
                    self.state = GameState.LISTENING
                    self.player_sequence = []
                    self.message = "Your turn!"
        else:
            # Currently flashing a button
            if self.flash_timer >= self.flash_duration:
                self.current_flash = -1
                self.flash_timer = 0
                self.current_step += 1

    def handle_player_input(self, button_id):
        """Handle player button press"""
        if self.state != GameState.LISTENING:
            return

        self.player_sequence.append(button_id)

        # Check if the input matches the sequence so far
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            # Wrong button pressed
            self.state = GameState.GAME_OVER
            self.message = f"Game Over! Final Score: {self.score}"
            return

        # Check if player completed the current sequence
        if len(self.player_sequence) == len(self.sequence):
            # Player got it right!
            self.score += 1
            self.add_to_sequence()
            self.start_showing_sequence()
            self.message = f"Round {len(self.sequence)} - Score: {self.score}"

    def update(self):
        """Update game state"""
        if self.state == GameState.SHOWING:
            self.update_showing()

    def draw(self, scr):
        """Draw the game"""
        scr.fill(BLACK)

        # Draw buttons
        for button_id, (x, y, w, h, normal_color, flash_color) in self.buttons.items():
            color = flash_color if button_id == self.current_flash else normal_color
            pygame.draw.rect(scr.surface, color, (x, y, w, h))
            pygame.draw.rect(scr.surface, WHITE, (x, y, w, h), 3)

        # Draw center circle
        pygame.draw.circle(scr.surface, GRAY, (WIDTH // 2, HEIGHT // 2), 80)
        pygame.draw.circle(scr.surface, WHITE, (WIDTH // 2, HEIGHT // 2), 80, 3)

        # Draw text
        scr.draw.text(self.message, centerx=WIDTH // 2, centery=HEIGHT // 2,
                      fontsize=24, color=WHITE)

        if self.state == GameState.GAME_OVER:
            scr.draw.text("Press SPACE to play again", centerx=WIDTH // 2,
                          centery=HEIGHT // 2 + 40, fontsize=20, color=WHITE)


# Create game instance
game = SimonGame()


def update():
    """Pygame Zero update function"""
    game.update()


def draw():
    """Pygame Zero draw function"""
    game.draw(screen)


def on_key_down(key):
    """Handle key presses"""
    if key == pygame.K_SPACE:
        if game.state == GameState.WAITING or game.state == GameState.GAME_OVER:
            game.start_game()


def on_mouse_down(pos):
    """Handle mouse clicks"""
    if game.state != GameState.LISTENING:
        return

    # Check which button was clicked
    for button_id, rect in game.button_rects.items():
        if rect.collidepoint(pos):
            game.handle_player_input(button_id)
            break

# Run the game
pgzrun.go()