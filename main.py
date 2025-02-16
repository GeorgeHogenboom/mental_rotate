import os
# Force SDL to center the Pygame window when it is created.
os.environ["SDL_VIDEO_CENTERED"] = "1"

import random
import itertools
import csv
import pygame
import sys
import pandas as pd
import time
from imagegen import imagegen  # Use your fixed imagegen.py

def is_correct(key_pressed, mirror_flag):
    """
    Check whether the key pressed is correct based on the mirrored flag.
    If mirror_flag == 1 (mirrored trial), the correct key is 'f'.
    If mirror_flag == 0 (non-mirrored trial), the correct key is 'j'.
    """
    if mirror_flag == 1:
        return 'correct' if key_pressed == 'f' else 'incorrect'
    else:
        return 'correct' if key_pressed == 'j' else 'incorrect'

def save_data(data_all_trials,user_number):
    """
    Save participant data to the data directory.
    """
    # Convert data rows to a Pandas DataFrame
    df = pd.DataFrame(data_all_trials)
    print(f"\nObtained data:\n{df}\n")

    # Define the filename within a 'data' folder inside the script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_directory, "data")
    os.makedirs(data_dir, exist_ok=True)  # Create folder if it doesn't exist
    filename = os.path.join(data_dir, f"data{user_number}.csv")

    # Save the DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"Saved data in:\n{filename}\n")

