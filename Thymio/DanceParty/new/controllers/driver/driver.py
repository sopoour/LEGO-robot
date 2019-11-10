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

from controller import Supervisor


class Driver (Supervisor):
    timeStep = 128
    x = 0.1
    z = 0.3
    translation = [x, 0.0, z]
    translationField = []
    message = ''
    previous_message = ''
   
    def __init__(self):
        super(Driver, self).__init__()
        self.emitter = self.getEmitter('emitter')
        #self.emitter.setChannel(1)
        self.translationField.append(self.getFromDef('ThymioII_1').getField('translation'))
        self.translationField.append(self.getFromDef('ThymioII_2').getField('translation'))
        self.translationField.append(self.getFromDef('ThymioII_3').getField('translation'))
        
    def run(self):
        # Main loop.
        # Lets the robot know that it is close to another robot 
        while True:
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            self.message = 'drives' 
            translationValues1 = self.translationField[0].getSFVec3f()
            translationValues2 = self.translationField[1].getSFVec3f()
            translationValues3 = self.translationField[2].getSFVec3f()

            print('ROBOT1 is located at (' + str(translationValues1[0]) + ',' + str(translationValues1[2]) + ')')
            print('ROBOT2 is located at (' + str(translationValues2[0]) + ',' + str(translationValues2[2]) + ')')
            print('ROBOT3 is located at (' + str(translationValues3[0]) + ',' + str(translationValues3[2]) + ')')
            
            # Send a new message through the emitter device.
            if self.message != '' and self.message != self.previous_message:
                self.previous_message = self.message
                print('Driver, ' + self.message)
                self.emitter.send(self.message.encode('utf-8'))
            
            if self.step(self.timeStep) == -1:
                break
            

controller = Driver()
controller.run()
