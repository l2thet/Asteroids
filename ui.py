import pygame
from constants import *

class UI(pygame.sprite.Sprite):
    paused = False
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        pass

    def draw(self, screen):
        if self.paused:
            text = self.font.render("Paused", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

    def get_time(self):
        return pygame.time.get_ticks() - self.start_time