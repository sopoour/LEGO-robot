from controller import Robot, Motor

TIME_STEP = 64
MAX_SPEED = 6.28    
# distance to the wall
dist = 12

# Wall following algorithm      
class Thymio (Robot):      
    def run(self):
        global TIME_STEP, MAX_SPEED, dist
        i = 500
        # get the values read by the sensor
        # sensors
        leftMotor = self.getMotor('motor.left')
        rightMotor = self.getMotor('motor.right')
        leftMotor.setPosition(float('inf'))
        rightMotor.setPosition(float('inf'))
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        
        # see functions of DistanceSensor: https://cyberbotics.com/doc/reference/distancesensor#wb_distance_sensor_enable
        # sensors
        sens0 = self.getDistanceSensor("prox.horizontal.0")
        sens1 = self.getDistanceSensor("prox.horizontal.1")
        sens2 = self.getDistanceSensor("prox.horizontal.2")
        sens3 = self.getDistanceSensor("prox.horizontal.3")
        sens4 = self.getDistanceSensor("prox.horizontal.4")
        # enable distance sensor measurements in sampling period of TIME_STEP
        sens0.enable(TIME_STEP)
        sens1.enable(TIME_STEP)
        sens2.enable(TIME_STEP)
        sens3.enable(TIME_STEP)
        sens4.enable(TIME_STEP)
        while i > 0:
            # get the values read by the sensor
            sens0_dist = sens0.getValue()
            sens1_dist = sens1.getValue()
            sens2_dist = sens2.getValue()
            sens3_dist = sens3.getValue()
            sens4_dist = sens4.getValue()
            print(sens0_dist)
            if sens0_dist > dist or sens1_dist > dist and sens2_dist > dist:
                # Turn right
                leftMotor.setVelocity(dist * 3.14159265359 / 4)
                rightMotor.setVelocity(-dist * 3.14159265359 / 4)
            
            elif sens2_dist > dist and sens3_dist > dist or sens4_dist > dist:
                # Turn left
                leftMotor.setVelocity(-dist * 3.14159265359 / 4)
                rightMotor.setVelocity(dist * 3.14159265359 / 4)
            
            else:
                leftMotor.setVelocity(0.1 * MAX_SPEED)
                rightMotor.setVelocity(0.1 * MAX_SPEED)

            i = i-1

controller = Thymio()
controller.run()