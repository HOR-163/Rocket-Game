from CONSTANTS import *
from coordinate_systems import *
from gameobjects import Object


# List of money, fuel and obstacles (all that need collision detection)


# Just used for the first time
last_chunk_coordinates = (0,0)


def create_objects_for_the_first_time(collision_group, images: dict) -> None:
    global objects

    for object_type in POWERUP_AMOUNTS: # Go through all powerup types
        for _ in range(POWERUP_AMOUNTS[object_type]): # Amount of powerups
            random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-OBJ_GEN_RADIUS, OBJ_GEN_RADIUS)), 
                                                            (C_WIDTH * (OBJ_GEN_RADIUS * 2 + 1), C_HEIGHT * (OBJ_GEN_RADIUS * 2 + 1)))
            if object_type == "money":
                object_level = get_money_level(world_to_chunk_coordinates(random_coordinates))
                collision_group.add(Object(object_type, object_level, random_coordinates, images[object_level]))
            
            elif object_type == "fuel":
                object_level = get_fuel_level(world_to_chunk_coordinates(random_coordinates))
                collision_group.add(Object(object_type, object_level, random_coordinates, images[object_level + 3]))
    
    # Create x amount of obstacles 

    for _ in range(OBSTACLE_AMOUNT):
        random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-OBJ_GEN_RADIUS, OBJ_GEN_RADIUS)), 
                                                            (C_WIDTH * (OBJ_GEN_RADIUS * 2 + 1), C_HEIGHT * (OBJ_GEN_RADIUS * 2 + 1)))
        # Get the first level of obstacles, then get a random obstacle type from there
        object_type = OBSTACLE_TYPES[1][random.randint(0, len(OBSTACLE_TYPES[1])) - 1] # len - 1 (lists start from 0)
        collision_group.add(Object(object_type, 1, random_coordinates, images[object_type])) # Instead of 1, there could be None, because that value is unused for obstacles


def reset_objects(collision_group, images: dict) -> None:
    for object in collision_group:
        object_level = object.level
        random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-OBJ_GEN_RADIUS, OBJ_GEN_RADIUS)), 
                                                            (C_WIDTH * (OBJ_GEN_RADIUS * 2 + 1), C_HEIGHT * (OBJ_GEN_RADIUS * 2 + 1)))
        if object.type == "money":
            object_level = get_money_level(world_to_chunk_coordinates(random_coordinates))
            object.__init__(object.type, object_level, random_coordinates, images[object_level])
        
        elif object.type == "fuel":
            object_level = get_fuel_level(world_to_chunk_coordinates(random_coordinates))
            object.__init__(object.type, object_level, random_coordinates, images[object_level + 3])

        elif object.type in ALL_OBSTACLES:
            # Get the first level of obstacles, then get a random obstacle type from there
            object.type = OBSTACLE_TYPES[1][random.randint(0, len(OBSTACLE_TYPES[1])) - 1] # len - 1 (lists start from 0)
            object.__init__(object.type, 1, random_coordinates, images[object.type]) # Instead of 1, there could be None, because that value is unused for obstacles


            
def objects_load_unload(collision_group, chunk_coordinates: tuple[int, int], images) -> None:
    """
    Load and unload objects if they are too far from the rocket.
    
    `chunk_coordinates`: rocket's current chunk cooridnates
    `images`: dictionary of all original image instances
    """
    global last_chunk_coordinates

    if last_chunk_coordinates != chunk_coordinates:

        # See if some powerups could be removed
        for object in collision_group:
            if object.chunk_coordinates[1] < chunk_coordinates[1] - OBJ_GEN_RADIUS: # object is too low
                create_new_object(object, chunk_coordinates, "up", images)
            elif object.chunk_coordinates[1] > chunk_coordinates[1] + OBJ_GEN_RADIUS: # object is too high
                create_new_object(object, chunk_coordinates, "down", images)
            elif object.chunk_coordinates[0] < chunk_coordinates[0] - OBJ_GEN_RADIUS: # object is too left
                create_new_object(object, chunk_coordinates, "right", images)
            elif object.chunk_coordinates[0] > chunk_coordinates[0] + OBJ_GEN_RADIUS: # object is too right
                create_new_object(object, chunk_coordinates, "left", images)
        last_chunk_coordinates = chunk_coordinates

