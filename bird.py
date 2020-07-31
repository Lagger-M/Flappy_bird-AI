from consts import *


class Bird:
    img_order = [0, 1, 2, 1]  # images of bird to be displayed in sequence

    def __init__(self) -> None:
        """
        Class initilization
        """
        self.x = BIRD_POS[0]
        self.y = BIRD_POS[1]
        self.img = BIRD_IMGS[0]
        self.img_order_index = 0
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0  # velocity goes up, + goes down
        self.heigth = self.y
        self.active = True  # for genetic algorithm purpose

    def draw(self, win: object) -> None:
        """
        Draw picture of bird. Tilt image based on the position of bird as well
        :param win: window object
        :return: None
        """
        self.img_order_index = self.img_order_index + 1 if self.img_order_index != len(self.img_order) - 1 else 0
        self.img = BIRD_IMGS[self.img_order[self.img_order_index]]

        # IMG tilting
        if self.heigth > self.y:
            self.img = pygame.transform.rotate(self.img, 20)
        elif self.heigth < self.y:
            self.img = pygame.transform.rotate(self.img, -20)

        win.blit(self.img, (self.x, self.y))

    def move(self) -> None:
        """
        Move birds. Defines how bird moves.
        :return:
        """
        # UP DOWN movement
        self.tick_count += 1
        d = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2
        d = MAX_POSITIVE_VELOCITY if d >= MAX_POSITIVE_VELOCITY else d
        d = d - 2 if d < 0 else d

        self.y += d

    def jump(self) -> None:
        """
        Jump action. Just change velocity and move will do the rest.
        :return:
        """
        self.velocity = -10.5
        self.tick_count = 0
        self.heigth = self.y

    def get_mask(self) -> object:
        """
        Fets the mask for the current image of the bird, for pixel collision.
        :return: None
        """
        return pygame.mask.from_surface(self.img)
