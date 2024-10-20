import pygame
import random

from circleshape import CircleShape
from constants import *
from minorbuff import MinorBuff


class Asteroid(CircleShape):   
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(1, 0) * ASTEROID_SPEED
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt

        # Check if the asteroid is outside the viewable area
        if (self.position.x + self.radius < 0 or self.position.x - self.radius > SCREEN_WIDTH or
                self.position.y + self.radius < 0 or self.position.y - self.radius > SCREEN_HEIGHT):
            self.kill()
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            if random.random() < 0.1:
                minor_buff = MinorBuff(self.position.x, self.position.y)
                return [minor_buff]
            return
        random_angle = random.uniform(20, 50)
        asteroid_one_velocity = self.velocity.rotate(random_angle)
        asteroid_two_velocity = self.velocity.rotate(-random_angle)
        asteroid_new_radius = self.radius - ASTEROID_MIN_RADIUS
        return [(asteroid_new_radius, self.position, asteroid_one_velocity * 1.2),
                (asteroid_new_radius, self.position,  asteroid_two_velocity * 1.2)]
        
        