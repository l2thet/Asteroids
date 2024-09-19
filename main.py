import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():  
    pygame.init()
    flags = pygame.SCALED
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    
    clock = pygame.time.Clock()
    dt = 0
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()
    
    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group, drawable_group, shots_group)
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        window_surface.fill((0, 0, 0))
        dt = clock.tick(FPS) / 1000
        
        for updatable in updatable_group:
            updatable.update(dt)
        
        for asteroid in asteroid_group:
            if player.collission_check(asteroid):
                print("Game Over!")
                pygame.quit()
                return
        
        for drawable in drawable_group:
            drawable.draw(window_surface)
        
        pygame.display.flip()
    
if __name__ == "__main__":
    main()