import pygame
from constants import *

class UI(pygame.sprite.Sprite):
    paused = False
    font = None
    start_time = 0
    score_text = ""
    elapsed_time_text = ""

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        # Generate "Survived:" text in white
        self.score_text = self.font.render('Survived:', True, (255, 255, 255))
        self.score_text_width = self.score_text.get_width()

         # Calculate elapsed time
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
        self.elapsed_time_text = f'{self.elapsed_time}'

        # Render elapsed time in red
        self.elapsed_time_text = self.font.render(f'{self.elapsed_time}', True, (255, 255, 255))

        pass

    def draw(self, screen):
        # Calculate positions
        surface_width = screen.get_width()
        x_score = surface_width - self.score_text_width - self.elapsed_time_text.get_width() - 10  # 10 pixels padding from the right edge
        x_time = x_score + self.score_text_width
        y = 10  # 10 pixels padding from the top edge
            
        # Blit texts to the screen
        screen.blit(self.score_text, (x_score, y))
        screen.blit(self.elapsed_time_text, (x_time, y))

        if self.paused:
            text = self.font.render("Paused", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

    def get_time(self):
        return pygame.time.get_ticks() - self.start_time