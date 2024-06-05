import os

PATH = os.getcwd()
# For IDLE or if you opened not a folder, but a file, then uncomment the following line (in VSCode comment this line)
#PATH = PATH[:PATH.rfind("\\") + 1] # <------- This one

# Screen size
WIDTH: int = 1000
HEIGHT: int = 750

# Size of background chunks
C_WIDTH: int = 500
C_HEIGHT: int = 375
CHUNK_GEN_RADIUS = 3 # (3+1+3)x(3+1+3) square of chunks

# Colors
GROUND_COLOR = (224, 173, 52)
SKY_COLOR = (176, 235, 230)

TEXT_DEFAULT_COLOR = (215, 252, 212)
TEXT_HOVER_COLOR = (255, 255, 255)
TEXT_HEADER_COLOR = (182, 143, 64)
TEXT_BACKGROUND_COLOR = (0, 0, 0, 128)

BAR_COLOR = (255, 255, 255)
UPGRADES_BAR_WIDTH = 500
UPGRADES_BACKGROUND_COLOR = (128, 128, 128)

# Physics constants
GRAVITY = 4
GROUND_FRICTION = 0.04
FALL_SPEED = 2000
WIND_CHANCE = 1000 # Every frame takes the chance of 1 / n
WIND_DURATION = [2, 4] # [x,y] x to y seconds of wind
MAX_WIND_STRENGTH = 10
MINIMUM_DISABLED = 1 # Minimum amount of seconds rocket is disabled when going through angry cloud
MAXIMUM_DISABLED = 3 # Maximum amount of seconds rocket is disabled when going through angry cloud


# Just some colors (for debug)
COLORS = ["red", "green", "blue", "yellow", "orange", "cyan", "magenta",]

# Powerups
OBJ_GEN_RADIUS = 7 # aka a (7+1+7)x(7+1+7) square of chunks where those powerups and obstacles are created (radius)
POWERUP_AMOUNTS = {"money": 15, 
                   "fuel": 15} # How many of each powerup will be generated
COLLECTIBLE_OBJECTS = [x for x in POWERUP_AMOUNTS.keys()]

MONEY_VALUES = {1: 1,2: 10, 3: 50} # {level: value, ...}
FUEL_VALUES = {1: 1,2: 10, 3: 50} # {level: value, ...}

MINIMUM_OBJECT_HEIGHT = -C_HEIGHT * 2.5

# Obstacles
OBSTACLE_AMOUNT = 5
OBSTACLE_TYPES = {1: ["plane", "helicopter", "hot_air_balloon", "cloud"],
                  2: ["fighter_jet"],
                  3: ["UFO", "satellite"]}
ALL_OBSTACLES = [
    x
    for xs in list(OBSTACLE_TYPES.values())
    for x in xs
]
SOLID_OBSTACLES = ["plane", "helicopter", "hot_air_balloon", "fighter_jet", "UFO", "satellite"]

MOVING_OBJECTS = {"plane": {"horisontal": 5},
                    "helicopter": {"all": 2},
                    "hot_air_balloon": {"all": 1},
                    "fighter_jet": {"horisontal": 10},
                    "UFO": {"horisontal": 4}}

MAGNETIC_OBJECTS = ["fuel", "money"]

DEFAULT_PLAYER_DATA = {"money": 0,
                       "starting_fuel": 10,
                       "starting_speed": 500,
                       "fuel_level": 0,
                       "magnet_level": 0,
                       "map_level": 0,
                       "max_speed_level": 0}

UPGRADE_COSTS = {
    "magnet_level": [10, 20, 30, 40],
    "max_speed_level": [15, 30, 45, 60, 75],
    "fuel_level": [12, 24, 36, 48, 60],
    "map_level": [5, 10, 15, 20, 25, 30, 35]
}

FUEL_LEVEL_MULTIPLIER = 30
MAGNET_LEVEL_MULTIPLIER = 100
ROCKET_SPEED_MULTIPLIER = 300
MAP_MULTIPLIER = 1

# Game states
PAUSED = 0
PLAYING = 1





