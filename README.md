# Silver Meteor Train Simulator

A simple train simulation built with Pygame Zero that models a train running between New York City and Miami.

## Overview

This simulator recreates the Silver Meteor route—a real Amtrak train service that travels approximately 1,400 miles along the East Coast. The train departs from one station, accelerates to cruising speed, then automatically decelerates to stop at the destination using physics-based calculations.

## Features

- **Realistic physics**: The train uses proper kinematic equations for acceleration and braking
- **Distance tracking**: Real-time display of miles to both NYC and Miami
- **Speed display**: Current speed shown in mph
- **Sound effects**: Train whistle on departure and brakes when stopping
- **Bidirectional travel**: After arriving at one station, click GO to travel back

## Requirements

- Python 3
- Pygame Zero (`pgzero`)
- Pygame

Install dependencies:
```bash
pip install pgzero pygame
```

## Sound Files

The game expects two sound files in a `sounds/` folder:
- `sounds/whistle.wav` (or `.ogg`) - plays when the train departs
- `sounds/brake.wav` (or `.ogg`) - plays when the train begins braking

## Running the Simulator

```bash
python "train simulator.py"
```

Or with `pgzrun`:
```bash
pgzrun "train simulator.py"
```

## Controls

- **Click the GO button** to start the train moving toward the next station
- The train handles acceleration and braking automatically

## How It Works

1. The train starts at NYC station
2. Press GO to depart—the whistle sounds and the train accelerates
3. At max speed (120 mph), it enters cruising mode
4. As it approaches Miami, it calculates stopping distance and begins braking
5. Once stopped at Miami, the GO button reappears for the return trip
