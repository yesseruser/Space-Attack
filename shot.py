import pygame.draw
import random
from typing import Union
from pygame import Surface
from pygame.surface import SurfaceType


class Shot:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.speed = 8
        self.game = game
        self.max_offset = 1
        self.offset = random.uniform(-self.max_offset, self.max_offset)
        self.image = pygame.image.load("img/shot.png")

    def move(self):
        self.y -= self.speed
        self.x += self.offset
        if self.y < 0:
            self.destroy()

    def collide(self, game):
        for invader in game.invaders:
            if invader.x < self.x < invader.x + invader.width:
                if invader.y < self.y < invader.y + invader.height:
                    invader.lives -= 1
                    if invader.lives == 1:
                        invader.img = pygame.image.load("img/invader.png")
                    elif invader.lives == 2:
                        invader.img = pygame.image.load("img/invader2.png")
                    elif invader.lives <= 0:
                        invader.destroy()
                    self.destroy()

    def destroy(self):
        self.game.shots.remove(self)

    def draw(self, window: Union[Surface, SurfaceType]):
        # pygame.draw.circle(window, self.color, (self.x, self.y), 5)
        window.blit(self.image, (self.x, self.y))


class InvaderShot(Shot):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.speed = 8
        self.game = game
        self.offset = None
        self.max_offset = None
        self.image = pygame.image.load("img/invadershot.png")

    def move(self):
        self.y += self.speed
        if self.y > self.game.window.get_height():
            self.destroy()

    def collide(self, game):
        player = game.player
        if player.y < self.y < player.y + player.height:
            if player.x < self.x < player.x + player.width:
                player.lose_life()
                self.destroy()
