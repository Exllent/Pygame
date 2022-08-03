from images import Images
from sounds import *
import pygame
from params import *
from points import draw_text
from health import draw_health_bar
from sprites import Sprites
from enemies import Enemies

# Frozen Jam от tgfcoder <https://twitter.com/tgfcoder>
# под лицензией CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1)

score = 0
checkpoint = True
while checkpoint:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checkpoint = False
    Sprites.all_sprites.update()

    hits = pygame.sprite.groupcollide(Sprites.enemies, Sprites.bullets, True, True)
    for hit in hits:
        expl_sound.play().set_volume(0.2)
        score += 50
        Enemies.spawnmobs()

    hits = pygame.sprite.spritecollide(Sprites.player, Sprites.enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        Sprites.player.shield -= 10
        Enemies.spawnmobs()
        if Sprites.player.shield <= 0:
            checkpoint = False

    Images.screen.blit(Images.background, Images.background_rect)
    Sprites.all_sprites.draw(Images.screen)
    draw_text(Images.screen, str(score), 18, WIDTH // 2, 10)
    draw_health_bar(Images.screen, 5, 5, Sprites.player.shield)
    pygame.display.update()

pygame.quit()
