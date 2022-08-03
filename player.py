import pygame
from params import *
from images import Images
from bullet import Bullet
from sounds import shoot_sound


class Player(pygame.sprite.Sprite, Images):
    def __init__(self, all_sprites, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.shoot_sound = shoot_sound
        self.bullets = bullets
        self.speed_x = None
        self.shield = 100
        self.image = self.player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 150
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        key = pygame.key.get_pressed()
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            self.shoots()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.speed_x = -9
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.speed_x = +9
        if key[pygame.K_SPACE]:
            self.shoots()
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoots(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.shoot_sound.play().set_volume(0.15)
