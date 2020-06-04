from Point import Point
from time import sleep
import pygame
from random import randint


class Car:

    def __init__(self, streets, data, color, name, v=1, a=0, v_changed=0):
        self.__currentStreet = streets[0]
        self.__track = self.set_track(streets, data)
        self.__a = a
        self.__v = v
        self.__color = color
        self.get_first_three_and_last()
        self.name = name
        self.__v_max = v + 1
        self.__v_changed = v_changed
        self.__street_names = streets

    def get_first_three_and_last(self):
        for item in self.__track:
            if (item['name'] == self.__currentStreet):
                self.set_curr_p(item["coordinates"][0])
                self.set_prev_p(item["coordinates"][1])
                self.set_next_p(item["coordinates"][2])

    def get_street_points(self):
        for item in self.__track:
            if (item['name'] == self.__currentStreet):
                lenght = len(item['coordinates'])
                self.set_curr_street_p(item["coordinates"][0])
                self.set_curr_street_c(item["coordinates"][1])
                self.set_curr_street_n(item["coordinates"][2])
                self.set_curr_street_l(item["coordinates"][lenght-1])

    def set_track(self,streets,data):

        track = []
        for street in streets:
            for road in data:
                if (road['name'] == street):
                    track.append(road)

        return track

    def set_curr_street_p(self,prev):
        self.curr_street_p = prev

    def set_curr_street_c(self, curr):
        self.curr_street_p = curr

    def set_curr_street_n(self, next):
            self.curr_street_p = next

    def set_curr_street_l(self,last):
        self.curr_street_l = last

    def get_curr_street_p(self):
        return self.curr_street_p

    def get_curr_street_c(self):
        return self.curr_street_p

    def get_curr_street_n(self):
        return self.curr_street_p

    def get_curr_street_l(self):
        return self.curr_street_l

    def get_track(self):
        return self.__track

    def get_v(self):
        return self.__v

    def get_a(self):
        return self.__a

    def set_v(self, v):
        self.__v = v

    def set_a(self, a):
        self.__a = a

    def get_prev_p(self):
        return self.__prevP

    def get_next_p(self):
        return self.__nextP

    def get_curr_p(self):
        return self.__currP

    def set_curr_p(self, currP):
        self.__currP = currP

    def set_prev_p(self, prevP):
        self.__prevP = prevP

    def set_next_p(self, nextP):
        self.__nextP = nextP

    def get_neigh(self):
        return [self.get_next_p(),self.get_prev_p()]

    def set_neigh(self, point1, point2):
        self.__nextP = point1
        self.__prevP = point2

    def set_last_p(self,lastP):
        self.__lastP = lastP

    def get_last_p(self):
        return self.__lastP

    def set_vmax(self, vmax):
        self.__v_max = vmax

    def get_vmax(self):
        return self.__v_max

    def get_v_change(self):
        return self.__v_changed

    def set_v_change(self, bool):
        self.__v_changed = bool

    def set_street_names(self,streets):
        self.__street_names = streets

    def get_street_names(self):
        return self.__street_names

    def get_current_street_coords(self):
        for road in self.__track:
            if(road['name'] == self.get_current_street()):
                return road['coordinates']

    def get_current_street(self):
        return self.__currentStreet

    def set_current_street(self, street):
        self.__currentStreet = street


    # funkcja sprawdzająca czy punkty przed nim sa zajete, jesli tak -> zwolnij
    def check_points_in_front(self, points):

        currIndex = self.__currP.get_index()
        nextIndex = currIndex
        j = 0
        for i in range(0, self.get_v() + 1):


                if(points[nextIndex].get_cords() == self.curr_street_l.get_cords()):
                    dict = self.get_track()
                    index = self.get_street_names().index(self.get_current_street())
                    nextPoint = dict[(index+1)%len(self.get_street_names())]['coordinates'][0]
                    nextIndex = nextPoint.get_index()
                    j = 1
                else:
                    nextIndex = nextIndex + j
                    j = 1

                if points[nextIndex].get_taken():
                    self.set_v(min(self.get_v(), i))
                    self.set_v_change(1)

    def accel_random(self):

        random = randint(0, 100)
        if (random > 5):
            self.set_v(min(self.get_v()+1, self.get_vmax()))
        else:
            self.set_v(max(self.get_v() - 1, 0))

    def move(self, screen, points):

        self.get_street_points()

        self.check_points_in_front(points)

        self.change_point(screen, points)

        if(self.get_v_change() == 0):
            self.accel_random()
        else:
            self.set_v_change(0)



    def change_point(self, screen, points):


    
        # petla predkosci dla danego pojazdu
        for i in range(self.__v):

            track = self.get_track()

            pygame.draw.circle(screen, self.__color, self.get_curr_p().get_cords(), 3)
            pygame.draw.circle(screen, (255, 255, 255), self.get_prev_p().get_cords(), 3)

            # ustawianie czy zajety czy nie
            points[self.get_curr_p().get_index()].set_taken(1)
            points[self.get_prev_p().get_index()].set_taken(0)

            self.set_prev_p(self.get_curr_p())
            self.set_curr_p(self.get_next_p())

            changeLine = 0

            for dictionaries in track:
                if dictionaries['name'] == self.get_current_street():
                    for i in range(len(dictionaries['coordinates'])):
                        if(self.get_next_p().same(dictionaries['coordinates'][i])):
                            if(i != len(dictionaries['coordinates']) - 1):
                                self.set_next_p(dictionaries['coordinates'][i+1])

                            else:
                                changeLine = 1

                            break

                elif(changeLine == 1):
                    self.set_next_p(dictionaries['coordinates'][0])
                    self.set_current_street(dictionaries['name'])
                    break


            lastRoadList = self.get_track()[len(self.get_track())-1]['coordinates']
            if(self.get_curr_p().get_cords() == lastRoadList[len(lastRoadList)-1].get_cords()):
                 firstRoadDict = self.__track[0]
                 self.set_current_street(firstRoadDict['name'])
                 self.set_next_p(firstRoadDict['coordinates'][0])




