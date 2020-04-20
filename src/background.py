from src.data import *
from src.gameobject import GameObject


class Background(GameObject):
    """
    Class that defines the moving background.
    """
    offset_y = -50
    origin_velocity = 0.7

    def __init__(self, screen: pygame.Surface, is_left: bool = True):
        """
        Initialize object (1 game = Background object).
        :param screen: surface to display background on
        :param is_left: bool
        """
        # Display settings
        self.image = images["bg_large"] if is_left else images["bg_large2"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen = screen
        self.screenHeight, self.screenWidth = self.screen.get_rect().size

        # Position settings
        self.x_pos1 = 0
        self.x_pos2 = self.x_pos1 + self.width
        self.y_pos = self.offset_y
        self.velocity = self.origin_velocity

    def move(self):
        """
        Make Background move.
        """
        self.x_pos1 -= self.velocity
        if self.x_pos1 < -self.width:
            self.x_pos1 = self.x_pos2 + self.width

        self.x_pos2 -= self.velocity
        if self.x_pos2 < -self.width:
            self.x_pos2 = self.x_pos1 + self.width

    def draw(self):
        """
        Draw Background object on game window.
        """
        self.screen.blit(self.image, (self.x_pos1, self.y_pos))
        self.screen.blit(self.image, (self.x_pos2, self.y_pos))

    def reset(self):
        """
        Reset some attributes to start a new game.
        """
        self.x_pos1 = 0
        self.x_pos2 = self.x_pos1 + self.width
        self.y_pos = self.offset_y
        self.velocity = self.origin_velocity
