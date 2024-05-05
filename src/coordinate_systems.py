from CONSTANTS import *
import random

def world_to_screen_coordinates(world_coords: tuple[int | None, int | None], rocket_position: tuple[int, int], scale: float) -> tuple[int | None, int | None]:
    """Convert world coordinates to screen coordinates."""
    screen_x, screen_y = None, None

    if world_coords[0] is not None:
        screen_x = int((-rocket_position[0] + world_coords[0]) * scale + WIDTH // 2)
    if world_coords[1] is not None:
        screen_y = int((-rocket_position[1] + world_coords[1]) * scale + HEIGHT // 2)

    return (screen_x, screen_y)

def screen_to_world_coordinates(screen_coords: tuple[int | None, int | None], rocket_position: tuple[int, int], scale: float) -> tuple[int | None, int | None]:
    """Convert screen coordinates to world coordinates."""
    world_x, world_y = None, None

    if screen_coords[0] is not None:
        world_x = int((2 * screen_coords[0] - WIDTH) // (2 * scale) + rocket_position[0])
    if screen_coords[1] is not None:
        world_y = int((2 * screen_coords[1] - HEIGHT) // (2 * scale) + rocket_position[1])

    return (world_x, world_y)

def world_to_chunk_coordinates(world_coords: tuple[int | None, int | None]) -> tuple[int | None, int | None]:
    """#### Convert world coordinates to chunk coordinates."""

    chunk_x, chunk_y = None, None

    if world_coords[0] is not None:
        chunk_x = int((world_coords[0] - (WIDTH - C_WIDTH) // 2) // C_WIDTH)
    if world_coords[1] is not None:
        chunk_y = int((-world_coords[1] + (HEIGHT - C_HEIGHT) // 2) // C_HEIGHT)

    return (chunk_x, chunk_y)

def chunk_to_world_coordinates(chunk_coords: tuple[int | None, int | None]) -> tuple[int | None, int | None]:
    """
    Convert chunk coordinates to world coordinates.

    World coordinates will be in the bottom left corner of the chunk.
    """
    world_x, world_y = None, None

    if chunk_coords[0] is not None:
        world_x = chunk_coords[0] * C_WIDTH + (WIDTH - C_WIDTH) // 2
    if chunk_coords[1] is not None:
        world_y = chunk_coords[1] * C_HEIGHT + (HEIGHT - C_HEIGHT) // 2
    return (world_x, -world_y)

def create_random_coordinates(coordinates: tuple[int, int], size: tuple[int, int]) -> tuple[int,int]:
    """Create random coordinates in a rectangle that starts from coordinates and has a size"""
    return (random.randint(coordinates[0], coordinates[0] + size[0]), 
            random.randint(coordinates[1], coordinates[1] + size[1]))