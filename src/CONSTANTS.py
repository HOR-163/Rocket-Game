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

# Physics constants
GRAVITY = 4
GROUND_FRICTION = 0.04
WIND_CHANCE = 1000 # Every frame takes the chance of 1 / n
WIND_DURATION = [2,4] # [x,y] x to y seconds of wind
MINIMUM_DISABLED = 1 # Minimum amount of seconds rocket is disabled when going through angry cloud
MAXIMUM_DISABLED = 3 # Maximum amount of seconds rocket is disabled when going through angry cloud


# Just some colors (for debug)
COLORS = ["red", "green", "blue", "yellow", "orange", "cyan", "magenta",]

# Powerups
OBJ_GEN_RADIUS = 7 # aka a (7+1+7)x(7+1+7) square of chunks where those powerups and obstacles are created (radius)
POWERUP_AMOUNTS = {"money": 15, "fuel": 15} # How many of each powerup will be generated
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

DEFAULT_PLAYER_DATA = {"starting_money": 100,
                       "starting_fuel": 100,
                       "magnet_radius": 200,
                       "minimap_radius": 3,
                       "upgrades": []}


# Game states
PAUSED = 0
PLAYING = 1





