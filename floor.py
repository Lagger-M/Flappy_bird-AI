from consts import *

class Floor:
    def __init__(self) -> None:
        """
        Initialization of floor. Floor consists of 2 pictures moving to the left.
        """
        self.floors = [FLOOR_POS[0], FLOOR_POS[0] + FLOOR_WIDTH]
        self.y = FLOOR_POS[1]
        self.img = FLOOR_IMG

    def draw(self, win: object) -> None:
        """
        Draw floor
        :param win: window object
        :return:
        """
        for f in self.floors:
            win.blit(self.img, (f, self.y))

    def move(self) -> None:
        """
        Move floor. If one floor picture disappears on the left, then move it after the next floor picture.
        :return:
        """
        self.floors = [f - GAME_SPEED for f in self.floors]
        for i in range(0, len(self.floors)):
            if self.floors[i] < -FLOOR_WIDTH:
                self.floors[i] = FLOOR_POS[0] + FLOOR_WIDTH

    def collide(self, bird: object) -> bool:
        """
        Collision check between floor and bird
        :param bird: Bird object
        :return: True if bird hits the floor, otherwise False
        """
        if bird.y >= self.y:
            return True
        return False
