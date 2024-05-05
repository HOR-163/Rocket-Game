# Screen size
WIDTH: int = 1000
HEIGHT: int = 750

# Size of background chunks
C_WIDTH: int = WIDTH / 2
C_HEIGHT: int = HEIGHT / 2

# Colors
GROUND_COLOR = (224, 173, 52)
SKY_COLOR = (176, 235, 230)

# Physics constants
GRAVITY = 4
FALL_SPEED = 600
GROUND_FRICTION = 0.04

# Just some colors (for debug)
COLORS = ["red", "green", "blue", "yellow", "orange", "cyan", "magenta"]

# Powerups
chunks_to_generate_powerups = 7 # aka a (7+1+7)x(7+1+7) square of chunks where those powerups and obstacles are created (radius)
powerup_amounts = {"money": 10, "fuel": 10} # How many of each powerup will be generated

# Obstacles
obstacle_amount = 5
obstacle_types = {1: ["plane", "helicopter", "hot_air_balloon", "cloud"],
                  2: ["fighter_jet"],
                  3: ["UFO", "satellite"]}
all_obstacles = [
    x
    for xs in list(obstacle_types.values())
    for x in xs
]




