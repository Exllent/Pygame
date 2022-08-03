import pygame
from images import Images
from params import BLACK


class Bullet(pygame.sprite.Sprite, Images):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
