from typing import List, Union

from pygame import Surface
from pygame.surface import SurfaceType

from shot import Shot
import pygame
from invader import Invader
from spaceship import Spaceship

import random

LINE_COLOR = (100, 100, 100)
TEXT_COLOR = (250, 250, 250)
YOUWIN_COLOR = (0, 250, 0)
GAMEOVER_COLOR = (250, 0, 0)


class Game:
    window: Union[Surface, SurfaceType]
    invaders: List[Invader]
    player: Spaceship
    shots: List[Shot]

    def __init__(self, diff=1):
        pygame.init()
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font.ttf", 80)
        self.smallfont = pygame.font.Font("font.ttf", 40)
        self.is_game_won = False
        self.is_game_over = False
        self.margin = 50
        self.difficulty = diff
        self.played = False

    def start(self):
        self.player = Spaceship(self.window.get_width() / 2 - 50, self.window.get_height() - 150, self)
        self.invaders = []
        self.shots = []

        if not self.played:
            self.draw_text("Press any key to start", self.smallfont)
            pygame.display.flip()
            start = False
            while not start:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        start = True
            self.draw_text("Press any key to start", self.smallfont, (0, 0, 0))
            pygame.display.flip()

        rows = random.randint(3, 4)
        for r in range(rows):
            for c in range(random.randint(10, 20)):
                self.invaders.append(Invader(50 + c * 60, 50 + r * 60, self, 3 - r))
        self.is_game_won = False
        self.is_game_over = False

    def loop(self):
        self.played = True
        run = True
        while run:
            # 1. EVENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_RETURN:
                        self.start()
                    else:
                        if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                            self.player.shoot(self)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.player.speed = -self.player.max_speed
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.player.speed = self.player.max_speed
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                            event.key == pygame.K_a or event.key == pygame.K_d:
                        self.player.speed = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shoot(self)
            # 2. UPDATE
            if not (self.is_game_won or self.is_game_over):
                self.player.update()
                for invader in self.invaders:
                    invader.collide(self)
                for invader in self.invaders:
                    invader.update()
                for shot in self.shots:
                    shot.move()
                    shot.collide(self)
                if len(self.invaders) == 0:
                    self.game_won()
            # 3. DRAW
            self.window.fill((0, 0, 0))
            pygame.draw.line(self.window, LINE_COLOR, (0, self.window.get_height() - 200),
                             (self.window.get_width(), self.window.get_height() - 200))
            self.player.draw(self.window)
            for invader in self.invaders:
                invader.draw(self.window)
            for shot in self.shots:
                shot.draw(self.window)
            if self.is_game_won:
                self.draw_text("YOU WIN!", self.font, YOUWIN_COLOR)
                self.draw_down_text("Press esc to exit, press enter to restart", self.smallfont)
            if self.is_game_over:
                self.draw_text("GAME OVER", self.font, GAMEOVER_COLOR)
                self.draw_down_text("Press esc to exit, press enter to restart", self.smallfont)
            pygame.display.flip()
            # 4. WAIT
            self.clock.tick(60)

    def game_won(self):
        self.is_game_won = True

    def game_over(self):
        self.is_game_over = True

    def draw_text(self, text, font: pygame.font.Font, color=TEXT_COLOR, ):
        render = font.render(text, True, color)
        self.window.blit(render, (
            self.window.get_width() // 2 - render.get_width() // 2,
            self.window.get_height() // 2 - render.get_height() // 2
        ))

    def draw_down_text(self, text, font: pygame.font.Font, color=TEXT_COLOR, ):
        render = font.render(text, True, color)
        self.window.blit(render, (
            self.window.get_width() // 2 - render.get_width() // 2,
            self.window.get_height() // 2 - render.get_height() // 2 + 60
        ))


difficulty: int = int(input("Enter Difficulty: ")) + 1
# difficulty = 1

my_game = Game(difficulty)
my_game.start()
my_game.loop()
