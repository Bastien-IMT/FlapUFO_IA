import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# const

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

maxPosShip = 10

# IMAGES
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
images = {"bg": pygame.image.load("src/assets/bg.png").convert(),
          "icon": pygame.image.load("src/assets/icon.png").convert_alpha(),
          "pipe_down1": pygame.image.load("src/assets/pipe_down.png").convert_alpha(),
          "pipe_up1": pygame.image.load("src/assets/pipe_up.png").convert_alpha(),
          "pipe_down2": pygame.image.load("src/assets/pipe_down2.png").convert_alpha(),
          "pipe_up2": pygame.image.load("src/assets/pipe_up2.png").convert_alpha(),
          "alien": pygame.image.load("src/assets/alien.png").convert_alpha(),
          "ship": pygame.image.load("src/assets/ship.png").convert_alpha(),
          "logo": pygame.image.load("src/assets/logo.png").convert_alpha(),
          "bg_large": pygame.image.load("src/assets/bg_large.png").convert(),
          "bg_large2": pygame.image.load("src/assets/bg_large2.png").convert(),
          "start": pygame.image.load("src/assets/start.png").convert_alpha(),
          "highscores": pygame.image.load("src/assets/highscore.png").convert_alpha(),
          "ready": pygame.image.load("src/assets/ready.png").convert_alpha(),
          "clock": pygame.image.load("src/assets/clock.png").convert_alpha(),
          "see_highscore": pygame.image.load("src/assets/see_highscores.png").convert_alpha(),
          "start_solo": pygame.image.load("src/assets/start_solo.png").convert_alpha(),
          "start_2_players": pygame.image.load("src/assets/start_2_players.png").convert_alpha(),
          "menu": pygame.image.load("src/assets/menu.png").convert_alpha(),
          "boom": pygame.image.load("src/assets/boom.png").convert_alpha(),
          "start_again": pygame.image.load("src/assets/start_again.png").convert_alpha(),
          "ia_menu": pygame.image.load("src/assets/ia_menu.png").convert_alpha()
          }

spriteShipJump1 = [pygame.image.load("src/assets/shipJump1/1.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump1/2.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump1/3.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump1/4.png").convert_alpha()]

spriteShipFall1 = [pygame.image.load("src/assets/shipFall1/1.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall1/2.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall1/3.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall1/4.png").convert_alpha()]

spriteShipJump2 = [pygame.image.load("src/assets/shipJump2/1.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump2/2.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump2/3.png").convert_alpha(),
                   pygame.image.load("src/assets/shipJump2/4.png").convert_alpha()]

spriteShipFall2 = [pygame.image.load("src/assets/shipFall2/1.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall2/2.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall2/3.png").convert_alpha(),
                   pygame.image.load("src/assets/shipFall2/4.png").convert_alpha()]

# FONT
font = {"bradbunr": "src/assets/BradBunR.ttf"}


def createTextObj(text: str, font_object: pygame.font.Font):
    """
    Creates a text object with a string and a font
    :type font_object: pygame.font.Font(font_name, 75)
    :param text: string to display
    :param font_object: font in which to display text
    :return: a surface with the text and its rect
    """
    textSurface = font_object.render(text, True, colors["white"])
    return textSurface, textSurface.get_rect()


# SOUNDS

sounds = {"music": pygame.mixer.music.load("src/assets/music.mp3"), "crash": pygame.mixer.Sound("src/assets/crash.wav"),
          "jump": pygame.mixer.Sound("src/assets/jump.wav"), "score": pygame.mixer.Sound("src/assets/score.wav"),
          "slow": pygame.mixer.Sound("src/assets/slow.wav")}

# COLORS
colors = {"black": (0, 0, 0), "darkgray": (70, 70, 70), "gray": (128, 128, 128), "lightgray": (200, 200, 200),
          "white": (255, 255, 255), "red": (255, 0, 0),
          "darkred": (128, 0, 0), "green": (0, 255, 0), "darkgreen": (0, 128, 0), "blue": (0, 0, 255),
          "navy": (0, 0, 128), "darkblue": (0, 0, 128),
          "yellow": (255, 255, 0), "gold": (255, 215, 0), "orange": (255, 165, 0), "lilac": (229, 204, 255),
          "lightblue": (135, 206, 250), "teal": (0, 128, 128),
          "cyan": (0, 255, 255), "purple": (150, 0, 150), "pink": (238, 130, 238), "brown": (139, 69, 19),
          "lightbrown": (222, 184, 135), "lightgreen": (144, 238, 144),
          "turquoise": (64, 224, 208), "beige": (245, 245, 220), "honeydew": (240, 255, 240),
          "lavender": (230, 230, 250), "crimson": (220, 20, 60)}

# score
name_score_file = "src/assets/scores"
