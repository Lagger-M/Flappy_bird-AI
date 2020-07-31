import pickle

import neat

from arg_parser import FlappyBirdArgParser
from bird import Bird
from consts import *
from floor import Floor
from pipe import Pipe


def execute_if_attribute_true(obj: object, atr_name: str, f_name: str, *args) -> None:
    """
    Execute function f_name of object objc, if attribute atr_name oh object obj is True. If obj is a list, then
    this applies for all objects of this list.
    :param obj: object
    :param atr_name: name of the object atrribute to check
    :param f_name: function of object to execute
    :param args: arguments of function
    :return:
    """
    if type(obj) == list:
        for o in obj:
            func = getattr(o, f_name)
            if hasattr(o, atr_name) and o.active:
                func(*args)
            elif not hasattr(o, atr_name):
                func(*args)
    else:
        func = getattr(obj, f_name)
        if hasattr(obj, atr_name) and obj.active:
            func(*args)
        elif not hasattr(obj, atr_name):
            func(*args)


def draw_window(win: object, score: int, *args) -> None:
    """
    Draw all objects on window
    :param win: window object
    :param score: score to show
    :param args: objects to draw
    :return:
    """
    win.blit(BG_IMG, BG_POS)

    # Draw score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (GAME_RES[0] - score_label.get_width() - 15, 10))

    # draw all objects that are active
    for arg in args:
        execute_if_attribute_true(arg,'active','draw',win)
    pygame.display.update()


def move_objects(*args) -> None:
    """
    Call move method on all objects in arguments. Supports list of objects and single objects
    :param args: objects to move
    :return:
    """
    for arg in args:
        execute_if_attribute_true(arg, 'active', 'move')


def check_collision(bird: object, obj_list: list) -> bool:
    """
    Check if collision between bird and any object in obj_list happened.
    :param bird: bird object
    :param obj_list: objects to check collision with
    :return: True if bird hit any object in obj_list, otherwise False
    """
    if bird.y < -10:
        return True
    for i in obj_list:
        if i.collide(bird):
            return True
    return False


def check_passed_pipe(bird: object, pipe_list: list) -> list:
    """
    Returns pipes that have been passed
    :param bird: bird object
    :param pipe_list: list of pipes
    :return: list of pipes objects that were passed
    """
    passed_pipes = []
    for pipe in pipe_list:
        if pipe.passed is False and pipe.check_passed(bird):
            passed_pipes.append(pipe)
    return passed_pipes


def check_pipe_to_delete(pipe_list: list) -> list:
    """
    Return list of pipes to delete (moved out of screen)
    :param pipe_list: list of pipe objects
    :return: list of pipe objects to delete
    """
    to_delete = []
    for pipe in pipe_list:
        if pipe.delete_pipe():
            to_delete.append(pipe)
    return to_delete


def handle_game_event(event, bird) -> None:
    """
    Handle events in game
    :param event: pygame event
    :return:
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    elif event.type == pygame.KEYDOWN:
        bird.jump()


def run_single_player() -> None:
    """
    Single player mode
    :return:
    """
    score = 0
    win = pygame.display.set_mode(GAME_RES)
    bird = Bird()
    floor = Floor()
    pipes = [Pipe()]
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)  # set frame rate
        for event in pygame.event.get():
            handle_game_event(event, bird)

        closest_pipe = next((pipe for pipe in pipes if pipe.passed is False), None)
        move_objects([bird, floor] + pipes)
        draw_window(win, score, bird, floor, pipes)
        if check_collision(bird, pipes + [floor]):
            break

        if len(check_passed_pipe(bird, pipes)) > 0:
            score += 1
            pipes.append(Pipe())
        for pipe_to_del in check_pipe_to_delete(pipes):
            pipes.remove(pipe_to_del)


def run(genomes, config):
    nets = []  # Neural nets
    birds = []  # birds
    ge = []  # genomes

    score = 0

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        ge.append(genome)

    win = pygame.display.set_mode(GAME_RES)
    floor = Floor()
    pipes = [Pipe(y=-300)]
    clock = pygame.time.Clock()

    run = True
    while run:
        if score > 100:
            break
        clock.tick(30)
        for event in pygame.event.get():
            handle_game_event(event, _)

        add_to_score = 0
        closest_pipe = next((pipe for pipe in pipes if pipe.passed is False), None)
        for i, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            if bird.active:
                ge[i].fitness += 0.1
                bot_pipe_distance = abs(bird.y - closest_pipe.y_bot)
                top_pipe_distance = abs(bird.y - (closest_pipe.y_top + closest_pipe.top_pipe_img.get_size()[1]))
                output = nets[birds.index(bird)].activate((bot_pipe_distance, top_pipe_distance))
                if output[0] > 0.5:  # jump condition
                    bird.jump()
                if check_collision(bird, pipes + [floor]): # check collision with other objects
                    bird.active = False
                    ge[i].fitness -= 1
                if len(check_passed_pipe(bird, pipes)) > 0: # check if pipe was passed
                    ge[i].fitness += 5
                    add_to_score = 1

        move_objects(birds, floor, pipes)
        draw_window(win, score, birds, floor, pipes)

        if add_to_score == 1:
            pipes.append(Pipe())
            score += 1

        for pipe_to_del in check_pipe_to_delete(pipes):
            pipes.remove(pipe_to_del)


if __name__ == '__main__':
    args = FlappyBirdArgParser().parse_args()
    pygame.font.init()  # init font
    STAT_FONT = pygame.font.SysFont("comicsans", 50)
    if args.single_player:
        run_single_player()
    elif args.train:
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, NEAT_CONFIG)
        p = neat.Population(config)
        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 100 generations.
        winner = p.run(run, 100)
        with open(WINNER_FILE, 'wb') as f:
            pickle.dump(winner, f)

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))
    elif args.emulate:
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, NEAT_CONFIG)
        with open(WINNER_FILE, 'rb') as f:
            genome = pickle.load(f)
        genomes = [(1, genome)]
        run(genomes, config)