def get_money_level(chunk_coordinates: tuple[int,int]) -> int:
    # Create the odds of each powerup to be created
    if chunk_coordinates[1] + 1 < 100:
        coin_percent = 100 - 100 * (chunk_coordinates[1] + 2) / 400
        cash_percent = 100 - coin_percent
        #money_bag_percent = 0
    elif chunk_coordinates[1] + 1 >= 100 and chunk_coordinates[1] + 1 <= 199:
        coin_percent = 50 - 50 * (chunk_coordinates[1] - 100 + 2) / 250
        cash_percent = 50 + 50 * (chunk_coordinates[1] - 100 + 2) / 500
        #money_bag_percent = 100 - coin_percent - cash_percent
    elif chunk_coordinates[1] + 1 >= 200:
        coin_percent = 20
        cash_percent = 60
        #money_bag_percent = 20

    # Create a random number to find the level of fuel
    rng = random.randint(0,100)

    if rng < coin_percent:
        # make a coin
        return 1
    elif rng >= coin_percent and rng < coin_percent + cash_percent:
        # make a cash
        return 2
    # make a money_bag
    return 3

def get_fuel_level(chunk_coordinates: tuple[int,int]) -> int:
    # Create the odds of each powerup to be created
    if chunk_coordinates[1] + 1 < 100:
        small_percent = 100 - 100 * (chunk_coordinates[1] + 2) / 400
        medium_percent = 100 - small_percent
        #large_percent = 0
    elif chunk_coordinates[1] + 1 >= 100 and chunk_coordinates[1] + 1 <= 199:
        small_percent = 50 - 50 * (chunk_coordinates[1] - 100 + 2) / 250
        medium_percent = 50 + 50 * (chunk_coordinates[1] - 100 + 2) / 500
        #large_percent = 100 - small_percent - medium_percent
    elif chunk_coordinates[1] + 1 >= 200:
        small_percent = 20
        medium_percent = 60
        #large_percent = 20

    # Create a random number to find the level of fuel
    rng = random.randint(0,100)
        
    if rng < small_percent:
        # make a coin
        return 1
    elif rng >= small_percent and rng < small_percent + medium_percent:
        # make a cash
        return 2
    # make a money_bag
    return 3

def get_obstacle_level(chunk_coordinates: tuple[int, int]) -> int:
    if chunk_coordinates[1] < 100:
        return 1
    elif chunk_coordinates[1] < 200:
        return 2
    elif chunk_coordinates[1] >= 200:
        return 3

def create_new_object(object, chunk_coordinates: tuple[int, int], direction: str, images: dict) -> None:

    # Create random coordinates, where the powerup is going to be placed
    if direction == "up":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - OBJ_GEN_RADIUS,         # start_x
                                                                            chunk_coordinates[1] + OBJ_GEN_RADIUS - 1)),       # start_y
                                                                            (C_WIDTH * (OBJ_GEN_RADIUS * 2 + 1), C_HEIGHT))   # size
    elif direction == "down":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - OBJ_GEN_RADIUS,         # start_x
                                                                            chunk_coordinates[1] - OBJ_GEN_RADIUS)),       # start_y
                                                                            (C_WIDTH * (OBJ_GEN_RADIUS * 2 + 1), C_HEIGHT))    # size
    elif direction == "right":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] + OBJ_GEN_RADIUS - 1,     # start_x
                                                                            chunk_coordinates[1] + OBJ_GEN_RADIUS)),           # start_y
                                                                            (C_WIDTH, C_HEIGHT * (OBJ_GEN_RADIUS * 2 + 1)))    # size
    elif direction == "left":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - OBJ_GEN_RADIUS,     # start_x
                                                                            chunk_coordinates[1] + OBJ_GEN_RADIUS)),           # start_y
                                                                            (C_WIDTH, C_HEIGHT * (OBJ_GEN_RADIUS * 2 + 1)))    # size

    # Create powerups according to their type
    if object.type == "money":
        object_level = get_money_level(chunk_coordinates)
        object.__init__(object.type, object_level, random_position, images[object_level])

    elif object.type == "fuel":
        object_level = get_fuel_level(chunk_coordinates)
        object.__init__(object.type, object_level, random_position, images[object_level + 3])
    elif object.type in ALL_OBSTACLES:
        obstacle_level = get_obstacle_level(chunk_coordinates)
        obstacle_type = OBSTACLE_TYPES[obstacle_level][random.randint(0, len(OBSTACLE_TYPES[obstacle_level]) - 1)]
        object.__init__(obstacle_type, obstacle_level, random_position, images[obstacle_type])