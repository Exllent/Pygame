import pygame
from os import path

WIDTH = 600
HEIGHT = 750


class Images:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    img_dir = path.join(path.dirname(__file__), "images")
    background = pygame.image.load(path.join(img_dir, "back2.jpg")).convert_alpha()
    background_rect = background.get_rect()
    enemies_img = pygame.image.load(path.join(img_dir, "enemy.jpg")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "laserGreen10.png")).convert()
    pygame.display.set_caption("Space adventures")
    pygame.display.set_icon(pygame.image.load(path.join(img_dir, "joy.png")))
    player_img = pygame.image.load(path.join(img_dir, "spa2.png")).convert()
