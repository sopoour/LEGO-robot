import numpy as np
from numpy import sin, cos, pi, sqrt
from shapely.geometry import LinearRing, LineString, Point, Polygon



class Robot:
    sides = 3.03  # meters
    RadiosRobot = 0.1

    robot_timestep = 0.1  # 1/robot_timestep equals update frequency of robot
    simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

    world = LinearRing([(0, 0), (sides, 0), (sides / 2, (sin(pi / 3) * sides / 2 / sin(pi / 6)), (0, 0))])

    R = 0.02  # radius of wheels in meters
    L = 0.094  # distance between wheels in meters

    lidararrayP = []
    lidararrayD = []

    def __init__(self,x,y,q):
        self.x = x
        self.y = y
        self.q = q

    def get_con(self):
        return (self.x ,self.y)

    def get_orientation(self):
        return self.q

    #Wall following
    def UpAction(self):
        if self.distance_sensor_front> 0.40 and self.distance_sensor_left>0.70:
            self.action=2
        elif self.distance_sensor_front< 0.40 or self.distance_sensor_left<0.40:
                self.action=0
        else: self.action=2



    def move(self,action):

        if action == 0:
            left_wheel_velocity = -self.L * pi / 4
            right_wheel_velocity = self.L * pi / 4
        elif action == 1:
            left_wheel_velocity = self.L * pi / 4
            right_wheel_velocity = -self.L * pi / 4
        else:
            left_wheel_velocity = 10 / (2 * pi)
            right_wheel_velocity = 10 / (2 * pi)

        for step in range(int(self.robot_timestep / self.simulation_timestep)):  # step model time/timestep times
            v_x = cos(self.q) * (self.R * left_wheel_velocity / 2 + self.R * right_wheel_velocity / 2)
            v_y = sin(self.q) * (self.R * left_wheel_velocity / 2 + self.R * right_wheel_velocity / 2)
            omega = self.R * left_wheel_velocity / self.L - self.R * right_wheel_velocity / self.L

            self.x += v_x * self.simulation_timestep
            self.y += v_y * self.simulation_timestep
            self.q += omega * self.simulation_timestep



    def sensorIR(self):
        ray_sensor_front = LineString([(self.x, self.y), (
            self.x + cos( self.q) * 2 *self.sides ,  self.y + sin( self.q) * 2 * self.sides)])  # a line from robot to a point outside arena in direction of q

        ray_sensor_left = LineString([(self.x, self.y), (self.x + cos(self.q + (pi / 3)) * 2 * self.sides, self.y + sin(
            self.q + (pi / 3)) * 2 * self.sides)])  # a line from robot to a point outside arena in direction of q

        self.sensor_front = self.world.intersection(ray_sensor_front)
        self.sensor_left = self.world.intersection(ray_sensor_left)

        self.distance_sensor_front = sqrt((self.sensor_front.x - self.x) ** 2 + (self.sensor_front.y -self.y) ** 2) - self.L / 2
        self.distance_sensor_left =sqrt((self.sensor_left.x - self.x) ** 2 + (self.sensor_left.y - self.y) ** 2) - self.L / 2


    def lidar(self):
        i=1
        grader=0
        self.lidararrayP=[]
        self.lidararrayD = []
        while i < 360/10:
            grader=pi/180 +grader*10
            point= self.world.intersection( LineString([(self.x, self.y), (self.x + cos(self.q + (grader)) * 2 * self.sides, self.y + sin(self.q + (grader)) * 2 * self.sides)]))
            self.lidararrayP.append(point)
            self.lidararrayD.append((point.x - self.x) ** 2 + (point.y - self.y) ** 2- self.L / 2)
            i=i+1


    def camera(self):
        poly = Polygon(((self.x, self.y), (self.y, (self.x + cos(self.q-pi/6) * 2 *self.sides ), (1, 1), (1, 0))))
        poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))

    def updat(self):
        self.lidar()
        self.sensorIR()
        self.UpAction()
        self.move(self.action)
       # print(self.q)





