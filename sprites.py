import pygame
from settings import *
from random import choice, randint


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.frames_imported()
        self.index_frame = 0
        self.image = self.frames[self.index_frame]

        # position
        self.rect = self.image.get_rect(
            midleft=(window_width/20, window_height/2))
        self.position = pygame.math.Vector2(self.rect.topleft)

        # phisic
        self.gravity = 1000
        self.direction = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # sound
        self.wing_sound = pygame.mixer.Sound('music/wing.wav')
        self.wing_sound.set_volume(0.3)

    def frames_imported(self):
        self.frames = []
        for i in range(3):
            player_surf = pygame.image.load(
                f'graphics/bird/{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(
                player_surf, pygame.math.Vector2(player_surf.get_size()))
            self.frames.append(scaled_surface)

    def animation(self, delta_time):
        self.index_frame += 10 * delta_time
        if self.index_frame >= len(self.frames):
            self.index_frame = 0
        self.image = self.frames[int(self.index_frame)]

    def real_gravity(self, delta_time):
        self.direction += self.gravity * delta_time
        self.position.y += self.direction * delta_time
        self.rect.y = round(self.position.y)

    def jumping(self):
        self.wing_sound.play()
        self.direction = -400

    def rotation(self):
        rotated_player = pygame.transform.rotozoom(
            self.image, -self.direction * 0.06, 1)
        self.image = rotated_player
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.real_gravity(delta_time)
        self.animation(delta_time)
        self.rotation()


class Pipes(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.sprite_type = 'pipe'
        pipe_surf = pygame.image.load(
            f'graphics/obstacle/2.png').convert_alpha()
        self.image = pygame.transform.scale(
            pipe_surf, pygame.math.Vector2(pipe_surf.get_size()))

        x = window_width + randint(40, 100)
        y = window_height + randint(1, 300)
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.position = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.position.x -= 400*delta_time
        self.rect.x = round(self.position.x)
        if self.rect.right <= -100:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/background.png').convert()
        # position
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.position = pygame.math.Vector2(self.rect.topleft)

    def update(self, delta_time):
        self.position.x -= 250 * delta_time
        if self.rect.centerx <= 0:
            self.position.x = 0
        self.rect.x = round(self.position.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.sprite_type = 'ground'
        self.image = pygame.image.load('graphics/ground.png').convert_alpha()
        # position
        self.rect = self.image.get_rect(bottomleft=(0, 850))
        self.position = pygame.math.Vector2(self.rect.bottomleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.position.x -= 360 * delta_time
        if self.rect.centerx <= 0:
            self.position.x = 0
        self.rect.x = round(self.position.x)
