import pygame
from triangleshape import TriangleShape
from constants import *
from shot import Shot

class Player(TriangleShape):
    rotation = 0
    shot_cooldown = 0
    joystick = None

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
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shot_cooldown -= dt
            self.shoot()
        
        # Handle joystick input
        if self.joystick:
            x_axis = self.joystick.get_axis(0)  # X-axis
            y_axis = self.joystick.get_axis(1)  # Y-axis
            if x_axis < -0.10:  # Left
                self.rotate(dt * x_axis)
            if x_axis > 0.10:  # Right
                self.rotate(dt * x_axis)
            if y_axis > -0.3:  # Up
                self.move(dt * y_axis)
            if y_axis < 0.3:  # Down
                self.move(dt * y_axis)
            if self.joystick.get_button(0):  # Button 0
                self.shot_cooldown -= dt
                self.shoot()
            
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