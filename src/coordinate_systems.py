from CONSTANTS import *

def world_to_screen_coordinates(world_coords: tuple[int | None, int | None], rocket_position: tuple[int, int], scale: float) -> tuple[int, int]:
    """Convert world coordinates to screen coordinates."""
    screen_x, screen_y = None, None

    if world_coords[0] is not None:
        screen_x = int((-rocket_position[0] + world_coords[0]) * scale + WIDTH // 2)
    if world_coords[1] is not None:
        screen_y = int((-rocket_position[1] + world_coords[1]) * scale + HEIGHT // 2)

    return (screen_x, screen_y)

def screen_to_world_coordinates(screen_coords: tuple[int | None, int | None], rocket_position: tuple[int, int], scale: float) -> tuple[int, int]:
    """Convert screen coordinates to world coordinates."""
    world_x, world_y = None, None

    if screen_coords[0] is not None:
        world_x = int((2 * screen_coords[0] - WIDTH) // (2 * scale) + rocket_position[0])
    if screen_coords[1] is not None:
        world_y = int((2 * screen_coords[1] - HEIGHT) // (2 * scale) + rocket_position[1])

    return (world_x, world_y)