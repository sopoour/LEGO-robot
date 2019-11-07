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
        robot = self.getFromDef('ThymioII_1')
        robot2 = self.getFromDef('ThymioII_2')
        self.keyboard.enable(Driver.timeStep)
        self.keyboard = self.getKeyboard()

    def run(self):
        # Main loop.
        while True:
            if self.step(self.timeStep) == -1:
             break


controller = Driver()
controller.run()