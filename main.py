import pygame, setting
from utility import tools
from grid import Grid
from sys import exit

pygame.init()


class App:
    def __init__(self, WIDTH, HEIGHT) -> None:
        self.get_inputs()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CLOCK = pygame.time.Clock()
        self.FPS = self.SPEED
        self.running = True

    def get_inputs(self):
        print(
            "press left click to start maze generation. after maze generation is finished press right click to start A star."
        )
        self.SPEED = int(
            tools.take_input(
                "please enter a frame rate(0):                                        >",
                0,
            )
        )
        self.CELL_SIZE = int(
            tools.take_input(
                "please enter cell size(20):                                          >",
                20,
            )
        )
        self.MAZE_GENERATED_FULLY = int(
            tools.take_input(
                "should i finnish making the maze in 1 frame: 1 for yes 0 for no (0): >",
                0,
            )
        )
        self.PATH_FOUND_FULLY = int(
            tools.take_input(
                "should the path be found completely 1 for yes 0 for no(0):           >",
                0,
            )
        )

    def setup(self):
        self.grid = Grid(0, 0, self.WIDTH - 1, self.HEIGHT - 1, self.CELL_SIZE)
        self.maze_started = False
        self.maze_finished = False
        self.path_started = False
        self.path_finished = False

    def update(self):
        self.WIN.fill((0, 0, 0))

        # maze
        if self.maze_started and (not self.maze_finished):
            if self.MAZE_GENERATED_FULLY:
                self.maze_finished = self.grid.generate_maze_full()
            else:
                self.maze_finished = self.grid.generate_maze_step()
            self.grid.show_grid(self.WIN)

        # pathfinding
        if self.path_started and (not self.path_finished):
            if self.PATH_FOUND_FULLY:
                self.path_finished = self.grid.a_star_full()
            else:
                self.path_finished = self.grid.a_star_step()
        elif self.path_finished and (not self.PATH_FOUND_FULLY):
            self.grid.a_star_step()

        self.grid.show_grid(self.WIN)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.mouse.get_pressed()[0]:
            self.maze_started = True
        if self.maze_finished and pygame.mouse.get_pressed()[2]:
            self.path_started = True

    def run(self):
        self.setup()
        while self.running:
            self.events()

            self.update()

            self.CLOCK.tick(self.FPS)
            pygame.display.set_caption(str(self.CLOCK.get_fps()))
            pygame.display.flip()


app = App(setting.window["width"], setting.window["height"])
app.run()
