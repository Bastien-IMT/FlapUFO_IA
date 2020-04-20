from src.background import Background
from src.data import *
from src.hourglass import Hourglass
from src.pipes import Pipes
from src.ship import Ship


class PlayGame:
    """
    PlayGame class used for solo and duo mode.
    One user plays in one PlayGame object
    """

    username = None

    def __init__(self, screen: pygame.Surface, username: str = None, solo: bool = True, is_left: bool = True):
        """
        Initialize the player's game.
        :param screen: surface to display game
        :param username: player's username
        :param solo: True if single player False if multi players
        :param is_left: True if solo and if multi player and player 1
        """
        # game settings
        self.end_game = False
        self.username = username
        self.screen = screen
        self.is_left = is_left
        self.solo = solo

        # display settings
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.game_window_width = self.screenWidth if self.solo else self.screenWidth / 2
        self.game_window_height = self.screenHeight
        self.game_window = pygame.Surface((self.game_window_width, self.game_window_height))
        self.rect = self.screen.get_rect(left=0 if is_left else self.screenWidth / 2)

        # creating game objects
        self.ship = Ship(self.game_window, solo=solo, is_left=is_left)
        self.pipes = []
        self.pipes_number = 2 if solo else 1
        for i in range(0, self.pipes_number):
            self.pipes.append(
                Pipes(self.game_window, first=True if (i == 0) else False, single_player=solo, is_left=is_left))
        self.bg = Background(self.game_window, is_left=is_left)
        self.hourglass = Hourglass(self.game_window)

        # control settings
        if is_left:
            self.jump_key = pygame.K_SPACE
        else:
            self.jump_key = pygame.K_RETURN

    def draw(self):
        """
        Draw all game objects on game window and display player's current score (to be called in main loop).
        """
        self.screen.blit(self.game_window, self.rect)

        self.bg.draw()
        self.ship.draw()
        for pipe in self.pipes:
            pipe.draw()
        self.hourglass.draw()

        text_font = pygame.font.Font(font["bradbunr"], 25)

        string1 = "Score {0} : {1}".format(self.username, self.ship.score)
        textSurface, textRect = createTextObj(string1, text_font)
        self.game_window.blit(textSurface, textRect)

        if not self.solo:
            x_rect_split = self.game_window_width if self.is_left else 0
            pygame.draw.rect(self.game_window, colors["black"], (x_rect_split, 0, 3, self.game_window_height))

    def update(self):
        """
        Update position and state of all game objects (to be called in main loop).
        """
        if self.ship.y_pos + self.ship.height > self.game_window_height:  # Ship falls
            self.end_game = True
        self.ship.move()

        if not self.ship.goForward:
            self.bg.move()
            self.hourglass.move()
            for pipe in self.pipes:
                pipe.move()

        self.updateScore()

        # if self.ship.collision_pipes(self.pipes):
        #     self.end_game = True

        for pipe in self.pipes:
            if pipe.collide_with_ship(self.ship):
                self.end_game = True

        if self.ship.collision_hourglass(self.hourglass):
            sounds["slow"].play()
            self.hourglass.updateCoordinates()
            for pipe in self.pipes:
                pipe.velocity = pipe.origin_velocity
            self.bg.velocity = self.bg.origin_velocity
            self.hourglass.x_velocity = self.hourglass.origin_x_velocity

    def updateScore(self):
        """
        Checks if ship passed current pipe without colliding it and add 1 point if it's the case.
        It also increase objects velocity and reduce space between top and bottom pipes.
        """
        for pipe in self.pipes:
            if self.ship.x_pos > pipe.x_pos and not pipe.passed:
                self.ship.score += 1
                sounds["score"].play()
                if pipe.velocity < 13:
                    for pipe_2 in self.pipes:
                        pipe_2.velocity += 0.5
                    self.hourglass.x_velocity += 0.5

                if self.bg.velocity < 4:
                    self.bg.velocity += 0.2

                if pipe.space > 230 and self.ship.score % 2 != 0:
                    for pipe_2 in self.pipes:
                        pipe_2.space -= 5

                pipe.passed = True

                if self.ship.score % 4 == 0 and self.ship.score != 0:
                    self.hourglass.start()

    def reset(self):
        """
        Resets all game settings to start a new game quickly.
        """
        self.end_game = False
        self.ship.reset()
        self.bg.reset()
        self.hourglass.reset()
        for pipe in self.pipes:
            pipe.reset()
