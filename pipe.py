import random
from consts import *


class Pipe:
    def __init__(self, y: int = 100) -> None:
        """
        Pipe initialization
        :param y: y axis value for pipe. Default 100.
        """
        self.x = GAME_RES[0]
        self.y_top = y if y != 100 else random.randint(PIPE_TOP_MAX_Y, PIPE_TOP_MIN_Y)
        self.y_bot = self.y_top + PIPE_HEIGHT + PIPE_GAP
        self.top_pipe_img = pygame.transform.rotate(PIPE_IMG, 180)
        self.bot_pipe_img = PIPE_IMG
        self.passed = False

    def draw(self, win: object) -> None:
        """
        Draw pipe
        :param win: window object
        :return:
        """
        win.blit(self.top_pipe_img, (self.x, self.y_top))
        win.blit(self.bot_pipe_img, (self.x, self.y_bot))

    def move(self) -> None:
        """
        Move pipe
        :return:
        """
        self.x -= GAME_SPEED

    def collide(self, bird: object) -> bool:
        """
        Check collision between pipe and bird based on pixel collision.
        :param bird: Bird object
        :return: True if bird hits any pipe, otherwise False
        """
        top_pipe_mask = pygame.mask.from_surface(self.top_pipe_img)
        bot_pipe_mask = pygame.mask.from_surface(self.bot_pipe_img)
        bird_mask = bird.get_mask()

        top_pipe_offset = (self.x - bird.x, self.y_top - round(bird.y))
        bot_pipe_offset = (self.x - bird.x, self.y_bot - round(bird.y))

        if bird_mask.overlap(top_pipe_mask, top_pipe_offset) or bird_mask.overlap(bot_pipe_mask, bot_pipe_offset):
            return True
        return False

    def check_passed(self, bird: object) -> bool:
        """
        Check if bird successfully passed the pipe
        :param bird: bird object
        :return: True if bird passed the pipe, otherwise False
        """
        if bird.x > self.x + self.top_pipe_img.get_size()[0]:
            self.passed = True
            return True
        return False

    def delete_pipe(self) -> bool:
        """
        Returns true if pipe should be deleted (moved far left so it cannot be seen)
        :return: True if pipe cannot be seen anymore, otherwise False
        """
        if self.x < PIPE_DELETE_X_TRESHOLD:
            return True
        return False
