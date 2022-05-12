import pygame
import random

from shot import Shot


class Spaceship:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.speed = 0
        self.max_speed = 12
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load("img/spaceship.png"),
                                            (self.width, self.height))
        self.max_charge = 100
        self.charge = self.max_charge
        self.color_charge = (255, 255, 0)
        self.full_charge_color = (0, 255, 0)
        self.lives = random.randint(3, 5)
        self.life_image = pygame.image.load("img/heart.png")
        self.life_heigth = self.life_image.get_height()
        self.life_width = self.life_image.get_width()

    def update(self):
        self.x += self.speed
        if self.x < 0:
            self.x = 0
        if self.x > self.game.window.get_width() - self.width:
            self.x = self.game.window.get_width() - self.width
        if self.x > self.game.window.get_width() - self.width - self.game.margin:
            self.x = self.game.window.get_width() - self.width - self.game.margin
        if self.x < 0 + self.game.margin:
            self.x = 0 + self.game.margin

        self.charge += 8 * (self.game.difficulty / 3)
        if self.charge > self.max_charge:
            self.charge = self.max_charge

    def shoot(self, game):
        if self.charge == self.max_charge:
            shot = Shot(self.x + self.width / 2, self.y, game)
            game.shots.append(shot)
            self.charge = 0

    def draw(self, window: pygame.Surface):
        window.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(window, (0, 250, 0), (self.x, self.y, self.width, self.height))
        if self.charge < self.max_charge:
            pygame.draw.rect(window, self.color_charge, (self.x, self.y + self.width + 5, self.charge, 10))
        else:
            pygame.draw.rect(window, self.full_charge_color, (self.x, self.y + self.width + 5, self.charge, 10))

        for i in range(self.lives):
            window.blit(self.life_image, (self.life_width * i, self.life_heigth))

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game.game_over()