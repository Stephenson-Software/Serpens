import pygame
from config import Config
from graphik import Graphik


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Serpens:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Serpens")
        self.config = Config()
        self.initializeGameDisplay()
        self.graphik = Graphik(self.gameDisplay)
        self.running = True

    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    def quitApplication(self):
        pygame.quit()
        quit()
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_q:
            self.quitApplication()
        elif key == pygame.K_d:
            if self.config.debug == True:
                self.config.debug = False
            else:
                self.config.debug = True
        elif key == pygame.K_F11:
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            self.initializeGameDisplay()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)

serpens = Serpens()
serpens.run()