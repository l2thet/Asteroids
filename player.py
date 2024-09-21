import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    rotation = 0
    shot_cooldown = 0
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
        
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
            
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.shot_cooldown > 0:
            return
        else:
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN
            shot = Shot(self.position.x, self.position.y, forward * PLAYER_SHOOT_SPEED)