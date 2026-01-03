import pygame

class Paddle:
    def __init__(self, y, x, width, height):
        '''
        Create a paddle
        
        :param self: It's a class.  Go figure.
        :param y: This is the y location.  It's a constant for the paddle.
        :param x: This is the x location.  It changes when the mouse moves.
        :param width: how wide the body of the paddle is
        :param height: how tall the body of the paddle is
        '''
        self.rect = pygame.Rect(x,y, width, height)
    
    def update_position(self, mouse_x, screen_width):
        '''
        Move the paddle to the location of the mouse
        
        :param self: This paddle.
        :param mouse_x: location of the mouse
        :param screen_width: how much screen we have to work with.
        '''
        new_x = mouse_x - (self.rect.width // 2)
        if new_x < 0:
            new_x = 0
        elif new_x > screen_width - self.rect.width:
            new_x = screen_width - self.rect.width
        self.rect.x = new_x