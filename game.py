import pygame
from os import path
from player import Player
from enemies import Enemies

# Frozen Jam от tgfcoder <https://twitter.com/tgfcoder>
# под лицензией CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
img_dir = path.join(path.dirname(__file__), "images")
snd_dir = path.join(path.dirname(__file__), "sounds")
WIDTH = 600
HEIGHT = 750
FPS = 60
# set color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

flags = pygame.SHOWN
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=flags)
pygame.display.set_caption("Space adventures")
pygame.display.set_icon(pygame.image.load(path.join(img_dir, "joy.png")))
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1)

font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newenemies():
    e = Enemies(HEIGHT, enemies_img)
    all_sprites.add(e)
    enemies.add(e)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


background = pygame.image.load(path.join(img_dir, "back2.jpg")).convert_alpha()
background_rect = background.get_rect()
background_rect.x = 1
player_img = pygame.image.load(path.join(img_dir, "spa2.png")).convert()
enemies_img = pygame.image.load(path.join(img_dir, "enemy.jpg")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserGreen10.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
expl_sound = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.play(loops=-1)
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(BLACK, WIDTH, HEIGHT, player_img, all_sprites, shoot_sound, bullets, Bullet)
all_sprites.add(player)
for i in range(12):
    newenemies()

score = 0

checkpoint = True
while checkpoint:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            checkpoint = False
    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        expl_sound.play().set_volume(0.2)
        score += 50
        newenemies()

    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        newenemies()
        if player.shield <= 0:
            checkpoint = False

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH // 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.update()

pygame.quit()
