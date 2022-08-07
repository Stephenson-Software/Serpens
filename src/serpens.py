import pygame
from config import Config
from environment import Environment
from graphik import Graphik
from snakePart import SnakePart


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
        self.environment = Environment("Serpens", self.config.gridSize)
        self.initializeLocationWidthAndHeight()

    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN)
        else:
            self.gameDisplay = pygame.display.set_mode((self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE)

    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x/self.environment.getGrid().getRows()
        self.locationHeight = y/self.environment.getGrid().getColumns()

    # Draws the environment in its entirety.
    def drawEnvironment(self):
        for location in self.environment.getGrid().getLocations():
            self.drawLocation(location, location.getX() * self.locationWidth, location.getY() * self.locationHeight, self.locationWidth, self.locationHeight)

    # Returns the color that a location should be displayed as.
    def getColorOfLocation(self, location):
        if location == -1:
            color = self.config.white
        else:
            color = self.config.white
            if location.getNumEntities() > 0:
                color = self.config.black
        return color

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)

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
        self.environment.addEntity(SnakePart())
        self.environment.printInfo()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)

            self.drawEnvironment()
            pygame.display.update()

serpens = Serpens()
serpens.run()