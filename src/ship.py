from src.data import *
from src.gameobject import GameObject
from src.hourglass import Hourglass


class Ship(GameObject):
    """
    Class that defines the character of the game (UFO ship).
    """
    origin_x_velocity = 4
    origin_y_velocity = -10

    def __init__(self, screen: pygame.Surface, solo: bool = True, is_left: bool = True):
        """
        Initialize the object.
        :param screen: pygame surface to display ship
        :param solo: True if solo mode False if duo mode
        :param is_left: True if screen left else false
        """

        # display settings
        self.screen = screen
        self.screenHeight = self.screen.get_rect().size[1]
        self.image = images["ship"]
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size
        self.spriteJump = spriteShipJump1 if is_left else spriteShipJump2
        self.spriteFall = spriteShipFall1 if is_left else spriteShipFall2

        # position settings
        self.x_pos = -self.width
        self.y_pos = self.screenHeight / 2 - self.height

        # movement settings
        self.isJump = False
        self.y_velocity = self.origin_y_velocity
        self.x_velocity = self.origin_x_velocity
        self.max_pos_y = maxPosShip

        # internal settings to make it run
        self.score = 0
        self.spriteCount = 0
        self.goForward = True
        self.final_pos_x = 150 if solo else 75

    def draw(self):
        """
        Draw ship and update animation on game window.
        """

        # I reset it at 24 because they're 4 images and I want the reduce the animation speed by 6 (6*4=24)
        if self.spriteCount + 1 >= 24:
            self.spriteCount = 0
        if self.isJump:
            self.screen.blit(self.spriteJump[self.spriteCount // 6], (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.spriteFall[self.spriteCount // 6], (self.x_pos, self.y_pos))
        self.spriteCount += 1

    def move(self):
        """
        Make ship move and update its position.
        """
        neg = -1  # neg used to change direction of velocity if ship is jumping or not

        if self.goForward:
            self.x_pos += self.x_velocity

        if self.x_pos > self.final_pos_x and self.goForward:
            self.goForward = False

        if self.y_velocity > 0:
            self.isJump = False
            neg = 1

        self.y_pos += (self.y_velocity ** 2) * neg / 15  # formula to simulate a real fall or jump
        self.y_velocity += 0.5

    def jump(self):
        """
        Make ship jump if it is not too high.
        """
        if self.y_pos > self.max_pos_y + self.height:
            self.isJump = True
            self.y_velocity = -13.5
            sounds["jump"].play()

    def collision_pipes(self, pipes_list: list):
        """
        Checks if ship collides with a pipe.
        :param pipes_list: all pipes on the game window
        :return: True or False
        """
        result = False
        for pipe in pipes_list:
            if self.x_pos + self.width > pipe.x_pos and self.x_pos < pipe.x_pos + pipe.width:
                if self.y_pos < pipe.y_pos_up + pipe.height:  # collide with top
                    result = True
                    break
                elif self.y_pos + self.height > pipe.y_pos_down:  # collide with bottom
                    result = True
                    break
        return result

    def collision_hourglass(self, hourglass: Hourglass):
        """
        Checks if ship collides with a pipe.
        :param hourglass: Clock_item object
        :return: True of False
        """
        result = False
        if self.x_pos + self.width >= hourglass.x_pos and self.x_pos < hourglass.x_pos + hourglass.width:  # x collapse
            if self.y_pos < hourglass.y_pos + hourglass.height and self.y_pos + self.height > hourglass.y_pos:
                # y collapse top ship
                result = True
            elif self.y_pos + self.height > hourglass.y_pos and self.y_pos < hourglass.y_pos + hourglass.height:
                # y collapse bottom ship
                result = True
        return result

    def reset(self):
        """
        Resets ship object to start a new game.
        :return:
        """
        self.x_pos = -self.width
        self.y_pos = self.screenHeight / 2 - self.height
        self.isJump = False
        self.y_velocity = self.origin_y_velocity
        self.x_velocity = self.origin_x_velocity
        self.score = 0
        self.spriteCount = 0
        self.goForward = True

    def get_mask(self):
        return pygame.mask.from_surface(images["ship"])
