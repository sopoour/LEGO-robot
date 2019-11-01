import random

class ThymioRobot:
    def __init__(self, id, gender, startPos, sensor_front, sensor_right):
        self.id = id
        self.gender = gender
        self.startPos = startPos
        self.sensor_front = sensor_front
        self.sensor_right = sensor_right

    # Choose random gender
    ##############
    # 0 = male = blue
    # 1 = female = red
    def generateGender(self):
        random.randint(0, 1)

    def generateStartPosition(self):
        random.random()

p1 = ThymioRobot()
p1.myfunc()