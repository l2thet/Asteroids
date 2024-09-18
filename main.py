import pygame
from constants import *
from player import Player

def main():  
    pygame.init()
    flags = pygame.SCALED
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    
    clock = pygame.time.Clock()
    dt = 0
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        window_surface.fill((0, 0, 0))
        player.draw(window_surface)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
    
if __name__ == "__main__":
    main()