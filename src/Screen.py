import pygame
from fetchPointsFromFile import *
from Car import Car
from InterfaceStuff import *
import time
from RepeatedTimer import RepeatedTimer, start_traffic_lights
from random import randint
from SimulationStatistics import *
import matplotlib.pyplot as plt
import threading
from Streets import possible_streets
import  time
import datetime as dt
from Car import outflows

class Screen:
    def __init__(self, data, points, streets, resolution, colors, over):
        self.data = data
        self.points = points
        self.resolution = resolution
        self.streets = streets
        self.colors = colors
        self.over = over
        self.cars = []
        self.iteration = 0

#macipelo

    def initialize_points(self, screen):
        for i in range(len(points)):
            pygame.draw.circle(screen, self.colors["white"], self.points[i].get_cords(), 3)

    def initialize_cars(self, how_many):
        for i in range(how_many):
            car = Car(self.streets[randint(0, len(self.streets)-1)], data, self.colors["red"], "car"+str(i), self.over, randint(0, 2))
            self.cars.append(car)

    def check_if_reached_end(self):
        for i in range(len(self.cars)):
            if self.cars[i].track_end:
                del self.cars[i]
                break

    def random_initialize(self, amount):
        if len(self.cars) < amount:
            x = randint(0, 100)
            if x < 20:
                for i in range(10):
                    car = Car(self.streets[randint(0, len(self.streets) - 1)], data, self.colors["red"], "car",
                          self.over, 0)
                    self.cars.append(car)

    # INFLOW
    def generate_car_on_each_intersection(self, amount):
        for track in possible_streets:
            for i in range(amount):
                car = Car(possible_streets[track][randint(0, len(possible_streets[track]) - 1)],
                          data, self.colors["red"], "car", self.over, 0)
                self.cars.append(car)




    def start(self, starting_num_cars, inflow, amount_of_inflow, time_end, fig):



        #Starting number of cars

        self.initialize_cars(starting_num_cars)


        #Inflows over time
        filharmonia_list = [0]
        idziego_list = [0]
        poczta_list = [0]
        slowackiego_list = [0]
        bagatela_list = [0]



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
        tick = 10


        # background color
        screen.fill(self.colors["black"])

        # draw road
        self.initialize_points(screen)

        # pause and velocity message
        text = ['To Pause press P To Continue press C', 'Average V: ', 'Average V_max: ', 'Percentage difference: ', 'Iteration: ', 'km/h', 'Number of Cars: ', 'Time: ', 'Inflow: ', 'Number of Inflow: ', 'Starting number of cars: ']
        message(screen, (self.resolution[0] // 2, self.resolution[1] // 2), self.colors, text[0])
        message(screen, (100, 50), self.colors, text[1])
        message(screen, (450, 50), self.colors, text[5])
        message(screen, (145, 100), self.colors, text[2])
        message(screen, (450, 100), self.colors, text[5])
        message(screen, (200, 700), self.colors, text[3])
        message(screen, (90, 800), self.colors, text[4])
        message(screen, (140, 750), self.colors, text[6])
        message(screen, (50, 850), self.colors, text[7])
        message(screen, (self.resolution[0] // 2 - 200, self.resolution[1] // 2 - 100), self.colors, text[8] + str(inflow))
        message(screen, (self.resolution[0] // 2 + 200, self.resolution[1] // 2 - 100), self.colors, text[9] + str(inflow_number))
        message(screen, (self.resolution[0] // 2, self.resolution[1] // 2 - 200), self.colors, text[10] + str(starting_num_cars))

        # thread for counting time - to handle traffic lights
        rt = RepeatedTimer(1.00, start_traffic_lights, points, screen)

        try:
            #thread.start()
            tab = [0, 0]


            # start timer
            start_time = dt.datetime.today().timestamp()

            # Main Loop
            time.sleep(1)
            while running:
                clockobject.tick(tick)
                time_diff = dt.datetime.today().timestamp() - start_time


                tab[1] = tab[0]
                tab[0] = int(time_diff)
                if tab[0] - tab[1] == 1 and tab[0] % inflow == 0:
                    self.generate_car_on_each_intersection(amount_of_inflow)
                    filharmonia_list.append(outflows['filharmonia'])
                    idziego_list.append(outflows['idziego'])
                    poczta_list.append(outflows['poczta'])
                    slowackiego_list.append(outflows['slowackiego'])
                    bagatela_list.append(outflows['bagatela'])




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

                self.check_if_reached_end()
                #self.random_initialize(70)

                add_stats(self.cars, self.iteration, time_diff)
                self.iteration += 1
                show_statistics(screen, self.colors)

                pygame.display.update()

                if(time_diff > time_end):
                    running = False

        finally:
            rt.stop()

            #ploting
            plot_numcars_v(inflow, amount_of_inflow, fig, starting_num_cars)
            plot_t_numcars(inflow, amount_of_inflow, fig, starting_num_cars)
            plot_t_v(inflow, amount_of_inflow, fig, starting_num_cars)
            plot_inflow(filharmonia_list, idziego_list, poczta_list, slowackiego_list, bagatela_list, inflow, amount_of_inflow, fig, starting_num_cars)
            outflow = [filharmonia_list, idziego_list, poczta_list, slowackiego_list, bagatela_list]
            final_data_append(fig, starting_num_cars, outflow)






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

def change_to_list(possible_streets):
    streets = []
    for track in possible_streets:
        for street in possible_streets[track]:
            streets.append(street)

    return streets


# fetching essential data from json
data, points = change_points_from_float_to_int("roads.json")
over = set_overtake_track(data)

#Input data
starting_num_cars = [300]
inflow_list = [15]
inflow_number_list = [5]
time_end = 20
fig = 1  #10

#Final data file
making_final_data()


streets = change_to_list(possible_streets)
s = Screen(data, points, streets, resolution, colors, over)
for inflow in inflow_list:
    for num_cars in starting_num_cars:
        for inflow_number in inflow_number_list:

            global outflows
            outflows["filharmonia"] = 0
            outflows["idziego"] = 0
            outflows["poczta"] = 0
            outflows["slowackiego"] = 0
            outflows["bagatela"] = 0

            s.start(num_cars, inflow, inflow_number, time_end, fig)
            del s
            data, points = change_points_from_float_to_int("roads.json")
            over = set_overtake_track(data)
            streets = change_to_list(possible_streets)
            fig += 1
            s = Screen(data, points, streets, resolution, colors, over)










