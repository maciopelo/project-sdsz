import pygame
from random import randint
from copy import deepcopy, copy
import json
outflows = {
                "filharmonia": 0,
                "idziego": 0,
                "poczta": 0,
                "slowackiego": 0,
                "bagatela": 0,
            }
class Car:

    def __init__(self, streets, data, color, name, over, v=1, a=0, v_changed=0):
        self.__currentStreet = streets[0]
        self.__data = data
        self.__track = self.set_track(streets, data)
        self.__a = a
        self.__v = v
        self.__color = color
        self.get_first_three_and_last()
        self.name = name
        self.rem_current_street = streets[0]
        self.__v_max = 3 if randint(0, 100) < 95 else 2
        self.__v_changed = v_changed
        self.__street_names = streets
        self.__overtake_track = over
        self.track_end = 0



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

    def set_track_from_track(self, track):
        self.__track = track


    def set_overtake_track(self, streets, data):
        track = []

        for street in streets:
            for road in data:
                if (road['name'] == street):
                    track.append(road['coordinates'])


        return track


    def set_color(self, color):
        self.__color = color


    def set_color_from_v(self, v):
        if(v == 0):
            self.set_color((255, 0, 0))
        elif(v == 1):
            self.set_color((255, 102, 0))
        elif(v == 2):
            self.set_color((255, 204, 0))
        elif(v == 3):
            self.set_color((51, 204, 51))


    def get_data(self):
        return  self.__data

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

    def get_overtake_track(self):
        return self.__overtake_track

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

    def get_color(self):
        return self.__color

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

        nextIndex = self.__currP.get_index()

        for i in range(1, self.get_v() + 1):


                if(points[nextIndex].get_cords() == self.curr_street_l.get_cords()):
                    dict = self.get_track()
                    index = self.get_street_names().index(self.get_current_street())
                    nextPoint = dict[(index+1)%len(self.get_street_names())]['coordinates'][0]
                    nextIndex = nextPoint.get_index()
                else:
                    nextIndex = nextIndex + 1

                if points[nextIndex].get_taken():
                    self.set_v(min(self.get_v(), i - 1))
                    self.set_v_change(1)
                    if(i == 1):
                        self.change_line(points)
                    break

        split = deepcopy(self.get_current_street().split('-'))
        if(split[1] == 'left' and self.get_v_change() == 0):
            self.change_line(points)
            self.set_v_change(1)


    def accel_random(self):

        random = randint(0, 100)
        if (random > 5):
            self.set_v(min(self.get_v()+1, self.get_vmax()))
        else:
            self.set_v(max(self.get_v() - 1, 0))
            self.set_v(max(self.get_v() - 1, 0))


    def check_if_line_free(self, points):
        procent_go = 90
        oposite, indexes = self.opposite_rl()
        list1 = indexes[0]
        list2 = indexes[1]
        rem_j = 1
        global_index = deepcopy(self.get_curr_p().get_index())

        for i in range(len(self.get_overtake_track()[list2])):
            if(global_index == self.get_overtake_track()[list2][i].get_index()):
                break

        giga_index = self.get_overtake_track()[list1][i].get_index()

        for j in range(0, self.get_vmax()):
            if(points[giga_index - j].get_taken()):
                procent_go = 20
                rem_j = j
                
        for k in range(0, self.get_vmax()):
            if(points[giga_index + k].get_taken()):
                procent_go = 0
                rem_j = 0

        return procent_go, oposite, rem_j, giga_index, list1

    def change_line(self, points):
        split = deepcopy(self.get_current_street().split('-'))
        if(split[1] == 'right' or split[1] == 'left'):
            procent_go, street, can_go, index, overtake_index = self.check_if_line_free(points)
            if(can_go):
                overtake = deepcopy(self.get_overtake_track())
                procent = randint(0,100)
                if(procent < procent_go):
                    self.set_v(self.get_vmax())
                    curr_street = deepcopy(self.get_current_street())
                    track = deepcopy(self.get_track())
                    street_names = deepcopy(self.get_street_names())



                    self.set_next_p(points[index])


                    change_index = street_names.index(curr_street)
                    street_names[change_index] = street
                    self.set_street_names(street_names)

                    self.set_current_street(street)
                    self.rem_current_street = street



                    for item in track:
                        if (item['name'] == curr_street):
                            item['name'] = street
                            for i in range(len(item['coordinates'])):
                                item['coordinates'][i] = overtake[overtake_index][i]

                            break

                    self.set_track_from_track(track)



    def opposite_rl(self):
        check = deepcopy(self.get_current_street())
        split = check.split('-')
        if(split[1] == 'left'):
            text = split[0] + '-' + 'right' + '-' + split[2]
            if (split[2] == 'ccw'):
                index_number = [0, 1]  # pierwszy to ten na który zmieniamy, a drugi to na którym byliśmy
            else:
                index_number = [2, 3]
        else:
            text = split[0] + '-' + 'left' + '-' + split[2]
            if (split[2] == 'ccw'):
                index_number = [1, 0]
            else:
                index_number = [3, 2]


        return text, index_number

    def check_if_taken(self, streets, points):
        data = self.get_data()
        points_to_check = []
        for road in data:
            if road['name'] in streets:

                if road['name'] == "westerplatte-right-cw" or road['name'] == "westerplatte-left-cw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length - int((3.0/self.get_vmax())*9), -1):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "gertrudy-poczta-ccw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length- int((3/self.get_vmax()*7)), -1):
                        points_to_check.append(road['coordinates'][i])

                # staro skret
                elif road['name'] == "sienna-staro-prosto" or road['name'] == "sienna-gertrudy-skret":
                    for i in range(4):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "sienna-westerplatte-skret":
                    length = len(road['coordinates'])
                    for i in range(length-2, length-5, -1):
                        points_to_check.append(road['coordinates'][i])
                # staro skret
                elif road['name'] == "staro-sienna-prosto" or road['name'] == "staro-gertrudy-skret":
                    for i in range(5):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "staro-westerplatte-skret":
                    length = len(road['coordinates'])
                    for i in range(length - 2, length - 6, -1):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "pawia-westerplatte-prosto" or road['name'] == "pawia-basztowa-skret":
                    for i in range(5):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "basztowa-lubicz-prosto" or road['name'] == "basztowa-westerplatte-skret":
                    for i in range(2):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "basztowa-cw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length-int(3/self.get_vmax()*3), -1):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "idziego-gertrudy-skret":
                    length = len(road['coordinates'])
                    for i in range(length - 2, length - 5, -1):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "gertrudy-stradom-skret":
                    length = len(road['coordinates'])
                    for i in range(length-5):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "zwierzyniecka-strasz-skret":
                    for i in range(6):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "basztowa-dunaj-ccw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length-3):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "dunaj-podwale-prosto":
                        for i in range(4):
                            points_to_check.append(road['coordinates'][i])

                elif road['name'] == "basztowa-ccw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length-int(3/self.get_vmax()*3),-1):
                        points_to_check.append(road['coordinates'][i])

                elif road['name'] == "basztowa-dunaj-cw":
                    length = len(road['coordinates'])
                    for i in range(length-1, length-int(3/self.get_vmax()*4), -1):
                        points_to_check.append(road['coordinates'][i])

                else:
                    for pkt in road['coordinates']:
                        points_to_check.append(pkt)


                for pkt in points_to_check:

                    if pkt.get_taken():

                        if self.get_current_street() == "dluga-basztowa-cw-skret":
                            points[1660].set_taken(1)
                            break

                        if self.get_current_street() == "basztowa-dluga-cw-skret":
                            points[1667].set_taken(1)
                            break

                        if self.get_current_street() == "karmelicka-podwale-skret":
                            points[1355].set_taken(1)
                            break

                        if self.get_current_street() == "karmelicka-dunaj-skret":
                            points[1371].set_taken(1)
                            break

                        if self.get_current_street() == "franc-strasz-skret":
                            points[1399].set_taken(1)
                            break

                        if self.get_current_street() == "bernard-gertrudy-prosto":
                            points[1429].set_taken(1)
                            break

                        if self.get_current_street() == "stradom-gert-skret":
                            points[1455].set_taken(1)
                            break

                        if self.get_current_street() == "lubicz-pawia-skret":
                            points[1624].set_taken(1)
                            break

                        if self.get_current_street() == "lubicz-westerplatte-skret":
                            points[1638].set_taken(1)
                            break

                        if self.get_current_street() == "westerplatte-basztowa-skret":
                            points[1600].set_taken(1)
                            break

                        if self.get_current_street() == "sienna-westerplatte-skret":
                            points[1558].set_taken(1)
                            break

                        if self.get_current_street() == "sienna-gertrudy-skret":
                            points[1551].set_taken(1)
                            break

                        if self.get_current_street() == "staro-westerplatte-skret":
                            points[1521].set_taken(1)
                            break

                        if self.get_current_street() == "staro-gertrudy-skret":
                            points[1528].set_taken(1)
                            break

                        if self.get_current_street() == "gertrudy-poczta-ccw":
                            points[377].set_taken(1)
                            break

                        if self.get_current_street() == "westerplatte-left-cw" or self.get_current_street() == "westerplatte-right-cw":
                            points[963].set_taken(1)
                            points[848].set_taken(1)
                            break

                    else:

                        if self.get_current_street() == "dluga-basztowa-cw-skret":
                            points[1660].set_taken(0)

                        if self.get_current_street() == "basztowa-dluga-cw-skret":
                            points[1667].set_taken(0)

                        if self.get_current_street() == "karmelicka-podwale-skret":
                            points[1355].set_taken(0)

                        if self.get_current_street() == "karmelicka-dunaj-skret":
                            points[1371].set_taken(0)

                        if self.get_current_street() == "franc-strasz-skret":
                            if points[1399].get_lights() == "green":
                                points[1399].set_taken(0)

                        if self.get_current_street() == "bernard-gertrudy-prosto":
                            if points[1429].get_lights() == "green":
                                points[1429].set_taken(0)

                        if self.get_current_street() == "stradom-gert-skret":
                            if points[1455].get_lights() == "green":
                                points[1455].set_taken(0)

                        if self.get_current_street() == "lubicz-pawia-skret":
                            points[1624].set_taken(0)

                        if self.get_current_street() == "lubicz-westerplatte-skret":
                            if points[1638].get_lights() == "green":
                                points[1638].set_taken(0)

                        if self.get_current_street() == "westerplatte-basztowa-skret":
                            points[1600].set_taken(0)

                        if self.get_current_street() == "sienna-gertrudy-skret":
                            if points[1558].get_lights() == "green":
                                points[1558].set_taken(0)

                        if self.get_current_street() == "sienna-westerplatte-skret":
                            if points[1551].get_lights() == "green":
                                points[1551].set_taken(0)

                        if self.get_current_street() == "staro-westerplatte-skret":
                            if points[1521].get_lights() == "green":
                                points[1521].set_taken(0)

                        if self.get_current_street() == "staro-gertrudy-skret":
                            if points[1528].get_lights() == "green":
                                points[1528].set_taken(0)

                        if self.get_current_street() == "gertrudy-poczta-ccw":
                            if points[377].get_lights() == "green":
                                points[377].set_taken(0)

                        if self.get_current_street() == "westerplatte-left-cw" or self.get_current_street() == "westerplatte-right-cw":
                            if points[963].get_lights() == "green" or points[848].get_lights() == "green":
                                points[963].set_taken(0)
                                points[848].set_taken(0)


    def check_right_hand_rule(self, points):

        possible_ways = ["gertrudy-poczta-ccw", "westerplatte-left-cw", "westerplatte-right-cw"]
        streets = []

        # skrety z gertrudy i z wester
        if self.get_curr_p().get_index() == self.get_curr_street_l().get_index()-1 and self.get_current_street() in possible_ways:
            index = self.get_street_names().index(self.get_current_street())

            if self.get_current_street() == "gertrudy-poczta-ccw":

                if self.get_street_names()[index + 1] == "gertrudy-sienna-skret":
                    streets = ["westerplatte-sienna-skret", "westerplatte-right-cw", "westerplatte-left-cw" ]

            elif self.get_current_street() == "westerplatte-left-cw" or self.get_current_street() == "westerplatte-right-cw":

                if self.get_street_names()[index + 1] == "westerplatte-staro-skret":
                    streets = ["gertrudy-poczta-ccw", "gertrudy-staro-skret"]

        # wszystkie skrety staro
        elif self.get_current_street() == "staro-gertrudy-skret" and self.get_curr_p().get_index() == 1527 \
                or self.get_current_street() == "staro-westerplatte-skret" and self.get_curr_p().get_index() == 1520:
            streets = ["sienna-staro-prosto", "sienna-gertrudy-skret", "sienna-westerplatte-skret"]

        # wszystkie skrety sienna
        elif self.get_current_street() == "sienna-gertrudy-skret" and self.get_curr_p().get_index() == 1550 \
                or self.get_current_street() == "sienna-westerplatte-skret" and self.get_curr_p().get_index() == 1557:
            streets = ["staro-sienna-prosto", "staro-gertrudy-skret", "staro-westerplatte-skret"]

        # wszystkie skrety wester-ccw
        elif self.get_current_street() == "westerplatte-basztowa-skret" and self.get_curr_p().get_index() == 1599:
            streets = ["pawia-westerplatte-prosto", "pawia-basztowa-skret"]

        # wszystkie lubicz skret
        elif self.get_current_street() == "lubicz-westerplatte-skret" and self.get_curr_p().get_index() == 1637:
            streets = ["basztowa-lubicz-prosto", "basztowa-westerplatte-skret","basztowa-cw"]

        # stradom skret
        elif self.get_current_street() == "stradom-gert-skret" and self.get_curr_p().get_index() == 1454:
            streets = ["idziego-gertrudy-skret"]

        # bernard wyjazd
        elif self.get_current_street() == "bernard-gertrudy-prosto" and self.get_curr_p().get_index() == 1428:
            streets = ["gertrudy-stradom-skret"]

        # franc skret
        elif self.get_current_street() == "franc-strasz-skret" and self.get_curr_p().get_index() == 1398:
            streets = ["zwierzyniecka-strasz-skret"]

        # karmelica wyjazd
        elif self.get_current_street() == "karmelicka-podwale-skret" and self.get_curr_p().get_index() == 1354 \
                or self.get_current_street() == "karmelicka-dunaj-skret" and self.get_curr_p().get_index() == 1370:
            streets = ["basztowa-dunaj-ccw", "dunaj-podwale-prosto"]

        elif self.get_current_street() == "basztowa-dluga-cw-skret" and self.get_curr_p().get_index() == 1666:
            streets = ["basztowa-ccw"]

        elif self.get_current_street() == "dluga-basztowa-cw-skret" and self.get_curr_p().get_index() == 1659:
            streets = ["basztowa-ccw", "basztowa-dunaj-cw"]


        self.check_if_taken(streets, points)



    def move(self, screen, points):

        self.get_street_points()

        self.check_right_hand_rule(points)

        self.check_points_in_front(points)

        self.change_point(screen, points)

        if(self.get_v_change() == 0):
            self.accel_random()
        else:
            self.set_v_change(0)




    def change_point(self, screen, points):
        self.set_color_from_v(self.get_v())
        # petla predkosci dla danego pojazdu
        for i in range(self.__v):

            track = self.get_track()

            # ustawianie czy zajety czy nie
            points[self.get_next_p().get_index()].set_taken(1)
            if points[self.get_curr_p().get_index()].get_lights() == "green" or points[self.get_curr_p().get_index()].get_lights() == None:
                points[self.get_curr_p().get_index()].set_taken(0)

            self.set_prev_p(self.get_curr_p())
            self.set_curr_p(self.get_next_p())

            self.set_current_street(self.rem_current_street)

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
                    self.rem_current_street = dictionaries['name']
                    break

            pygame.draw.circle(screen, self.__color, self.get_curr_p().get_cords(), 3)
            pygame.draw.circle(screen, (255, 255, 255), self.get_prev_p().get_cords(), 3)

            lastRoadList = self.get_track()[len(self.get_track()) - 1]['coordinates']
            if (self.get_curr_p().get_cords() == lastRoadList[len(lastRoadList) - 1].get_cords()):
                points[self.get_prev_p().get_index()].set_taken(0)
                points[self.get_curr_p().get_index()].set_taken(0)
                points[self.get_next_p().get_index()].set_taken(0)
                pygame.draw.circle(screen, (255, 255, 255), self.get_curr_p().get_cords(), 3)
                self.track_end = 1
                global outflows

                if self.get_current_street() == "dunaj-karmelicka-skret":
                    outflows['bagatela'] += 1

                elif self.get_current_street() == "strasz-franc-skret":
                    outflows['filharmonia'] += 1

                elif self.get_current_street() == "bernard-stradom-skret"\
                        or self.get_current_street() == "gertrudy-stradom-skret"\
                        or self.get_current_street() == "idziego-stradom-prosto":
                    outflows['idziego'] += 1

                elif self.get_current_street() == "gertrudy-sienna-skret"\
                        or self.get_current_street() == "westerplatte-sienna-skret"\
                        or self.get_current_street() == "staro-sienna-prosto" \
                        or self.get_current_street() == "gertrudy-staro-skret" \
                        or self.get_current_street() == "westerplatte-staro-skret" \
                        or self.get_current_street() == "sienna-staro-prosto":
                    outflows['poczta'] += 1

                elif self.get_current_street() == "basztowa-lubicz-prosto"\
                        or self.get_current_street() == "westerplatte-lubicz-skret"\
                        or self.get_current_street() == "lubicz-pawia-skret"\
                        or self.get_current_street() == "westerplatte-pawia-prosto":
                    outflows['slowackiego'] += 1