def wait_for_keypress():
    """Wait until the participant presses any key."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def instructionphase(screen):
    """
    Display instruction screens in pygame that mimic your original look.
    Each screen shows white text on a black background and waits for any keypress.
    """
    # Screen 1: "Click to start!"
    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont("Arial", 30)
    text = font_large.render("Click to start!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    wait_for_keypress()

    # Screen 2: Informed Consent
    screen.fill((0, 0, 0))
    font_medium = pygame.font.SysFont("Arial", 20)
    lines = [
        "INFORMED CONSENT",
        "In this experiment, we collect anonymized data, including:",
        "- Your test responses",
        "- Sex assigned at birth",
        "- Age",
        "- Handedness (left/right)",
        "Your participation is voluntary. You can withdraw at any time.",
        "By continuing, you consent to the collection of this data.",
        "Press any key to continue..."
    ]
    y = screen.get_height() * 0.2
    for line in lines:
        rendered_text = font_medium.render(line, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(screen.get_width() / 2, y))
        screen.blit(rendered_text, text_rect)
        y += 30
    pygame.display.flip()
    wait_for_keypress()

    # Screen 3: Welcome Message
    screen.fill((0, 0, 0))
    lines = [
        "Welcome, to the mental_rotation task!",
        "Press any key to continue to the instructions..."
    ]
    y = screen.get_height() * 0.4
    for line in lines:
        rendered_text = font_large.render(line, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(screen.get_width() / 2, y))
        screen.blit(rendered_text, text_rect)
        y += 40
    pygame.display.flip()
    wait_for_keypress()

    # Screen 4: Experiment Instructions
    screen.fill((0, 0, 0))
    lines = [
        "This experiment contains several objects, which are tools or non_tools.",
        "Your goal is to determine whether the two objects are mirrored or not.",
        "The objects are positioned at different angles.",
        "Press F if a target is mirrored, or J if they are not mirrored.",
        "Press any key to continue to the test phase..."
    ]
    y = screen.get_height() * 0.3
    for line in lines:
        rendered_text = font_medium.render(line, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(screen.get_width() / 2, y))
        screen.blit(rendered_text, text_rect)
        y += 30
    pygame.display.flip()
    wait_for_keypress()

    # Screen 5: Test Phase Instructions
    screen.fill((0, 0, 0))
    lines = [
        "This is the test phase.",
        "A test phase will help you get used to the task.",
        "You need to get at least 80% correct (16/20) to continue.",
        "Press any key to start the test phase..."
    ]
    y = screen.get_height() * 0.4
    for line in lines:
        rendered_text = font_medium.render(line, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=(screen.get_width() / 2, y))
        screen.blit(rendered_text, text_rect)
        y += 30
    pygame.display.flip()
    wait_for_keypress()

def trainingphase(screen):
    """
    Runs a training phase where participants practice the mental rotation task.
    They must complete 20 practice trials with at least 80% correct (16/20) to proceed.
    """
    # Define the training conditions (all 20 unique combinations: 2*5*2 = 20)
    mirrored = [0, 1]
    angles = [0, 45, 90, 135, 180]
    categories = ['tools', 'non_tools']
    all_combinations = list(itertools.product(mirrored, angles, categories))
    # Randomize order (there are exactly 20 trials)
    test_trials = random.sample(all_combinations, 20)
    required_correct = 16

    while True:
        correct_count = 0  # Reset counter each attempt
        # Run through each training trial
        for trial in test_trials:
            mirror_flag, angle, category = trial
            key, reaction, random_image = imagegen(mirror_flag, angle, category)
            result = is_correct(key, mirror_flag)
            if result == 'correct':
                correct_count += 1

        if correct_count >= required_correct:
            # Show success feedback
            screen.fill((0, 0, 0))
            font_medium = pygame.font.SysFont("Arial", 20)
            success_text = font_medium.render(
                f"You've passed the training phase with {correct_count} correct responses.",
                True, (255, 255, 255)
            )
            text_rect = success_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(success_text, text_rect)
            pygame.display.flip()
            wait_for_keypress()
            break
        else:
            # Show failure feedback and retry prompt
            screen.fill((0, 0, 0))
            font_medium = pygame.font.SysFont("Arial", 20)
            fail_text = font_medium.render(
                "You failed the training phase. Press any key to retry...",
                True, (255, 255, 255)
            )
            text_rect = fail_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(fail_text, text_rect)
            pygame.display.flip()
            wait_for_keypress()
            # Resample a new set of 20 trials
            test_trials = random.sample(all_combinations, 20)

    # Screen 1: "Click to start!"

    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont("Arial", 30)
    text = font_large.render("The experiment will now start. Press any key to continue...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    wait_for_keypress()


def get_key():
    """
    Waits for a KEYDOWN event and returns the pressed key as a lowercase character.
    """
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            # Use event.unicode if available; fallback to pygame.key.name.
            if event.unicode:
                return event.unicode.lower()
            else:
                return pygame.key.name(event.key)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def completionphase(screen):
    """
    Handles the completion phase of the experiment by displaying messages and
    collecting user input for sex assigned at birth and handedness.

    This function:
    - Displays a completion message.
    - Prompts the user for their sex assigned at birth (F/M) until valid input is received.
    - Prompts the user for their handedness (L/R) until valid input is received.
    - Displays a thank-you message and waits for any key press.

    Returns:
        tuple: (user_input_hand, user_input_gender)
            - user_input_hand (str): 'l' for left-handed or 'r' for right-handed.
            - user_input_gender (str): 'f' for female or 'm' for male.
    """
    # Define valid options.
    gender_options = ['f', 'm']
    hand_options = ['l', 'r']

    font_large = pygame.font.SysFont("Arial", 30)

    # -- Display completion message --
    screen.fill((0, 0, 0))
    msg1 = font_large.render("You have completed the experiment.", True, (255, 255, 255))
    msg2 = font_large.render("Press any key to continue to the questions...", True, (255, 255, 255))
    rect1 = msg1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    rect2 = msg2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(msg1, rect1)
    screen.blit(msg2, rect2)
    pygame.display.flip()
    wait_for_keypress()  # already defined in your code

    # -- Collect Sex Assigned at Birth --
    user_input_gender = ''
    while user_input_gender not in gender_options:
        screen.fill((0, 0, 0))
        question = font_large.render("What is your sex assigned at birth? (F/M)", True, (255, 255, 255))
        rect = question.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(question, rect)
        pygame.display.flip()
        user_input_gender = get_key()

    # -- Collect Handedness --
    user_input_hand = ''
    while user_input_hand not in hand_options:
        screen.fill((0, 0, 0))
        question = font_large.render("Are you left-handed or right-handed? (L/R)", True, (255, 255, 255))
        rect = question.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(question, rect)
        pygame.display.flip()
        user_input_hand = get_key()

    # -- Display Thank-You Message --
    screen.fill((0, 0, 0))
    thanks1 = font_large.render("Thank you for participating in the experiment.", True, (255, 255, 255))
    thanks2 = font_large.render("Press any key to exit...", True, (255, 255, 255))
    rect1 = thanks1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    rect2 = thanks2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(thanks1, rect1)
    screen.blit(thanks2, rect2)
    pygame.display.flip()
    wait_for_keypress()

    return user_input_hand, user_input_gender


def pause_screen():
    font = pygame.font.Font(None, 36)


    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    screen.fill((0, 0, 0))
    font_large = pygame.font.SysFont("Arial", 30)
    msg1 = font_large.render("This is a Pause", True, (255, 255, 255))
    msg2 = font_large.render("Press any key to continue with the experiment...", True, (255, 255, 255))
    rect1 = msg1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    rect2 = msg2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(msg1, rect1)
    screen.blit(msg2, rect2)
    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # Resume when any key is pressed


def run_rotation_experiment():
    # Define conditions for the main experiment
    global user_number
    mirrored = [0, 1]
    angles = [0, 45, 90, 135, 180]
    categories = ['tools', 'non_tools']
    data_all_trials = []

    # Create trial combinations (repeat them to reach the desired trial count)
    combinations_tools = list(itertools.product(mirrored, angles, ['tools'])) * 10
    combinations_non_tools = list(itertools.product(mirrored, angles, ['non_tools'])) * 10
    combinations = combinations_tools + combinations_non_tools
    random.shuffle(combinations)
    print(combinations)
    print("Total trials:", len(combinations))

    trial_counter = 1
    i = 0  # current trial index
    while i < len(combinations):
        current_trial = combinations[i]
        mirror_flag = current_trial[0]
        angle = current_trial[1]
        category = current_trial[2]

        if i % 41 == 0 and i != 0:
            pause_screen()
        # Run a single trial with the current parameters.
        key, reaction, random_image = imagegen(mirror_flag, angle, category)
        
        # Determine correct key mapping: 'f' if mirrored, 'j' if not.
        correct_key = 'f' if mirror_flag == 1 else 'j'
        result = is_correct(key, mirror_flag)

        trial_counter += 1
        
        # If response is incorrect, reappend the trial for additional measurement.
        if result != 'correct':
            combinations.append(current_trial)

        print(f'dit is de key: {key}')
        print(f'Dit is de reaction time: {reaction}')

        # Store trial data
        data_single_trial = {
            "mirrorered": current_trial[0],
            "angle": current_trial[1],
            "toolness": current_trial[2],
            "key": key,
            "rt": reaction,
            "correctness": result,
            "image": random_image 
        }
        print(data_single_trial)
        data_all_trials.append(data_single_trial)
        print(len(combinations))
        
        i += 1

    save_data(data_all_trials,user_number)

def main():

    


    pygame.init()
    # Create a windowed fullscreen (borderless) window.
    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    pygame.display.set_caption("Mental Rotation Experiment")
    
    # Run the instruction phase in pygame.
    instructionphase(screen)
    
    # Run the training phase.
    trainingphase(screen)
    
    # Run the main experiment.
    run_rotation_experiment()

    handedness, gender = completionphase(screen)
    print("Collected Data:")
    print("Handedness:", handedness)
    print("Gender:", gender)

    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    user_number = input('What is the user number: \n')
    main()
