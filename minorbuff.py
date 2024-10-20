import pygame
from circleshape import CircleShape
from constants import *

class MinorBuff(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, MINOR_BUFF_RADIUS)
        self.position = pygame.math.Vector2(x, y)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.position, self.radius, 2)

    def update(self, dt):
        pass