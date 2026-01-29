
import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.screen import Screen

screen: Screen

# Create an actor using the 'alien' image (you can replace with any image you have)
actor = Actor('alien')
# Set initial position
actor.pos = (100, 300)

def draw():
    # Clear the screen
    screen.clear()
    # Draw the actor
    actor.draw()

def update():
    # Check if right arrow key is pressed
    if keyboard.right:
        # Move the actor to the right by adding to its x position
        actor.x += 4  # You can adjust the speed by changing this value

# Set the window size
WIDTH = 800
HEIGHT = 600

pgzrun.go()