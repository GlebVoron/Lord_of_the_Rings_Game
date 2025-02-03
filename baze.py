import pygame
import random
import time
import os
import sys

pygame.init()
clock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 8

all_sprites = pygame.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join('sprite', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
