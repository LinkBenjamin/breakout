import pygame

class Ball:
    def __init__(self, boundaries, position, radius, velocities):
        '''
        Generate a new Ball
        
        :param self: We're in a class.  Go figure.
        :param boundaries: a Tuple representing the upper bounds of the screen (lower bounds are 0,0)
        :param position: a Tuple representing the current location
        :param radius: an Integer representing the radius of a ball
        :param velocities: a Tuple representing the horizontal and vertical velocities of the ball)
        '''
        self.radius = radius
        self.x = float(position[0])
        self.y = float(position[1])
        self.rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)

        self.speed = 7

        # Velocity components
        self.vel_x = float(velocities[0])
        self.vel_y = float(velocities[1])

        self.screen_width = boundaries[0]
        self.screen_height = boundaries[1]

    def start_ball(self):
        '''
        Method to be called when starting the first ball on a game board.  It will sit still until this method is called to set its initial velocity, which is to drop (straight vertical) at speed 1.
        
        :param self: This ball
        '''
        self.vel_y = self.speed

    def update_position(self):
        """Pure math: Move the ball based on current velocity."""
        self.x += self.vel_x
        self.y += self.vel_y

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce_x(self):
        """Reverse horizontal direction."""
        self.vel_x = -self.vel_x

    def bounce_y(self):
        """Reverse vertical direction."""
        self.vel_y = -self.vel_y

    def handle_wall_collisions(self):
        """Check for screen boundary hits and bounce."""
        # Hit left or right walls
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.bounce_x()
            
        # Hit top wall
        if self.rect.top <= 0:
            self.bounce_y()
            
        # Return True if the ball falls off the bottom (Game Over trigger)
        if self.rect.bottom >= self.screen_height:
            return True
        return False