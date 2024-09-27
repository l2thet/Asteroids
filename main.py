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
    pygame.joystick.init()
    
    flags = pygame.SCALED
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    
    def draw():
        window_surface.fill((0, 0, 0))
        
        for drawable in drawable_group:
            drawable.draw(window_surface)
                
        # Render "Score:" text in bold white
        score_text = font.render('Survived:', True, (255, 255, 255))  # White color
        score_text_width = score_text.get_width()
        
        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
        elapsed_time_text = f'{elapsed_time}'
        
        # Render elapsed time in red
        elapsed_time_text = font.render(f'{elapsed_time}', True, (255, 255, 255))  # Red color
        
        # Calculate positions
        surface_width = window_surface.get_width()
        x_score = surface_width - score_text_width - elapsed_time_text.get_width() - 10  # 10 pixels padding from the right edge
        x_time = x_score + score_text_width
        y = 10  # 10 pixels padding from the top edge
            
        # Blit texts to the screen
        window_surface.blit(score_text, (x_score, y))
        window_surface.blit(elapsed_time_text, (x_time, y))
            
        pygame.display.flip()
    
    
    clock = pygame.time.Clock()
    dt = 0
    
    updatable_group = pygame.sprite.Group()
    drawable_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()
    ui_group = pygame.sprite.Group()
    
    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group, drawable_group, shots_group)
    UI.containers = (updatable_group, drawable_group, ui_group)
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()
    
    # Create a font object
    font = pygame.font.Font(None, 36)# None for default font, 36 for font size
    
    # Initialize start time
    start_time = pygame.time.get_ticks()
    
    # Initialize paused state
    paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle paused state

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