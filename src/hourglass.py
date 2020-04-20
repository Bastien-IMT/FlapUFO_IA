from random import randint, choice

from src.data import *
from src.gameobject import GameObject


class Hourglass(GameObject):
    """
    Class that defines the hourglass that reduce pipes and background speed if it's taken by ship.
    """

    origin_x_velocity = 7.5
    direction = [-1, 1]
    origin_y_velocity = 1 * choice(direction)

    def __init__(self, screen: pygame.Surface):
        """
        Initialize Hourglass object.
        :param screen: surface to display hourglass on
        """

        # Display settings
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_rect().size
        self.image = images["clock"]
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size

        # Position settings
        self.up_pos_max = 30
        self.low_pos_max = self.screenHeight - (30 + self.height)
        self.start_point = self.screenWidth + self.width + images["pipe_down1"].get_rect().size[0]
        self.x_pos = self.start_point
        self.y_pos = randint(self.up_pos_max, self.low_pos_max)
        self.x_velocity = self.origin_x_velocity
        self.y_velocity = self.origin_y_velocity

        # internal settings to make it run
        self.appears = False

    def move(self):
        """
        Make Hourglass move.
        """
        if self.appears:
            self.x_pos -= self.x_velocity
            self.y_pos -= self.y_velocity
            if self.x_pos < -self.width:
                self.updateCoordinates()
            if self.y_pos < self.up_pos_max:
                self.y_velocity *= -1
            if self.y_pos > self.low_pos_max:
                self.y_velocity *= -1

    def draw(self):
        """
        Draw hourglass on game window.
        """
        if self.appears:
            self.screen.blit(self.image, (self.x_pos, self.y_pos))

    def reset(self):
        """
        Reset some attributes to start a new game.
        """
        self.x_pos = self.start_point
        self.y_pos = randint(self.up_pos_max, self.low_pos_max)
        self.x_velocity = self.origin_x_velocity
        self.y_velocity = self.origin_y_velocity * choice(self.direction)
        self.appears = False

    def updateCoordinates(self):
        """
        Update coordinates when it crosses the screen and need to start again.
        """
        self.x_pos = self.start_point
        self.y_pos = randint(self.up_pos_max, self.low_pos_max)
        self.y_velocity = self.origin_y_velocity * choice(self.direction)
        self.appears = False

    def start(self):
        """Start make it move."""
        self.appears = True
