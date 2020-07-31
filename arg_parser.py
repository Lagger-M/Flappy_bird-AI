import argparse

class FlappyBirdArgParser(argparse.ArgumentParser):
    """
    Argument parser Class for Flappy bird
    """

    def __init__(self):
        """
        Initalize parser
        """
        super().__init__()
        super().add_argument("-s", "--single-player", action="store_true", help="Play game as a single player")
        super().add_argument("-t", "--train", action="store_true", help="Run training of evulation algorithm")
        super().add_argument("-e", "--emulate", action="store_true", help="Emulate best saved genome from training")

