'''Main.py - Program Entry Point'''

import logging
import json
import pygame
import sys
from core.game import Game
from screens.menu import MainMenu

CONFIG_FILE_PATH = "app_config.json"
logger = None

def configure_logging(config):
    '''
    configure_logging(config)
    
    :param config: Dictionary with 'level' and (optionally) 'file' defined.
    '''

    l = logging.getLevelName(logging._nameToLevel.get(config.get("level").upper(), logging.DEBUG)) 
    # Get the level from the dict, or default to DEBUG if it's wrong or missing so they can see the configuration isn't right in the log file.
    # These are nested because we only have to do it once, but the gist is that log levels are stored as both ints and strs at various points
    #   and we have to do a mapping thing to end up with the log level object we need for basicConfig().

    file = config.get("file", None)
    # Get the file from the dict, if provided. None is ok... we'll just not configure logging to a file in that case.

    handlerz = [logging.StreamHandler(sys.stdout)]
    # Always log to stdout
    if file:
        handlerz.append(logging.FileHandler(file, mode='a'))
        # Configure a log file if they asked for one

    logging.basicConfig(
        level=l, # Sets the minimum level to process (e.g., ignore DEBUG messages)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlerz
    )
    # All set - we've built the log level, format, and handlers.

def load_app_config(filename):
    '''
    load_app_config: loads the configuration from the json file
    
    :param filename: the name of the config file.
    '''
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_app_config(config, filename):
    '''
    save_app_config - Storing the application configuration back to the config file so that it will remember your preferences
    
    :param config: A dictionary representing the app config we're going to store
    :param filename: The name of the json file it should be stored in
    '''
    logger.info(f"Saving Configuration File to {filename}")
    try:
        # 1. Open the file in 'w' (write) mode to overwrite the contents
        with open(CONFIG_FILE_PATH, 'w') as f:
            
            # 2. Use json.dump() to write the Python dictionary to the file
            json.dump(
                config,  # The data to be written
                filename,            # The file object
                indent=4      # A crucial argument for human-readable output
            )        
    except IOError as e:
        logger.error(f"Failed to save configuration file: {e}")

def main_menu_screen(screen, config):
    """
    Creates the Menu instance and waits for a choice.
    """
    menu = MainMenu(screen, config)
    response = menu.run() # This blocks until a choice is made
    return response

def main():
    '''
    main() is the program entry point.  It's where all the basic initialization
    occurs and where the program starts and ends.
    '''

    game_playing = True  # This is the boolean that keeps us from termination until the user chooses "quit"
    config = load_app_config(CONFIG_FILE_PATH) # Grab the app config
    configure_logging(config.get("logging")) # Use the logging section of the config to set up app logging
    logger = logging.getLogger("main") # Define a logger for main()

    logger.info("Config loaded and logging initialized.")
    logger.debug(config.get("logging")) 

    pygame.init()
    screen = pygame.display.set_mode((config['app']['screen_width'], config['app']['screen_height']))
    pygame.display.set_caption(config['app']['name'])
    
    while game_playing:
        logger.info("Calling Main Menu")
        menu_selection = main_menu_screen(screen, config)
        logger.debug(f"Menu Selection: {menu_selection}")

        match menu_selection:
            case 'new':
                logger.debug("Matched 'new'")
                # Initialize the game with default settings
                pass
            case 'load':
                logger.debug("Matched 'load'")
                # Initialize the game with settings from a file
                pass
            case 'options':
                logger.debug("Matched 'options'")
                # Go to the options page
                pass
            case 'quit':
                logger.debug("Matched 'quit'")
                game_playing = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()