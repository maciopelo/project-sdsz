import pygame
from fetchPointsFromFile import *
from Car import Car
from InterfaceStuff import pause
import time
from RepeatedTimer import RepeatedTimer, start_traffic_lights
from random import randint
from SimulationStatistics import add_stats, making_file_statistic, run_stats
import matplotlib.pyplot as plt
import threading


class Screen:
    def __init__(self, data, points, streets, resolution, colors, over):
        self.data = data
        self.points = points
        self.resolution = resolution
        self.streets = streets
        self.colors = colors
        self.over = over
        self.cars = self.initialize_cars()
        self.iteration = 0


    def initialize_points(self, screen):
        for i in range(len(points)):
            pygame.draw.circle(screen, self.colors["white"], self.points[i].get_cords(), 3)

    def initialize_cars(self):
        cars = []
        for i in range(20):
            if (i % 11 == 0):

                car = Car(self.streets[0], data, self.colors["blue"], "car" + str(i), self.over, 0)

            else:

                car = Car(self.streets[1], data, self.colors["red"], "car" + str(i), self.over, 0)

            cars.append(car)
        return cars

    def start(self):

        making_file_statistic()
        thread = threading.Thread(target=run_stats)

        # initialize
        pygame.init()

        # create screen
        screen = pygame.display.set_mode(resolution)

        # running condition and title
        running = True
        pygame.display.set_caption("Cracow Road Simulation")

        # time delay
        clockobject = pygame.time.Clock()
        tick = 15

        # background color
        screen.fill(self.colors["black"])

        # draw road
        self.initialize_points(screen)

        # pause message
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('To Pause press P To Continue press C', True, self.colors["green"])
        text_rect = text.get_rect()
        text_rect.center = (resolution[0] // 2, resolution[1] // 2)
        screen.blit(text, text_rect)

        # thread for counting time - to handle traffic lights
        rt = RepeatedTimer(1.00, start_traffic_lights, points, screen)

        try:
            thread.start()

            # Main Loop
            time.sleep(1)
            while running:
                clockobject.tick(tick)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            pause(clockobject)
                        elif event.key == pygame.K_RIGHT:
                            tick = max(tick + 5, 3)
                        elif event.key == pygame.K_LEFT:
                            tick = max(tick - 5, 3)

                for car in self.cars:
                    car.move(screen, points)

                add_stats(self.cars, self.iteration)
                self.iteration += 1
                pygame.display.update()

                pass

        finally:
            rt.stop()


resolution = (1800, 900)

colors = {
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "cyan": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "grey": (22, 22, 22)
}

# fetching essential data from json
data, points = change_points_from_float_to_int("roads.json")
over = set_overtake_track(data)

# roads for tests
tmp = ["dluga-basztowa-cw-skret", "basztowa-cw"]
tmp2 = ["basztowa-dunaj-cw","basztowa-cw-basztowa-prosto", "basztowa-cw"]

streets = [tmp, tmp2]

s = Screen(data, points, streets, resolution, colors, over)
s.start()










