from controller import Robot, Motor

TIME_STEP = 64

MAX_SPEED = 6.28

#distance to the wall
dist = 1200

# create the Robot instance.
robot = Robot()

#See Thymio specific Webots names: https://cyberbotics.com/doc/guide/thymio2#thymio2-wbt
#See "robot" specific functions: https://cyberbotics.com/doc/reference/robot?tab=python#getlightsensor
#Motors
leftMotor = robot.getMotor('motor.left')
rightMotor = robot.getMotor('motor.right')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

#see functions of DistanceSensor: https://cyberbotics.com/doc/reference/distancesensor#wb_distance_sensor_enable
#sensors
sens0 = robot.getDistanceSensor("prox.horizontal.0")
sens1 = robot.getDistanceSensor("prox.horizontal.1")
sens2 = robot.getDistanceSensor("prox.horizontal.2")
sens3 = robot.getDistanceSensor("prox.horizontal.3")
sens4 = robot.getDistanceSensor("prox.horizontal.4")
#enable distance sensor measurements in sampling period of TIME_STEP
sens0.enable(TIME_STEP)
sens1.enable(TIME_STEP)
sens2.enable(TIME_STEP)
sens3.enable(TIME_STEP)
sens4.enable(TIME_STEP)

#Wall following algorithm

while robot.step(TIME_STEP) != -1:
    #get the values read by the sensor
    sens0_dist = sens0.getValue()
    sens1_dist = sens1.getValue()
    sens2_dist = sens2.getValue()
    sens3_dist = sens3.getValue()
    sens4_dist = sens4.getValue()
    
    if sens0_dist > dist or sens1_dist > dist and sens2_dist > dist:
       #Turn right 
       leftMotor.setVelocity(dist*3.14159265359/4)
       rightMotor.setVelocity(-dist*3.14159265359/4)
    
    elif sens2_dist > dist and sens3_dist > dist or sens4_dist > dist:
        #Turn left
       leftMotor.setVelocity(-dist*3.14159265359/4)
       rightMotor.setVelocity(dist*3.14159265359/4)
    
    else: 
       leftMotor.setVelocity(0.1 * MAX_SPEED)
       rightMotor.setVelocity(0.1 * MAX_SPEED)