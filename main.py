import pygame
import sys
import time
from settings import *
from sprites import Player, Pipes, Background, Ground


class Game:
    # setup
    def __init__(self):
        pygame.init()
        # window
        self.game_surface = pygame.display.set_mode(
            (window_width, window_height))
        pygame.display.set_caption('Bird Game')
        self.clock = pygame.time.Clock()
        self.active = True

        # groups for sprites
        self.game_sprites = pygame.sprite.Group()
        self.colliders_sprites = pygame.sprite.Group()

        # adding sprites
        Background(self.game_sprites)
        Ground([self.game_sprites, self.colliders_sprites])
        self.player = Player(self.game_sprites)

        # timer
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, 1000)

        # text
        self.font = pygame.font.Font(None, 30)
        self.score = 0
        self.start_offset = 0
        # menu
        self.menu_surf = pygame.image.load(
            'graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(
            center=(window_width/2, window_height/2))

        # music
        self.music = pygame.mixer.Sound('music/BG.wav')
        self.die = pygame.mixer.Sound('music/die.wav')
        self.music.play(loops=-1)

    def colliders(self):
        if pygame.sprite.spritecollide(self.player, self.colliders_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top <= 0:
            for sprite in self.colliders_sprites.sprites():
                if sprite.sprite_type == 'pipe':
                    sprite.kill()
            self.active = False
            self.player.kill()
            self.die.play()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = window_height/10
        else:
            y = window_height/2 + (self.menu_rect.height/1.5)
        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(window_width/2, y))
        self.game_surface.blit(score_surf, score_rect)

    def run(self):
        saved_time = time.time()
        while True:

            # delta time
            delta_time = time.time() - saved_time
            saved_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.active:
                        self.player.jumping()
                    else:
                        self.player = Player(
                            self.game_sprites)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.pipe_timer and self.active == True:
                    Pipes([self.game_sprites, self.colliders_sprites])

            # game logic
            self.game_surface.fill('black')
            self.game_sprites.update(delta_time)
            self.game_sprites.draw(self.game_surface)
            self.display_score()
            if self.active:
                self.colliders()
            else:
                self.game_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
