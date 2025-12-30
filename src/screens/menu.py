# src/menu.py

import pygame
import logging

class MainMenu:
    def __init__(self, screen, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen = screen
        self.config = config
        
        # Load colors/fonts from config
        self.bg_color = config.get('menu',{}).get('bg_color',[0,0,0])
        self.text_color = config.get('menu',{}).get('text_color',[255,255,255])
        raw_font_size = config.get('menu',{}).get('font_size', 60)
        self.font_size = raw_font_size if isinstance(raw_font_size, int) else 60
        self.logger.debug(f"Font size = {self.font_size}")
        self.font = pygame.font.Font(config.get('menu',{}).get('font','assets/fonts/Blox2.ttf'), self.font_size)
        
        self.screen_width = config.get('app',{}).get('screen_width',800)
        self.screen_height = config.get('app',{}).get('screen_height',800)

        # Define Menu Options and their Return Values
        self.menu_items = [
            {"label": "New Game", "action": "new"},
            {"label": "Load Game", "action": "load"},
            {"label": "Options",  "action": "options"},
            {"label": "Quit Game", "action": "quit"}
        ]
        
        # Create Rect objects for buttons (centered)
        self.buttons = []
        self._setup_buttons()

    def _setup_buttons(self):
        """Calculates positions and creates Rects for each menu item."""
        start_y = 200
        padding = 75
        
        for i, item in enumerate(self.menu_items):
            # Create a text surface to get the dimensions
            text_surf = self.font.render(item["label"], True, self.text_color)
            rect = text_surf.get_rect(center=(self.screen_width // 2, start_y + (i * padding)))
            
            # Store the rect and the associated action
            self.buttons.append({"rect": rect, "action": item["action"], "label": item["label"]})

    def _draw(self):
        """Draws the title and buttons."""
        self.screen.fill(self.bg_color)
        
        # Draw Title
        title_font = pygame.font.Font(self.config.get('menu',{}).get('font','assets/fonts/Blox2.ttf'), self.font_size + 20)
        title_surf = title_font.render(self.config.get('app', {}).get('name',"Blocks"), True, self.text_color)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_surf, title_rect)

        # Draw Buttons
        for btn in self.buttons:
            # Check if mouse is hovering (for a simple hover effect)
            mouse_pos = pygame.mouse.get_pos()
            color = (200, 200, 200) if btn["rect"].collidepoint(mouse_pos) else self.text_color
            
            text_surf = self.font.render(btn["label"], True, color)
            self.screen.blit(text_surf, btn["rect"])

        pygame.display.flip()

    def run(self):
        """
        The internal loop for the menu. 
        Returns the action string when a button is clicked.
        """
        self.logger.info("Menu opened.")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        for btn in self.buttons:
                            if btn["rect"].collidepoint(event.pos):
                                self.logger.info(f"Menu selection: {btn['action']}")
                                return btn["action"]

            self._draw()