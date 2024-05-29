from math import *

def info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, dt, highest_dt):
    x_position, y_position = rocket.position
    x_speed, y_speed = rocket.speed
    x_acc = round((x_speed - last_speed[0]), 3)
    y_acc = round((y_speed - last_speed[1]), 3)

    angle = round(rocket.angle, 3)
    texts = [debug_font.render(f"x-position: {round(x_position, 3)}", True, 'red', 'white'),
             debug_font.render(f"y-position: {round(y_position, 3)}", True, 'blue', 'white'),
             debug_font.render(f"Chunk based position: {chunk_coordinates[0]} {chunk_coordinates[1]}", True, 'black', 'white'),
             debug_font.render(f"x-speed: {-round(x_speed, 3)}", True, 'red', 'white'),
             debug_font.render(f"y-speed: {-round(y_speed, 3)}", True, 'blue', 'white'),
             debug_font.render(f"Actual speed: {round(sqrt(x_speed ** 2 + y_speed ** 2),3)}", True, 'black', 'white'),
             debug_font.render(f"x-acceleration: {-x_acc}", True, 'red', 'white'),
             debug_font.render(f"y-acceleration: {-y_acc}", True, 'blue', 'white'),
             debug_font.render(f"Angle: {-angle}", True, 'red', 'white'),
             debug_font.render(f"Scale: {round(scale, 2)}", True, 'black', 'white'),
             debug_font.render(f"FPS: {round(1/(dt), 3)}", True, 'black', 'white'),
             debug_font.render(f"lowest FPS: {round(1/(highest_dt))}", True, 'black', 'white'), 
             ]
    for index, text in enumerate(texts):
        screen.blit(text, (0, index * 16))