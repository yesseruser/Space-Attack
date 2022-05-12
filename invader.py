import pygame
from shot import InvaderShot
import random


class Invader:
    direction = 1
    margin = 50

    def __init__(self, x, y, game, lives):
        self.x = x
        self.y = y
        self.speed = 2
        self.lives = lives
        if lives == 4:
            lives = 3
        if lives <= 0:
            lives = 1
        if lives == 1:
            # self.img = (200, 150, 0)
            self.img = pygame.image.load("img/invader.png")
        elif lives == 2:
            # self.img = (0, 150, 200)
            self.img = pygame.image.load("img/invader2.png")
        elif lives == 3:
            # self.img = (200, 0, 150)
            self.img = pygame.image.load("img/invader3.png")
        self.game = game
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        Invader.timer = random.uniform(100, 500)

    def collide(self, game):
        if self.x < Invader.margin:
            Invader.direction = 1
            for invader in game.invaders:
                invader.y += 20
        if self.x > game.window.get_width() - Invader.margin - self.width:
            Invader.direction = -1
            for invader in game.invaders:
                invader.y += 20
        if self.y + self.height >= game.player.y:
            game.game_over()

    def destroy(self):
        self.game.invaders.remove(self)

    def update(self):
        self.x += Invader.direction * self.speed * self.game.difficulty
        Invader.timer -= random.uniform(0.5, 3)
        self.reset_timer()
        if Invader.timer <= 0:
            self.shoot()
            Invader.timer = random.uniform(1000, 5000)

    def shoot(self):
        shot = InvaderShot(self.x + self.width / 2, self.y + self.height, self.game)
        self.game.shots.append(shot)

    def draw(self, window: pygame.Surface):
        # pygame.draw.rect(window, self.img, (self.x, self.y, self.width, self.height))
        window.blit(self.img, (self.x, self.y))

    @staticmethod
    def reset_timer():
        if random.randint(1, 3000) == 5:
            Invader.timer = random.uniform(1000, 5000)
