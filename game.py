import pygame
import random
from os import path

# Frozen Jam от tgfcoder <https://twitter.com/tgfcoder>
# под лицензией CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
img_dir = path.join(path.dirname(__file__), "images")
snd_dir = path.join(path.dirname(__file__), "sounds")
WIDTH = 600
HEIGHT = 750
FPS = 60
# Задаем цвета
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
    e = Enemies()
    all_sprites.add(e)
    enemies.add(e)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 40
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 150
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        key = pygame.key.get_pressed()
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            self.shoots()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.speedx = -9
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.speedx = +9
        if key[pygame.K_SPACE]:
            self.shoots()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoots(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play().set_volume(0.15)


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemies_img
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
player = Player()
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
