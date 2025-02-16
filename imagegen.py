import os
import pygame
import random
import time
import sys

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
# Define the path to the 'photos' folder
photos_directory = os.path.join(script_directory, "photos")

# Pygame initialization (only do this once)
pygame.init()
# Create the initial display surface. This might be replaced later by main.py.
_initial_screen = pygame.display.set_mode((1920, 1080))

# Define tool and non-tool images with correct extensions
tool_images = ['stanleyknife.png', 'hammer.png', 'wrench.png', 'swissknife.png', 'jigsaw.png'] 
non_tool_images = ['shark.png','cactus.png', 'stomach.png', 'icicle.png', 'cordyceps.png','feather.png']
                   

def imagegen(mirror, angle, tool):
    """
    Displays two images with random rotation and measures reaction time.
    
    Parameters:
        mirror (int): 0 for non-mirrored, 1 for mirrored.
        angle (int): Rotation angle (in degrees).
        tool (str): 'tools' or 'non_tools' to determine which image set to use.
        
    Returns:
        keypress (str): The key pressed by the participant.
        reaction_time (float): Time in seconds from display until response.
    """
    # Always get the current active display surface.
    screen = pygame.display.get_surface()
    if screen is None:
        raise Exception("Display Surface is not initialized.")

    screen.fill((255, 255, 255))  # Clear screen
    
    # Select a random image based on category
    if tool == 'tools':
        random_image = random.choice(tool_images)
        photo = os.path.join(photos_directory, random_image)
    elif tool == 'non_tools':
        random_image = random.choice(non_tool_images)
        photo = os.path.join(photos_directory, random_image)
    else:
        raise ValueError("Invalid tool category")
    
    # Normalize path to avoid errors
    photo = os.path.normpath(photo)
    
    # Load and process image
    try:
        image = pygame.image.load(photo).convert_alpha()
    except Exception as e:
        print(f"Error loading image: {photo}")
        raise e

    fixed_size = (300, 300)
    fixed_image = pygame.transform.smoothscale(image, fixed_size)
    randomdegree = random.choice(range(360))

    # Apply transformations
    left_rotated = pygame.transform.rotate(fixed_image, randomdegree)
    right_fixed = pygame.transform.flip(fixed_image, True, False) if mirror else fixed_image
    total_angle = angle + randomdegree
    right_rotated = pygame.transform.rotate(right_fixed, total_angle)

    # Adjust positions for balance
    left_rect = left_rotated.get_rect(center=(650, 540))
    right_rect = right_rotated.get_rect(center=(1250, 540))
    
    # Draw images and a separating line
    screen.blit(left_rotated, left_rect)
    screen.blit(right_rotated, right_rect)
    pygame.draw.line(screen, (0, 0, 0), (960, 300), (960, 800), 3)
    
    pygame.display.flip()

    # Reaction time measurement
    start_time = time.time()
    waiting = True
    keypress = None
    reaction_time = None

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit experiment
                    pygame.quit()
                    sys.exit()
                keypress = pygame.key.name(event.key)
                reaction_time = time.time() - start_time
                waiting = False
    
    return keypress, reaction_time, random_image
