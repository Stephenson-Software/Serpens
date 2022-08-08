import random
import time
import pygame
from config import Config
from entity import Entity
from environment import Environment
from food import Food
from graphik import Graphik
from grid import Grid
from location import Location
from snakePart import SnakePart


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Ophidian:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ophidian")
        self.config = Config()
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load('src/icon.PNG'))
        self.graphik = Graphik(self.gameDisplay)
        self.running = True
        self.environment = Environment("Ophidian", self.config.gridSize)
        self.initializeLocationWidthAndHeight()
        self.snakeParts = []
        self.initialize()
        self.tick = 0
        
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
                topEntity = location.getEntities()[-1]
                return topEntity.getColor()
        return color

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)
    
    def restartApplication(self):
        self.__init__()

    def quitApplication(self):
        print("Length of snake:", len(self.snakeParts))
        pygame.quit()
        quit()
    
    def getLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid.getLocation(locationID)

    def getLocationAndGrid(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid, grid.getLocation(locationID)

    def moveEntity(self, entity: Entity, direction):
        grid, location = self.getLocationAndGrid(entity)

        newLocation = -1
        # get new location
        if direction == 0:
            newLocation = grid.getUp(location)
        elif direction == 1:
            newLocation = grid.getLeft(location)
        elif direction == 2:
            newLocation = grid.getDown(location)
        elif direction == 3:
            newLocation = grid.getRight(location)
    
        if newLocation == -1:
            # location doesn't exist, we're at a border
            return

        # if new location has a snake part already
        for e in newLocation.getEntities():
            if type(e) is SnakePart:
                # we have a collision
                print("The ophidian collides with itself and ceases to be.")
                time.sleep(1)
                if self.config.restartUponCollision:
                    self.restartApplication()
                else:
                    self.running = False
        
        # move entity
        location.removeEntity(entity)
        newLocation.addEntity(entity)
        entity.lastPosition = location

        # move all attached snake parts
        if entity.hasPrevious():
            self.movePreviousSnakePart(entity)        
        
        if self.config.debug:
            print("[EVENT] ", entity.getName(), "moved to (", location.getX(), ",", location.getY(), ")")
        
        food = -1
        # check for food
        for e in newLocation.getEntities():
            if type(e) is Food:
                food = e
        
        if food == -1:
            return

        foodColor = food.getColor()

        self.removeEntity(food)
        self.spawnFood()
        self.spawnSnakePart(entity.getTail(), foodColor)
    
    def movePreviousSnakePart(self, snakePart):
        previousSnakePart = snakePart.previousSnakePart

        previousSnakePartLocation = self.getLocation(previousSnakePart)

        if previousSnakePartLocation == -1:
            print("Error: A previous snake part's location was unexpectantly -1.")
            time.sleep(1)
            self.quitApplication()
        
        targetLocation = snakePart.lastPosition
        
        # move entity
        previousSnakePartLocation.removeEntity(previousSnakePart)
        targetLocation.addEntity(previousSnakePart)
        previousSnakePart.lastPosition = previousSnakePartLocation

        if previousSnakePart.hasPrevious():
            self.movePreviousSnakePart(previousSnakePart)
    
    def removeEntityFromLocation(self, entity: Entity):
        location = self.getLocation(entity)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def removeEntity(self, entity: Entity):
        self.removeEntityFromLocation(entity)
    
    def handleKeyDownEvent(self, key):
        if key == pygame.K_q:
            self.running = False
        elif key == pygame.K_w or key == pygame.K_UP:
            if self.selectedSnakePart.getDirection() != 2:
                self.selectedSnakePart.setDirection(0)
        elif key == pygame.K_a or key == pygame.K_LEFT:
            if self.selectedSnakePart.getDirection() != 3:
                self.selectedSnakePart.setDirection(1)
        elif key == pygame.K_s or key == pygame.K_DOWN:
            if self.selectedSnakePart.getDirection() != 0:
                self.selectedSnakePart.setDirection(2)
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            if self.selectedSnakePart.getDirection() != 1:
                self.selectedSnakePart.setDirection(3)
        elif key == pygame.K_F11:
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            self.initializeGameDisplay()
        elif key == pygame.K_l:
            if self.config.limitTickSpeed:
                self.config.limitTickSpeed = False
            else:
                self.config.limitTickSpeed = True

    def getRandomDirection(self, grid: Grid, location: Location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)
    
    def getLocationDirection(self, direction, grid, location):
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getLeft(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getRight(location)
    
    def getLocationOppositeDirection(self, direction, grid, location):
        if direction == 0:
            return grid.getDown(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getUp(location)
        elif direction == 3:
            return grid.getLeft(location)
        
    def spawnSnakePart(self, snakePart: SnakePart, color):
        newSnakePart = SnakePart(color)
        snakePart.setPrevious(newSnakePart)
        newSnakePart.setNext(snakePart)
        grid, location = self.getLocationAndGrid(snakePart)
        
        targetLocation = -1
        while True:
            targetLocation = self.getRandomDirection(grid, location)
            if targetLocation != -1 and targetLocation != self.getLocationDirection(snakePart.getDirection(), grid, location):
                break;

        self.environment.addEntityToLocation(newSnakePart, targetLocation)
        self.snakeParts.append(newSnakePart)
        print("The ophidian grows.")
    
    def spawnFood(self):
        food = Food((random.randrange(50, 200), random.randrange(50, 200), random.randrange(50, 200)))
        
        # get target location
        targetLocation = -1
        notFound = True
        while notFound:
            targetLocation = self.environment.getGrid().getRandomLocation()
            if targetLocation.getNumEntities() == 0:
                notFound = False
        
        self.environment.addEntity(food)
    
    def initialize(self):
        self.selectedSnakePart = SnakePart((random.randrange(50, 200), random.randrange(50, 200), random.randrange(50, 200)))
        self.environment.addEntity(self.selectedSnakePart)
        self.snakeParts.append(self.selectedSnakePart)
        print("The ophidian enters the world.")
        self.spawnFood()
        self.environment.printInfo()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyDownEvent(event.key)
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()
            
            if self.selectedSnakePart.getDirection() == 0:
                self.moveEntity(self.selectedSnakePart, 0)
            elif self.selectedSnakePart.getDirection() == 1:
                self.moveEntity(self.selectedSnakePart, 1)
            elif self.selectedSnakePart.getDirection() == 2:
                self.moveEntity(self.selectedSnakePart, 2)
            elif self.selectedSnakePart.getDirection() == 3:
                self.moveEntity(self.selectedSnakePart, 3)

            self.gameDisplay.fill(self.config.white)
            self.drawEnvironment()
            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
        
        self.quitApplication()

ophidian = Ophidian()
ophidian.run()