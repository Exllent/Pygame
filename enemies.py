import pygame
import random
from params import HEIGHT
from images import Images
from sprites import Sprites


class Enemies(pygame.sprite.Sprite, Images):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.HEIGHT = HEIGHT
        self.image = self.enemies_img
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(random.randint(50, 550), 0))
        self.rect.y = random.randrange(-100, 40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(50, 550)
            self.rect.y = random.randrange(1, 4)

    @staticmethod
    def spawnmobs():
        e = Enemies()
        Sprites.all_sprites.add(e)
        Sprites.enemies.add(e)

# def newenemies():



x = [Enemies.spawnmobs() for i in range(12)]

#
# for i in range(12):
#     newenemies()
