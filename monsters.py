#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import baze
import os

MONSTER_COLOR = "#2110FF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_MONSTERHORYSONTAL = [('%s/monsters/fire1.png' % ICON_DIR),
                               ('%s/monsters/fire2.png' % ICON_DIR)]
ANIMATION_MONSTERHORYSONTAL1 = [('%s/monsters/Orc1.png' % ICON_DIR),
                                ('%s/monsters/Orc2.png' % ICON_DIR)]
ANIMATION_MONSTERHORYSONTAL2 = [('%s/monsters/Sauron1.png' % ICON_DIR),
                                ('%s/monsters/Sauron2.png' % ICON_DIR)]


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, p):
        if p == 1:
            self.flag = True
            MONSTER_HEIGHT = 32
            MONSTER_WIDTH = 32
            A = ANIMATION_MONSTERHORYSONTAL
        elif p == 2:
            self.flag = False
            MONSTER_WIDTH = 50
            MONSTER_HEIGHT = 70
            A = ANIMATION_MONSTERHORYSONTAL2
        else:
            self.flag = True
            MONSTER_WIDTH = 35
            MONSTER_HEIGHT = 40
            A = ANIMATION_MONSTERHORYSONTAL1
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        if self.flag:
            for anim in A:
                boltAnim.append((anim, 0.3))
            self.boltAnim = baze.PygAnimation(boltAnim)
            self.boltAnim.play()
        else:
            for anim in A:
                boltAnim.append((anim, 0.3))
            self.boltAnim = baze.PygAnimation(boltAnim)
            self.boltAnim.play()

    def update(self, platforms):  # по принципу героя
        global ANIMATION_MONSTERHORYSONTAL
        global ANIMATION_MONSTERHORYSONTAL1
        global A
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
            A = ANIMATION_MONSTERHORYSONTAL1
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль
            A = ANIMATION_MONSTERHORYSONTAL

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel
