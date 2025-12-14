'''Main.py - Program Entry Point'''

import logging
import json
import pygame
import sys
from game import Game

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

def main_menu():
    return 'quit'

def main():
    '''
    main() is the program entry point.  It's where all the basic initialization
    occurs and where the program starts and ends.
    '''

    game_playing = True  # This is the boolean that keeps us from termination until the user chooses "quit"
    config = load_app_config("app_config.json") # Grab the app config
    configure_logging(config.get("logging")) # Use the logging section of the config to set up app logging
    logger = logging.getLogger("main") # Define a logger for main()

    logger.info("Config loaded and logging initialized.")

    logger.debug(config.get("logging")) 
    

    while game_playing:
        menu_selection = main_menu()

        match menu_selection:
            case 'new':
                # Initialize the game with default settings
                pass
            case 'load':
                # Initialize the game with settings from a file
                pass
            case 'options':
                # Go to the options page
                pass
            case 'quit':
                game_playing = False


if __name__ == "__main__":
    main()