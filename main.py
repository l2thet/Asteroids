import pygame
from constants import *
from minorbuff import MinorBuff
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
    
    menu_items = ['Resume', 'Options', 'Quit']
    ui = UI(menu_items)
    updatable_group.add(ui)
    drawable_group.add(ui)

    Player.containers = (updatable_group, drawable_group)
    Asteroid.containers = (updatable_group, drawable_group, asteroid_group)
    AsteroidField.containers = (updatable_group)
    Shot.containers = (updatable_group, drawable_group, shots_group)
    UI.containers = (updatable_group, drawable_group)
    MinorBuff.containers = (updatable_group, drawable_group)
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    player.toggle_pause()
                if player.paused:
                    if event.key == pygame.K_UP:
                        ui.navigate(-1)
                    elif event.key == pygame.K_DOWN:
                        ui.navigate(1)
                    elif event.key == pygame.K_RETURN:
                        if ui.selected_index == 0:
                            player.toggle_pause()
                        elif ui.selected_index == 2:
                            pygame.quit()
                            return
                            
        player.handle_pause_input()

        UI.paused = player.paused
        
        if player.paused:
            ui.draw(window_surface)
            pygame.display.flip()
        else:
            dt = clock.tick(FPS) / 1000
            
            for updatable in updatable_group:
                updatable.update(dt)
            
            for asteroid in asteroid_group:
                if not player.invulnerable and player.collission_check(asteroid):
                    pygame.quit()
                    return
                for shot in shots_group:
                    if shot.collission_check(asteroid):
                        new_objects = asteroid.split()
                        if new_objects:
                            for obj in new_objects:
                                if isinstance(obj, MinorBuff):
                                    updatable_group.add(obj)
                                    drawable_group.add(obj)
                                else:
                                    asteroid_field.spawn(*obj)
                        shot.kill()
                        break
                for i, offset in enumerate(player.circles):
                    circle_position = player.position + offset
                    if circle_position.distance_to(asteroid.position) < player.radius + asteroid.radius:
                        if i == 0:
                            print("Game Over!")
                            pygame.quit()
                            return
                        else:
                            player.circles.pop(i)
                            break
            
            # Check for collisions between player and MinorBuff objects
            for minor_buff in updatable_group:
                if isinstance(minor_buff, MinorBuff) and player.collission_check(minor_buff):
                    player.collect_minor_buff()
                    minor_buff.kill()                  
            draw()
    

        
    
    
if __name__ == "__main__":
    main()