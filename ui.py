import pygame
from constants import *

class UI(pygame.sprite.Sprite):
    paused = False
    font = None
    start_time = 0
    survived_text = ""
    elapsed_time_text = ""

    def __init__(self, items, font_size=36):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.items = items
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.selected_index = 0
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        self.build_survived_text()
        pass

    def draw(self, surface):
        self.draw_survived(surface)    

        if self.paused:
            surface.fill((0, 0, 0))
            for i, item in enumerate(self.items):
                color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
                text_surface = self.font.render(item, True, color)
                text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + i * self.font_size))
                surface.blit(text_surface, text_rect)

    def get_time(self):
        return pygame.time.get_ticks() - self.start_time
    
    def build_survived_text(self):
        self.survived_text = self.font.render('Survived:', True, (255, 255, 255))
        self.score_text_width = self.survived_text.get_width()

        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
        self.elapsed_time_text = f'{self.elapsed_time}'

        self.elapsed_time_text = self.font.render(f'{self.elapsed_time}', True, (255, 255, 255))

    def draw_survived(self, screen):
        # Calculate positions
        surface_width = screen.get_width()
        x_score = surface_width - self.score_text_width - self.elapsed_time_text.get_width() - 10  # 10 pixels padding from the right edge
        x_time = x_score + self.score_text_width
        y = 10  # 10 pixels padding from the top edge
            
        screen.blit(self.survived_text, (x_score, y))
        screen.blit(self.elapsed_time_text, (x_time, y))
    
    def navigate(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.items)

    def select(self):
        return self.items[self.selected_index]