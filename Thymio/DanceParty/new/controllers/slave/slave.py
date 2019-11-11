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
            self.name = name


class Slave (Robot):
    timeStep = 64
    Mode = Enumerate('STOP MOVE_FORWARD AVOIDOBSTACLES TURN')
    maxSpeed = 10.0
    mode = Mode.AVOIDOBSTACLES
    motors = []
    distanceSensors = []
    led = 0
    dist = 8
    gender = -1
    isSingle = True
    state = 0 
    weight = -1
    sens0_dist = -1
    sens1_dist = -1
    sens2_dist = -1
    sens3_dist = -1
    sens4_dist = -1
    checksIfEnoughCourage = -1
    message = ''
    previous_message = ''
    activeCommunication = False
    counter = 0
    tempCounter = 0
    #name = []

   

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
        
        #Enable sensors:
        self.distanceSensors[0].enable(self.timeStep)
        self.distanceSensors[1].enable(self.timeStep)
        self.distanceSensors[2].enable(self.timeStep)
        self.distanceSensors[3].enable(self.timeStep)
        self.distanceSensors[4].enable(self.timeStep)
        #self.LED.getLED("leds.top")
        
        #Initializing receiver:
        self.receiver = self.getReceiver('receiver')
        self.receiver.enable(self.timeStep)
        #Initializing emitter:
        self.emitter = self.getEmitter('emitter')
        
        #self.name = self.getName.split("0x",1)
       

        
    #  and change their color to reﬂect their gender 
    # (blue, red) 1. The robot is shy at the moment and stays still along the wall. 
    # It timidly awaits another robot to ask it to dance.
    def benchWarmer(self):
        #The robots randomly decide on a gender
        self.gender = random.randint(1,2)
        if(self.gender == 1):
            #self.LED.set(self, R0G0B32)
            print("male", self.gender)
        else:
            #self.LED.set(self, R32G0B0)
            print("female", self.gender)
        
        #Activate receiving communication
        self.activeCommunication = True
      
        #Missing: prox.comm.enable & timer=100ms
        self.state = 1  
    
    def findDancePartner(self):
        self.checksIfEnoughCourage = random.randint(1,1000)
        #print("courage: ", self.checksIfEnoughCourage)
        
    def wallFollowing(self):
        #print("wallFollowing")
        
        # Turn left
        #print("sensor is noooooooooooow: ", self.sens2_dist)
        if self.sens2_dist > self.dist and self.sens3_dist > self.dist or self.sens4_dist > self.dist:
            print("sens2 ", self.sens2_dist)
            print("sens4 ", self.sens4_dist)
            self.motors[0].setVelocity(-self.dist * 3.14159265359 / 4)
            self.motors[1].setVelocity(self.dist * 3.14159265359 / 4)

        else:
            self.motors[0].setVelocity(0.1 * self.maxSpeed)
            self.motors[1].setVelocity(0.1 * self.maxSpeed)

        
    def pairing(self):
        print("pairing")
        # Send a new message through the emitter device.
        self.message = 'dance?' 
        if self.message != '' and self.message != self.previous_message:
            self.previous_message = self.message
            #print('doooooooooooooooooooooooooooooooooooooooooooooo, ' + self.message)
            self.emitter.send(self.message.encode('utf-8'))
    
    def matching(self):
        print("mathcing")
        
    def moveToCenter(self):
        print("move to center")
   
    def dance(self):
        print("dance")
             
    
    def returnToRest(self):
        if self.sens2_dist > self.dist and self.sens3_dist > self.dist or self.sens4_dist > self.dist:
            self.state = 7

        else:
            self.motors[0].setVelocity(0.1 * self.maxSpeed)
            self.motors[1].setVelocity(0.1 * self.maxSpeed)
       
    def faceArena(self):
        if self.sens2_dist < self.dist and self.sens4_dist < self.dist:
            self.state = 8
        else:
            # Todo: turn left 180
            self.motors[0].setVelocity(-self.dist * 3.14159265359 / 4)
            self.motors[1].setVelocity(self.dist * 3.14159265359 / 4)
            
    
    def getSensorValues(self):
        self.sens0_dist = self.distanceSensors[0].getValue()
        self.sens1_dist = self.distanceSensors[1].getValue()
        self.sens2_dist = self.distanceSensors[2].getValue()
        self.sens3_dist = self.distanceSensors[3].getValue()
        self.sens4_dist = self.distanceSensors[4].getValue()
        
        
    def run(self):
        while True:
            #print("name is", self.name)
            self.getSensorValues()
            print("sens2 ", self.sens2_dist)
            print("sens4 ", self.sens4_dist)
            #Check if we received invitation to dance, then dance
            if self.activeCommunication == True:
                if self.receiver.getQueueLength() > 0:
                    message = self.receiver.getData().decode('utf-8')
                    self.receiver.nextPacket()
                    print('I should ' + message + '!')
                    self.dance()
                    self.state = 6
            
            #Wall following
            if(self.checksIfEnoughCourage == 2):
                #print("wall following"')
                if(self.tempCounter < 30000):
                    print("Temp counter: ", self.tempCounter)
                    self.wallFollowing()   
                else:
                    self.state = 1
                    self.motors[0].setVelocity(0.0)
                    self.motors[1].setVelocity(0.0)
                    self.checkIfEnoughCourage = -1
                self.tempCounter = self.tempCounter + 1            
            
            #Benchwarmer
            elif(self.state == 0):
                #print("state: ", self.state)
                self.benchWarmer()              
            #Find dance partner
            elif(self.state == 1):
                #print("state: ", self.state)
                self.findDancePartner()                 
            #Pairing
            elif(self.state == 2):
                #print("state: ", self.state)
                self.pairing()
                self.state = 3
            #Match
            elif(self.state == 3): 
                #print("state: ", self.state)
                self.state = 4
            #MoveToCenter
            elif(self.state == 4): 
                #print("state: ", self.state)
                self.state = 5
            #Dance
            elif(self.state == 5): 
                #print("state: ", self.state)
                self.state = 6  
            #Return to rest 
            elif(self.state == 6): 
                #print("state: ", self.state)
                self.state = 7
            #Repeat from Find dance partner    
            elif(self.state == 7): 
                #print("state: ", self.state)           
                self.state = 1
             
                             
            #print("state: ", self.state)
            
            self.counter = self.counter + 1
            
            if self.step(self.timeStep) == -1:
                break

        
        
        
controller = Slave()
controller.run()
