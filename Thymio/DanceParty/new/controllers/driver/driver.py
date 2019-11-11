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
This controller gives to its node the following behavior:
Listen the keyboard. According to the pressed key, send a
message through an emitter or handle the position of Robot1.
"""
import math
from controller import Supervisor


class Driver (Supervisor):
    timeStep = 128
    x = 0.1
    z = 0.3
    translation = [x, 0.0, z]
    translationField = []
    rotationField = []
    message = ''
    previous_message = ''
    checkIfClose = False
   
    def __init__(self):
        super(Driver, self).__init__()
        self.emitter = self.getEmitter('emitter')
        #self.emitter.setChannel(1)
        self.translationField.append(self.getFromDef('ThymioII_1').getField('translation'))
        self.translationField.append(self.getFromDef('ThymioII_2').getField('translation'))
        self.translationField.append(self.getFromDef('ThymioII_3').getField('translation'))
        
        self.rotationField.append(self.getFromDef('ThymioII_1').getField('rotation'))
        self.rotationField.append(self.getFromDef('ThymioII_2').getField('rotation'))
        self.rotationField.append(self.getFromDef('ThymioII_3').getField('rotation'))
        
       
        
    def com_in_range(self,x1,z1,A1,x2,z2,A2):
        dis = math.sqrt( ((x1-x2)**2)+((z1-z2)**2) ) 
        #print(dis)
        ang = (A1+A2)%2*math.pi
        #print(ang)
        if (ang > math.pi/4 and dis < 0.30):
            self.checkIfClose = True
            #print("Com"+str(dis))
            
    def sendMsg(self):
        #Send a new message through the emitter device.
        if self.message != '' and self.message != self.previous_message:
            self.previous_message = self.message
            print("My name is " + self.message)
            self.emitter.send(self.message.encode('utf-8'))
           
            
    def run(self):
        # Main loop.
        # Lets the robot know that it is close to another robot 
        while True:
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            translationValues1 = self.translationField[0].getSFVec3f()
            translationValues2 = self.translationField[1].getSFVec3f()
            translationValues3 = self.translationField[2].getSFVec3f()
            
            
            rotationValues1 = self.rotationField[0].getSFRotation()
            rotationValues2 = self.rotationField[1].getSFRotation()
            rotationValues3 = self.rotationField[2].getSFRotation()
          
            #print('ROBOT1 is located at (' + str(translationValues1[0]) + ',' + str(translationValues1[2]) + ')')
            #print('ROBOT2 is located at (' + str(translationValues2[0]) + ',' + str(translationValues2[2]) + ')')
            #print('ROBOT3 is located at (' + str(translationValues3[0]) + ',' + str(translationValues3[2]) + ')')
        
            self.com_in_range((translationValues1[0]),(translationValues1[2]),rotationValues1[3],(translationValues2[0]),(translationValues2[2]),rotationValues2[3])
            if(self.checkIfClose == True):
                #print("communicateee")
                self.checkIfClose = False
                self.message = "robot1and2"
                self.sendMsg()
            else:
                self.com_in_range((translationValues1[0]),(translationValues1[2]),rotationValues1[3],(translationValues3[0]),(translationValues3[2]),rotationValues3[3])
            if(self.checkIfClose == True):
                #print("communicateee")
                self.checkIfClose = False
                self.message = "robot1and3"
                self.sendMsg()
            else:
                self.com_in_range((translationValues2[0]),(translationValues2[2]),rotationValues2[3],(translationValues3[0]),(translationValues3[2]),rotationValues3[3])
            if(self.checkIfClose == True):
                #print("communicateee")
                self.checkIfClose = False
                self.message = "robot2and3"
                self.sendMsg()

            if self.step(self.timeStep) == -1:
                break
            

controller = Driver()
controller.run()
