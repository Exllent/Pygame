import pygame
from player import Player


class Sprites:
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player(all_sprites, bullets)
    all_sprites.add(player)
