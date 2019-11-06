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
    timeStep = 64
    x = 0.1
    z = 0.3
    translation = [x, 0.0, z]

    def __init__(self):
        super(Driver, self).__init__()
        self.emitter = self.getEmitter('emitter')
        robot = self.getFromDef('ThymioII')
        #robot2 = self.getFromDef('ThymioII_2')
        self.translationField = robot.getField('translation')
        #self.translationField2 = robot2.getField('translation')
        #self.keyboard.enable(Driver.timeStep)
       

    def run(self):
        # Main loop.
        message = 'hi'
        while True:
            #self.emitter.send(message.encode('utf-8'))
            # Deal with the pressed keyboard key.
            #translationValues = self.translationField.getSFVec3f()
            #print('ROBOT1 is located at (' + str(translationValues[0]) + ',' + str(translationValues[2]) + ')')
            #translationValues2 = self.translationField2.getSFVec3f()
            #print('ROBOT12 is located at (' + str(translationValues2[0]) + ',' + str(translationValues2[2]) + ')')
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break

    def displayHelp(self):
        print(
            'Commands:\n'
            ' I for displaying the commands\n'
            ' A for avoid obstacles\n'
            ' F for move forward\n'
            ' S for stop\n'
            ' T for turn\n'
            ' R for positioning ROBOT1 at (0.1,0.3)\n'
            ' G for knowing the (x,z) position of ROBOT1'
        )


controller = Driver()
controller.run()
