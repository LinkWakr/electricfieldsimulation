import pygame
import math

WIDTH = 1920
HEIGHT = 1080

SCALE = 40
PADDING = int(SCALE/2)

currentCharge = 0

def electricField(q, x1, y1, x2, y2):

    angle = math.atan2(y2 - y1, x2 - x1)
    if ((x2 - x1) == 0 and (y2 - y1) == 0):        
        return [0, 0]
    else:
        magnitude = -1000*q/(pow((x2 - x1), 2) + pow((y2 - y1), 2))
        return [magnitude*(math.cos(angle)), magnitude*(math.sin(angle))]


class ElectricCharge:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        if charge > 0:
            self.chargeColor = "red"
        elif charge < 0:
            self.chargeColor = "blue"
        else:
            self.chargeColor = "white"
        # self.chargeColor = pygame.Color(127 + red, 0, 127 + charge)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calcElectricField(self):
        totalElectricField = [0, 0]

        for charge in chargePlane:
            ef = electricField(charge.charge, self.x, self.y, charge.x, charge.y)

            totalElectricField[0] = totalElectricField[0] + ef[0]
            totalElectricField[1] = totalElectricField[1] + ef[1]

        if (abs(totalElectricField[0]) < 0.5 and abs(totalElectricField[1]) < 0.5):
            totalElectricField = [0, 0]
        
        return totalElectricField


planeHeight = int(math.ceil(HEIGHT/SCALE))
planeWidth = int(math.ceil(WIDTH/SCALE))

plane = []

for y in range(planeHeight):
    row = []
    for x in range(planeWidth):
        point = Point(x*SCALE + PADDING, y*SCALE + PADDING)
        row.append(point)
    plane.append(row)

chargePlane = []

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                chargePlane = []
        if event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1):
                chargePlane.append(ElectricCharge(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], currentCharge))
            elif (event.button == 3):
                currentCharge = 0
            elif (event.button == 4):
                currentCharge += 1
            elif (event.button == 5):
                currentCharge -= 1


    screen.fill("black")

    chargePlane.append(ElectricCharge(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], currentCharge))

    for row in plane:
        for point in row:
            pointElectricField = point.calcElectricField()
            electricFieldMagnitude = math.sqrt(math.pow(pointElectricField[0], 2) + math.pow(pointElectricField[1], 2))
            factor = -2 + SCALE/2

            if (pointElectricField != [0, 0]):
                electricFieldAngle = math.atan2(pointElectricField[1], pointElectricField[0])
                pygame.draw.line(screen, "white", (point.x, point.y), (point.x + int(factor*math.cos(electricFieldAngle)), point.y + int(factor*math.sin(electricFieldAngle))), 3)
            else:
                pygame.draw.circle(screen, "white", (point.x, point.y), 3)

    for charge in chargePlane:
        if charge.charge != 0:
            pygame.draw.circle(screen, charge.chargeColor, (charge.x, charge.y), 40)
    
    chargePlane.pop()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()