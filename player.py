import pygame
from triangleshape import TriangleShape
from constants import *
from shot import Shot
from ui import UI

class Player(TriangleShape):
    rotation = 0
    shot_cooldown = 0
    joystick = None
    paused = False
    pause_button_pressed = False

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.joystick = None

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
    def triangle(self):
        # Calculate the vertices of the triangle based on the position and rotation
        a = self.position + pygame.Vector2(0, -self.radius).rotate(self.rotation)
        b = self.position + pygame.Vector2(self.radius, self.radius).rotate(self.rotation)
        c = self.position + pygame.Vector2(-self.radius, self.radius).rotate(self.rotation)
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 0, 0), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(-dt)
        if keys[pygame.K_s]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shot_cooldown -= dt
            self.shoot()
        
        # Handle joystick input
        if self.joystick:
            x_axis = self.joystick.get_axis(0)
            y_axis = self.joystick.get_axis(1)
            
            # Apply dead zone threshold
            if abs(x_axis) < CONTROLLER_DEAD_ZONE:
                x_axis = 0
            if abs(y_axis) < CONTROLLER_DEAD_ZONE:
                y_axis = 0
            
            # Rotate and move based on joystick input
            self.rotation += x_axis * PLAYER_TURN_SPEED * dt
            self.move(y_axis * dt)

            # Shoot if the joystick trigger is pressed
            if self.joystick.get_button(0):
                self.shot_cooldown -= dt
                self.shoot()
        
        # Ensure the player stays within the viewable area
        self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.position.y))
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.shot_cooldown <= 0:
            # Calculate the front vertex of the triangle
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
            shot_position = self.position + forward * self.radius
            shot_velocity = forward * SHOT_SPEED
            Shot(shot_position.x, shot_position.y, shot_velocity)
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN

    def handle_pause_input(self):
        if self.joystick:
            if self.joystick.get_button(7):
                if not self.pause_button_pressed:
                    self.toggle_pause()
                    self.pause_button_pressed = True
            else:
                self.pause_button_pressed = False

    def toggle_pause(self):
        self.paused = not self.paused