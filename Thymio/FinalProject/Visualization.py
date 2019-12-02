# visolis
import pygame
from pymunk import Vec2d

import robot
from numpy import sin, cos, pi, sqrt

import numpy as np

import pymunk


class Visualization:
    white = ((255, 255, 255))
    blue = ((0, 0, 255))
    green = ((0, 255, 0))
    red = ((255, 0, 0))
    black = ((0, 0, 0))
    orange = ((255, 100, 10))
    yellow = ((255, 255, 0))
    blue_green = ((0, 255, 170))
    marroon = ((115, 0, 0))
    lime = ((180, 255, 100))
    pink = ((255, 100, 180))
    purple = ((240, 0, 255))
    gray = ((127, 127, 127))
    magenta = ((255, 0, 230))
    brown = ((100, 40, 0))
    forest_green = ((0, 50, 0))
    navy_blue = ((0, 0, 100))
    rust = ((210, 150, 75))
    dandilion_yellow = ((255, 200, 0))
    highlighter = ((255, 255, 100))
    sky_blue = ((0, 255, 255))
    light_gray = ((200, 200, 200))
    dark_gray = ((50, 50, 50))
    tan = ((230, 220, 170))
    coffee_brown = ((200, 190, 140))
    moon_glow = ((235, 245, 255))

    sides = 3.03  # meters

    robotcoler = [(255,0,0),(0,255,0),(0,0,255)]
    rede = (255, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)

    screenSize = 800
    cant = (screenSize * 0.05)
    scalingcor = (screenSize - cant * 2) / 3


    width = 40
    height = 60

    R = 0.02  # radius of wheels in meters
    L = 0.094  # distance between wheels in meters


    def __init__(self,robots):
        pygame.init()
        self.win = pygame.display.set_mode((self.screenSize, self.screenSize))
        pygame.display.set_caption("Simolation")
        self.robots =robots
        self.visLoop()


    def scaling(self,x, y):
        y = self.sides - y
        return int(x * self.scalingcor + self.cant), int(y * self.scalingcor + self.cant)

    def converter(self,m):
        return int(self.scalingcor*m)

    def visLoop(self):
        run = True
        while run:
            pygame.time.delay(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


            #wolde
            self.win.fill(self.white)  # Fills the screen with black

            pygame.draw.lines(self.win, self.gray, True, [(self.scaling(0, 0)), (self.scaling(3, 0)),
                                                           (self.scaling(self.sides / 2, (
                                                                   sin(pi / 3) * self.sides / 2 / sin(pi / 6))))], 4)

            pygame.draw.circle(self.win, self.green, (self.scaling(-0.1,-0.1)), self.converter(0.1))
            pygame.draw.circle(self.win, self.blue, (self.scaling(3.1,-0.1)), self.converter(0.1))
            pygame.draw.circle(self.win, self.rede, ((self.scaling(self.sides / 2, (
                                                                   sin(pi / 3) * self.sides / 2 / sin(pi / 6))+0.1))), self.converter(0.1))

            i=0
            for robot in self.robots:
                robot.updat()
                x,y=robot.get_con()

                pygame.draw.circle(self.win,self.robotcoler[i], (self.scaling(x,y)),self.converter(robot.L/2))
                pygame.draw.line(self.win, self.black, (self.scaling(x, y)), (self.scaling(x+robot.L/2*cos(robot.q), y+robot.L/2*sin(robot.q))), 2)


                # PLOT IR SENSOR
                pygame.draw.circle(self.win,self.robotcoler[i], (self.scaling(robot.sensor_front.x,robot.sensor_front.y)),5)
                pygame.draw.circle(self.win, self.robotcoler[i],
                                   (self.scaling(robot.sensor_left.x, robot.sensor_left.y)), 5)

                # PLOT LIDRA AS POINT
                for lidra in robot.lidararrayP:
                    pygame.draw.circle(self.win, self.robotcoler[i],
                                       (self.scaling(lidra.x, lidra.y)), 5)
                     #PLOT LIDRA AS LEINS
                    pygame.draw.line(self.win, self.black, (self.scaling(x, y)),
                                     (self.scaling(lidra.x,lidra.y)), 2)

                i = i + 1


            # pygame.draw.rect(win, (255, 0, 0), (a, b, width, height))
            # pygame.draw.circle(win,(255, 0, 0),(a,b,),10,2)

            pygame.display.update()



        pygame.quit()

if __name__ == '__main__':
    r1=robot.Robot(1, 1, 0)
    r2=robot.Robot(1.5,1.4, 0)
    li = [r1,r2]
   # print(li[0].get_con())
    Visualization(li)
