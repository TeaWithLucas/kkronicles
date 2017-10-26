import pygame
import random

class Main_Game():
    def ___init__(self, width, height):
        self.window = pygame.display.set_mode((width, height))
        self.running = True


    def game_run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

my_game = Main_Game(600,800)
my_game.game_run()
