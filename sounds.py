import pygame
from os import path

snd_dir = path.join(path.dirname(__file__), "sounds")
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
expl_sound = pygame.mixer.Sound(path.join(snd_dir, "expl6.wav"))
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.play(loops=-1)
