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

- **DEPART button** (green): Click to start the train from a station
- **STOP button** (red): Appears while train is moving; click to brake smoothly
- **RESUME button** (orange): Appears when paused mid-journey; click to resume
- The train handles acceleration and braking automatically when approaching stations

## How It Works

1. The train starts at NYC station
2. Press DEPART—the whistle sounds and the train accelerates
3. At max speed (120 mph), it enters cruising mode
4. You can press STOP at any time to smoothly brake the train
5. When paused mid-journey, press RESUME to continue toward the same destination
6. As it approaches a station, it calculates stopping distance and begins braking automatically
7. Once stopped at a station, the DEPART button reappears for the return trip
