import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from ui import UI

def main():  
    pygame.init()
    pygame.font.init()


    flags = pygame.SCALED
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

    def draw():
        window_surface.fill((0, 0, 0))
        
        for drawable in drawable_group:
            drawable.draw(window_surface)
            
        pygame.display.flip()
    
    
    clock = pygame.time.Clock()
    dt = 0
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()
    
    ui = UI()
    updatable_group.add(ui)
    drawable_group.add(ui)

    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group, drawable_group, shots_group)
    UI.containers = (updatable_group, drawable_group)
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()

    paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        UI.paused = paused
        
        if not paused:
            dt = clock.tick(FPS) / 1000
            
            for updatable in updatable_group:
                updatable.update(dt)
            
            for asteroid in asteroid_group:
                if player.collission_check(asteroid):
                    pygame.quit()
                    return
                for shot in shots_group:
                    if shot.collission_check(asteroid):
                        new_asteroids = asteroid.split()
                        if new_asteroids:
                            for asteroid_data in new_asteroids:
                                asteroid_field.spawn(*asteroid_data)
                        shot.kill()
                        break
        else:
            clock.tick(FPS)
        draw()
    

        
    
    
if __name__ == "__main__":
    main()