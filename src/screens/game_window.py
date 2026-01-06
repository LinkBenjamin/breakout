import pygame
import logging
import math
import random
from core.ball import Ball
from core.paddle import Paddle
from core.level import Level

class GameWindow:
    def __init__(self, screen, config, data=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screen = screen
        self.config = config

        self.s_width = config.get('app', {}).get("screen_width", 800)
        p_width = self.s_width // 6

        self.s_height = config.get('app', {}).get("screen_height", 600)
        p_height = self.s_height // 20

        p_y = self.s_height - (2 * p_height)

        self.paddle = Paddle(p_y, self.s_width // 2, p_width, p_height)
        self.paddle_color = config.get('game', {}).get('paddle_color', [255,255,255])
        self.background_color = config.get('game', {}).get('background_color',[0,0,0])

        self.logger.debug(f"GameWindow initialized successfully.")

        self.balls = []

        ball_start = (self.s_width // 2, self.s_height - (3 * p_height))
        ball_radius = config.get('game',{}).get('default_ball_radius',10)
        ball = Ball((self.s_width,self.s_height),ball_start,ball_radius, (0,0))
        self.balls.append(ball)

        self.brick_color = config.get('game',{}).get('brick_color',[100,100,100])
        self.bricks = self.load_level(1)

    def load_level(self, lev):
        self.current_level = lev
        level = Level(lev, self.s_width, self.s_height)
        return level.load_level()

    def check_collision_side(self, ball, brick):
        # Calculate the overlap on all four sides
        dr = abs(ball.right - brick.left)
        dl = abs(ball.left - brick.right)
        db = abs(ball.bottom - brick.top)
        dt = abs(ball.top - brick.bottom)

        # Find the smallest overlap
        min_overlap = min(dr, dl, db, dt)

        if min_overlap == dr:
            return "right"  # Player hit the left side of the obstacle
        elif min_overlap == dl:
            return "left"   # Player hit the right side of the obstacle
        elif min_overlap == db:
            return "bottom" # Player hit the top of the obstacle
        elif min_overlap == dt:
            return "top"    # Player hit the bottom of the obstacle

    def start_play(self):
        self.logger.debug("Starting the first ball on the game board now...")
        self.balls[0].start_ball()

    def calculate_bounce_angle(self, ball, paddle, speed, max_angle_deg=70.0):
        # Calculate relative hit position (-1.0 to 1.0)
        paddle_center = float(paddle.centerx)
        relative_hit = (float(ball.centerx) - paddle_center) / (float(paddle.width) / 2)
        
        # Clamp the value to ensure it stays within -1 to 1 (in case of edge overlaps)
        relative_hit = max(-1, min(1, relative_hit))
        if abs(relative_hit) < 0.25:
            relative_hit = 0
        elif abs(relative_hit) < 0.5:
            relative_hit = random.uniform(0.01, 0.1)
            
        elif abs(relative_hit) < 0.75:
            relative_hit = random.uniform(0.1, 0.25)

        # Convert max angle to radians and calculate actual bounce angle
        max_angle_rad = math.radians(max_angle_deg)
        bounce_angle = relative_hit * max_angle_rad
        
        # Calculate new velocity vectors
        # We use sin for X and cos for Y because 0 degrees is "Straight Up"
        new_vel_x = -speed * math.sin(bounce_angle)
        new_vel_y = -speed * math.cos(bounce_angle) # Negative moves UP

        return (new_vel_x, new_vel_y)
        
    def run(self):
        clock = pygame.time.Clock()
        fps = self.config.get("app",{}).get('fps',60)
        running = True
        pygame.mouse.set_visible(False)
        throw_away_first_mouseup = False # We arrived at this screen by clicking - the mouseup will be captured here.  We need to ignore it.
        
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if not throw_away_first_mouseup:
                        throw_away_first_mouseup = True
                    else:
                        self.logger.debug(f"Detected Mouse UP: len(self.balls)={len(self.balls)}, vel_x={self.balls[0].vel_x}, vel_y={self.balls[0].vel_y}")
                        if len(self.balls) == 1 and self.balls[0].vel_x == 0 and self.balls[0].vel_y == 0:
                            self.start_play()
                if event.type == pygame.QUIT:
                    running = False
                
            mouse_x, _ = pygame.mouse.get_pos()

            self.screen.fill(self.background_color)

            self.paddle.update_position(mouse_x, self.s_width)
            pygame.draw.rect(self.screen, self.paddle_color, self.paddle.rect)

            for ball in self.balls:
                ball.update_position()
                pygame.draw.circle(self.screen,[255,255,255],ball.rect.center,ball.radius)

                if ball.rect.colliderect(self.paddle.rect):
                    self.logger.info(f"Paddle Hit: p{self.paddle.rect.centerx}, b{ball.rect.centerx}, s{ball.speed}")
                    v_new = self.calculate_bounce_angle(self.paddle.rect,ball.rect, ball.speed)
                    self.logger.debug(f"New Velocity: {v_new}")
                    ball.vel_x = v_new[0]
                    ball.vel_y = v_new[1]
                    ball.rect.bottom = self.paddle.rect.top
                
                new_bricks = []
                for brick in self.bricks:
                    if ball.rect.colliderect(brick):
                        cside = self.check_collision_side(ball.rect, brick)
                        self.logger.info(f"Brick hit on {cside}!")
                        if cside in ['left', 'right']:
                            ball.vel_x *= -1
                        if cside in ['top', 'bottom']:
                            ball.vel_y *= -1
                    else:
                        new_bricks.append(brick)
                    pygame.draw.rect(self.screen, self.brick_color,brick)
                self.bricks = new_bricks

            pygame.display.flip()  

            self.balls = [b for b in self.balls if not b.handle_wall_collisions()]
            if not self.balls:
                running = False # Game over, you lost the last one
            if not self.bricks:
                # do something, you won!
                pass

        pygame.mouse.set_visible(True)
        return "MENU"