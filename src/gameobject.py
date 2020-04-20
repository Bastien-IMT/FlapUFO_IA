from abc import ABC


class GameObject(ABC):
    """
    Abstract class for all objects in game.
    """

    def move(self): pass

    def draw(self): pass

    def reset(self): pass
