from random import randint

from src.data import *
from src.gameobject import GameObject
from src.ship import Ship


class Pipes(GameObject):
    """
    Class that defines pipes that the character has to pass threw.
    """
    origin_space = 300
    origin_velocity = 7.5
    max_pos = -570
    min_pos = -220

    def __init__(self, screen: pygame.Surface, first: bool = True, single_player: bool = True, is_left: bool = True):
        """
        Initialize pipes object (= top pipe + bottom pipe).
        :param screen: surface to display pipes
        :param first: bool if this pipe is the first that must appear on the screen
        :param single_player: bool True if single player, False if multi players
        """

        # display settings
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_rect().size
        self.image = {"up": images["pipe_up1"], "down": images["pipe_down1"]} if is_left else {"up": images["pipe_up2"],
                                                                                               "down": images[
                                                                                                   "pipe_down2"]}
        self.rect = self.image["up"].get_rect()
        self.width, self.height = self.image["up"].get_rect().size

        # internal settings to make it run
        self.passed = False
        self.first = first
        self.single_player = single_player

        # position settings
        self.space = self.origin_space
        self.space_next_pipes = (self.screenWidth / 2) + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = self.origin_velocity
        self.start_point = self.screenWidth - self.width
        if first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + self.space_next_pipes

    def move(self):
        """
        Make pipes move.
        """
        self.x_pos -= self.velocity
        if self.x_pos < -self.width:
            self.updateCoordinates()

    def draw(self):
        """
        Draw pipes on game window.
        """
        self.screen.blit(self.image["up"], (self.x_pos, self.y_pos_up))
        self.screen.blit(self.image["down"], (self.x_pos, self.y_pos_down))

    def reset(self):
        """
        Reset some attributes to start a new game.
        """
        self.space = self.origin_space
        if self.first:
            self.x_pos = self.start_point
        else:
            self.x_pos = self.start_point + self.space_next_pipes
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.velocity = self.origin_velocity
        self.passed = False

    def updateCoordinates(self):
        """
        Update coordinates when pipes cross the screen and need to start again.
        """
        self.x_pos = self.screenWidth + self.width
        self.y_pos_up = randint(self.max_pos, self.min_pos)
        self.y_pos_down = self.y_pos_up + self.height + self.space
        self.passed = False

    def collide_with_ship(self, ship: Ship):
        """
        Check if ship collide with top of bottom pipe
        :param ship:
        :return:
        """
        ship_mask = ship.get_mask()
        top_mask = pygame.mask.from_surface(self.image["up"])
        bottom_mask = pygame.mask.from_surface(self.image["down"])

        top_offset = round(self.x_pos - ship.x_pos), round(self.y_pos_up - round(ship.y_pos))
        bottom_offset = round(self.x_pos - ship.x_pos), round(self.y_pos_down - round(ship.y_pos))

        b_point = ship_mask.overlap(bottom_mask, bottom_offset)
        t_point = ship_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
