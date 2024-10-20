import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, velocity, shot_radius):
        if shot_radius is None:
            super().__init__(x, y, SHOT_RADIUS)
        else:
            super().__init__(x, y, shot_radius)
        self.velocity = pygame.Vector2(velocity)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt