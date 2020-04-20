import neat
import pygame

from src.background import Background
from src.data import SCREEN_HEIGHT, SCREEN_WIDTH
from src.pipesIA import PipesIA
from src.ship import Ship

GEN = 0
SCREEN = set()


def draw_window(win, ships, pipes, bg, score, gen):
    bg.draw()
    STAT_FONT = pygame.font.SysFont("comicsans", 50)

    for pipe in pipes:
        pipe.draw()

    text = STAT_FONT.render(f"Score : {score}", 1, (255, 255, 255))
    win.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render(f"Generation : {str(gen)}", 1, (255, 255, 255))
    win.blit(text, (10, 10))

    for ship in ships:
        ship.draw()

    pygame.display.update()


def run(config_path, screen):
    global SCREEN
    SCREEN = screen
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genome, 50)


def eval_genome(genomes, config):
    global GEN, SCREEN
    GEN += 1
    nets = []
    ge = []
    ships = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ships.append(Ship(SCREEN))
        g.fitness = 0
        ge.append(g)

    bg = Background(SCREEN, is_left=True)
    pipes = [PipesIA(SCREEN)]

    score = 0
    clock = pygame.time.Clock()

    play = True
    while play:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(ships) > 0:
            if len(pipes) > 1 and ships[0].x_pos > pipes[0].x_pos + pipes[0].width:  # if we passed the pipe
                pipe_ind = 1  # we will look at the second pipe
        else:
            play = False
            break

        for x, ship in enumerate(ships):
            ship.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (ship.y_pos, abs(ship.y_pos - pipes[pipe_ind].y_pos_up + pipes[pipe_ind].height),
                 abs(ship.y_pos - pipes[pipe_ind].y_pos_down)))

            if output[0] > 0.5:
                ship.jump()

        remove = []
        add_pipe = False
        for pipe in pipes:

            for x, ship in enumerate(ships):
                if pipe.collide_with_ship(ship):
                    ge[x].fitness -= 1
                    ships.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x_pos < ship.x_pos:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x_pos + pipe.width < 0:
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(PipesIA(SCREEN))

        for r in remove:
            pipes.remove(r)

        for x, ship in enumerate(ships):
            if ship.y_pos + ship.height >= SCREEN_HEIGHT or ship.y_pos < 0:
                ships.pop(x)
                nets.pop(x)
                ge.pop(x)

        bg.move()
        draw_window(SCREEN, ships, pipes, bg, score, GEN)
