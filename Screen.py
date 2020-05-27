import pygame
from Point import Point
from fetchPointsFromFile import *
from Car import Car
from InterfaceStuff import pause

def initializePoints(points):
    for i in range(len(points)):
        pygame.draw.circle(screen, white, points[i].getCords(), 3)


resolution = (1800,900)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)

# fetching essential data from json
data, points = ChangePointsFromFloatToInt("roads.json")
points = removeDuplicates(points)



# set track to car
streets = ["bagatela-filharmonia-ccw",
           "strasz-strasz-prosto",
           "filharmonia-gertrudy-ccw",
            "idziego-gertrudy-skret",
           "gertrudy-poczta-ccw",
            "gertrudy-westerplatte-prosto",
           "westerplatte-right-ccw",
            "westerplatte-basztowa-skret",
           "basztowa-ccw",
            "basztowa-ccw-basztowa-prosto",
           "basztowa-dunaj-ccw",
            "dunaj-podwale-prosto",
           ]

streets2 = [
           "filharmonia-gertrudy-ccw",
            "idziego-gertrudy-skret",
           "gertrudy-poczta-ccw",
            "gertrudy-westerplatte-prosto",
           "westerplatte-right-ccw",
            "westerplatte-basztowa-skret",
           "basztowa-ccw",
            "basztowa-ccw-basztowa-prosto",
           "basztowa-dunaj-ccw",
            "dunaj-podwale-prosto",
            "bagatela-filharmonia-ccw",
           "strasz-strasz-prosto",
           ]
streets3 = [
            "basztowa-dunaj-ccw",
            "dunaj-podwale-prosto",
            "bagatela-filharmonia-ccw",
           "strasz-strasz-prosto",
           "filharmonia-gertrudy-ccw",
            "idziego-gertrudy-skret",
           "gertrudy-poczta-ccw",
            "gertrudy-westerplatte-prosto",
           "westerplatte-right-ccw",
            "westerplatte-basztowa-skret",
           "basztowa-ccw",
            "basztowa-ccw-basztowa-prosto",
           ]

car = Car(streets, data, (255, 0, 0), 2)

car2 = Car(streets2, data, (255, 0, 0), 1)

car3 = Car(streets3, data, (255, 0, 0), 3)

# initialize
pygame.init()

# create screen
screen = pygame.display.set_mode(resolution)

#running condition and title
running = True
pygame.display.set_caption("Cracow Road Simulation")

# time delay
clockobject = pygame.time.Clock()

# background color
screen.fill(black)

# draw road
initializePoints(points)

#Pause message
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('To Pause press P To Continue press C', True, green)
textRect = text.get_rect()
textRect.center = (resolution[0] // 2, resolution[1] // 2)
screen.blit(text, textRect)


#Main Loop
while running:

    clockobject.tick(20)

    occupied = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause(clockobject)
                print("siema")




    car.move(screen, points)
    #car2.move(screen, points)
    car3.move(screen, points)


    #taktyczna petla do sprawdzania ile w globalnej liscie points jest zajetych puntkow
    # for i in range(len(points)):
    #     if (points[i].getTaken() == 1):
    #         occupied += 1
    # print(occupied)


    pygame.display.update()

    pass


