import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    rotation = 0
    shot_cooldown = 0
    joystick = None
    paused = False
    pause_button_pressed = False
    invulnerable = False
    invulnerable_time = INVULENERABILITY_TIME
    invulnerability_cooldown = 0
    minor_buffs_obtained = 1

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.joystick = None

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
          
    def draw(self, screen):
        color = (255, 0, 0) if not self.invulnerable else (255, 255, 0)

        pygame.draw.circle(screen, color, self.position, self.radius, 2)
        
        direction_length = self.radius * 1.5
        direction_end = self.position + pygame.Vector2(0, -direction_length).rotate(self.rotation)
        pygame.draw.line(screen, color, self.position, direction_end, 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_a]:
            self.move_x(-dt)
        if keys[pygame.K_d]:
            self.move_x(dt)
        if keys[pygame.K_w]:
            self.move_y(-dt)
        if keys[pygame.K_s]:
            self.move_y(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_LSHIFT] and self.invulnerability_cooldown <= 0:
            self.activate_invulnerability()
        
        # Handle joystick input
        if self.joystick:
            x_axis = self.joystick.get_axis(0)
            y_axis = self.joystick.get_axis(1)
            x_axis_2 = self.joystick.get_axis(2)
            y_axis_2 = self.joystick.get_axis(3)
            
            # Apply dead zone threshold
            if abs(x_axis) < CONTROLLER_DEAD_ZONE:
                x_axis = 0
            if abs(y_axis) < CONTROLLER_DEAD_ZONE:
                y_axis = 0

            if abs(x_axis_2) < CONTROLLER_DEAD_ZONE:
                x_axis_2 = 0
            if abs(y_axis_2) < CONTROLLER_DEAD_ZONE:
                y_axis_2 = 0
            
            #move based on joystick input
            self.move_y(y_axis * dt)
            self.move_x(x_axis * dt)

            if x_axis_2 != 0 or y_axis_2 != 0:
                self.rotation = pygame.math.Vector2(x_axis_2, -y_axis_2).angle_to(pygame.math.Vector2(0, 1))
                self.shot_cooldown -= dt
                self.shoot()

            if self.joystick.get_button(5) and self.invulnerability_cooldown <= 0:
                self.activate_invulnerability()
                
        if self.invulnerable:
            self.invulnerable_time -= dt
            if self.invulnerable_time <= 0:
                self.invulnerable = False
                self.speed_boost = 1.0

        if self.invulnerability_cooldown > 0:
            self.invulnerability_cooldown -= dt

        self.shot_cooldown -= dt

        # Ensure the player stays within the viewable area
        self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.position.y))
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.invulnerable:
            self.position += forward * (PLAYER_SPEED * PLAYER_SPEED_BOOST) * dt
        else:        
            self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.shot_cooldown <= 0:
            # Calculate the front vertex of the triangle
            forward = pygame.Vector2(0, -1).rotate(self.rotation)
            shot_position = self.position + forward * self.radius
            shot_velocity = forward * SHOT_SPEED
            Shot(shot_position.x, shot_position.y, shot_velocity, SHOT_RADIUS * self.minor_buffs_obtained)
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN

    def handle_pause_input(self):
        if self.joystick:
            if self.joystick.get_button(7):
                if not self.pause_button_pressed:
                    self.toggle_pause()
                    self.pause_button_pressed = True
            else:
                self.pause_button_pressed = False

    def toggle_pause(self):
        self.paused = not self.paused

    def activate_invulnerability(self):
        self.invulnerable = True
        self.invulnerable_time = INVULENERABILITY_TIME
        self.invulnerability_cooldown = INVULENERABILITY_COOLDOWN

    def move_y(self, dt):
        if self.invulnerable:
            self.position.y += PLAYER_SPEED * dt * PLAYER_SPEED_BOOST
        else:
            self.position.y += PLAYER_SPEED * dt
    
    def move_x(self, dt):
        if self.invulnerable:
            self.position.x += PLAYER_SPEED * dt * PLAYER_SPEED_BOOST
        else:
            self.position.x += PLAYER_SPEED * dt

    def rotate(self, dt):
        self.rotation = PLAYER_TURN_SPEED * dt

    def collect_minor_buff(self):
        self.minor_buffs_obtained += 1