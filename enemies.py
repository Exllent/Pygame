import pygame
import random


class Enemies(pygame.sprite.Sprite):
    def __init__(self, HEIGHT, enemies_img):
        pygame.sprite.Sprite.__init__(self)
        self.HEIGHT = HEIGHT
        self.image = enemies_img
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(random.randint(50, 550), 0))
        self.rect.y = random.randrange(-100, 40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > self.HEIGHT:
            self.rect.x = random.randrange(50, 550)
            self.rect.y = random.randrange(1, 4)
