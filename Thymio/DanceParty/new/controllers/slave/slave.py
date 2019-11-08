# Copyright 1996-2019 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This controller gives to its robot the following behavior:
According to the messages it receives, the robot change its
behavior.
"""

from controller import Robot, Motor
import random, time

class Enumerate(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)


class Slave (Robot):

    Mode = Enumerate('STOP MOVE_FORWARD AVOIDOBSTACLES TURN')
    timeStep = 32
    maxSpeed = 10.0
    mode = Mode.AVOIDOBSTACLES
    motors = []
    distanceSensors = []
    dist = 12
    gender = -1
    isSingle = True
    state = 0 

    def boundSpeed(self, speed):
        return max(-self.maxSpeed, min(self.maxSpeed, speed))

    def __init__(self):
        super(Slave, self).__init__()
        #Initializing motors:
        self.motors.append(self.getMotor("motor.left"))
        self.motors.append(self.getMotor("motor.right"))
        self.motors[0].setPosition(float("inf"))
        self.motors[1].setPosition(float("inf"))
        self.motors[0].setVelocity(0.0)
        self.motors[1].setVelocity(0.0)
        
        #Initializing sensors:
        self.distanceSensors.append(self.getDistanceSensor("prox.horizontal.0"))
        self.distanceSensors.append(self.getDistanceSensor("prox.horizontal.1"))
        self.distanceSensors.append(self.getDistanceSensor("prox.horizontal.2"))
        self.distanceSensors.append(self.getDistanceSensor("prox.horizontal.3"))
        self.distanceSensors.append(self.getDistanceSensor("prox.horizontal.4"))
        self.distanceSensors[0].enable(self.timeStep)
        self.distanceSensors[1].enable(self.timeStep)
        self.distanceSensors[2].enable(self.timeStep)
        self.distanceSensors[3].enable(self.timeStep)
        self.distanceSensors[4].enable(self.timeStep)
        
    #  and change their color to reﬂect their gender 
    # (blue, red) 1. The robot is shy at the moment and stays still along the wall. 
    # It timidly awaits another robot to ask it to dance.
    def benchWarmer(self, sens2_dist, sens3_dist, sens4_dist):
        #The robots randomly decide on a gender
        self.gender = random.randint(0,1)
        if(self.gender == 0):
            #self.leds.top
            print("zero", self.gender)
        else:
            #self.leds.top = 'green'
            print("one", self.gender)


    def returnToWall(self, sens2_dist, sens3_dist, sens4_dist):
        if sens2_dist > self.dist and sens3_dist > self.dist or sens4_dist > self.dist:
            self.state = 1

        else:
            self.motors[0].setVelocity(0.1 * self.maxSpeed)
            self.motors[1].setVelocity(0.1 * self.maxSpeed)
       
    def faceArena(self, sens2_dist, sens3_dist, sens4_dist):
        if sens2_dist < self.dist:
            self.state = 2
        else:
            # Todo: turn left 180
            self.motors[0].setVelocity(-self.dist * 3.14159265359 / 4)
            self.motors[1].setVelocity(self.dist * 3.14159265359 / 4)
            
    def run(self):
        while True:
            sens0_dist = self.distanceSensors[0].getValue()
            sens1_dist = self.distanceSensors[1].getValue()
            sens2_dist = self.distanceSensors[2].getValue()
            sens3_dist = self.distanceSensors[3].getValue()
            sens4_dist = self.distanceSensors[4].getValue()
            
            if(self.state == 0):
                #self.benchWarmer(sens2_dist, sens3_dist, sens4_dist)
                self.returnToWall(sens2_dist, sens3_dist, sens4_dist)
            elif(self.state == 1):
                self.faceArena(sens2_dist, sens3_dist, sens4_dist)
            elif(self.state == 2):
                print("I'm here")
                #self.faceArena(sens2_dist, sens3_dist, sens4_dist)
            


            if self.step(self.timeStep) == -1:
                break
        
        
        
controller = Slave()
controller.run()
