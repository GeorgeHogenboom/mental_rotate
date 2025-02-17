import os
import pygame
import random
import time
import sys

# Directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the 'photos' folder
photos_directory = os.path.join(script_directory, "photos")

# Pygame initialization 
pygame.init()

# List of the images either tools or non-tools located in \images
tool_images = ['stanleyknife.png', 'hammer.png', 'wrench.png', 'swissknife.png', 'jigsaw.png'] 
non_tool_images = ['shark.png','cactus.png', 'stomach.png', 'icicle.png', 'cordyceps.png','feather.png']
                   

def imagegen(mirror, angle, tool):
    """
    Displays two images with random rotation and measure reaction time.
    
    Parameters:
        mirror: 0 for non-mirrored, 1 for mirrored.
        angle: Rotation angle (in degrees).
        tool: 'tools' or 'non_tools' to determine which image set to use.
        
    Returns:
        keypress : The key pressed by the participant.
        reaction_time : Time in seconds from display until response.
    """
    #  Get the current active display resolution.
    screen = pygame.display.get_surface()
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
    
    # Make the path variable for compatibility with mac folder system / instead of \
    photo = os.path.normpath(photo)
    
    # Load the image using pygame and define it as image.
    image = pygame.image.load(photo).convert_alpha()

    # Make all the images same size
    fixed_size = (300, 300)
    fixed_image = pygame.transform.smoothscale(image, fixed_size)
    randomdegree = random.choice(range(360)) # Define a random degree for both images from 0-360 degrees

    # Apply transformations and rotate the images
    left_rotated = pygame.transform.rotate(fixed_image, randomdegree)
    right_fixed = pygame.transform.flip(fixed_image, True, False) if mirror else fixed_image #mirror if mirrored input = T
    total_angle = angle + randomdegree #calculate rotation second image with delta degrees
    right_rotated = pygame.transform.rotate(right_fixed, total_angle)

    # Adjust positions 
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


    # Wait for a keypress and measure reacture time
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
