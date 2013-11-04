'''
Created on 4-nov.-2013

@author: Lily
'''
#This is the file for the Motor Control class.
import Motor, time

class MotorControl():
    
    def __init__(self, basis):
        
        self.left_motor = Motor.Motor(cw_pin = 4, ccw_pin = 24, enabler = 14) #14 and 15 are next to 18 on BCM
        self.right_motor = Motor.Motor(cw_pin = 17, ccw_pin = 23, enabler = 15)
        self.vert_motor = Motor.VerticalMotor(cw_pin = 7, ccw_pin = 9,enabler = 18)
        #self.distance_sensor = DistanceSensor.DistanceSensor()
        
        self.basis = basis
    
    # This method will make the zeppelin move forward or backward, depending on the direction.
    # direction    1 to move forward
    #              -1 to move backward
    def leftTest(self, direction):
        now = time.time()
        future = now + 5
        self.left_motor.disable()
        self.left_motor.direction = direction
        self.left_motor.enable()
        print "Left motor is testing for 5 seconds"
        if time.time() > future:
            self.left_motor.disable()
            print "Left motor has completed testing"
            
    def rightTest(self, direction):
        now = time.time()
        future = now + 5
        self.right_motor.disable()
        self.right_motor.direction = direction
        self.right_motor.enable()
        print "Right motor is testing for 5 seconds"
        if time.time() > future:
            self.right_motor.disable()
            print "Right motor has completed testing"
        
    def updownTest(self, direction):
        now = time.time()
        future = now + 10
        halfway = now + 5
        self.vert_motor.disable()
        self.vert_motor.direction = direction
        self.vert_motor.enable()
        print "Vertical motor is testing for 10 seconds, speed should increase and decrease gradually"
        #test hier nog wat er gebeurt als we onder/over max/min toerental gaan
        while time.time() < halfway:
            time.sleep(1)
            print "Increasing by 0.2"
            self.vert_motor.level += self.vert_motor.direction*0.2
        while (time.time() > halfway) and (time.time() < future) :
            time.sleep(1)
            print "Decreasing by 0.2"
            self.vert_motor.level -= self.vert_motor.direction*0.2
        if time.time() > future:
            self.vert_motor.disable()
            print "Vertical motor has completed testing"
            
    def move(self, direction):
        self.left_motor.disable()
        self.right_motor.disable()
        
        self.left_motor.direction = direction
        self.right_motor.direction = direction
        
        self.left_motor.enable()
        self.right_motor.enable()
        
    def turn(self, angle):
        
        self.left_motor.disable() #"reset" the motors
        self.right_motor.disable()
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        seconds = a*angle + b  #seconds is a function of angle
        
        #Calculate direction here (rechterhandregel yo)
        if angle >= 0:
            self.left_motor.direction = -1
            self.right_motor.direction = 1
        else:
            self.left_motor.direction = 1
            self.right_motor.direction = -1
        
        #motors start, turning begins.
        self.left_motor.enable()
        self.right_motor.enable() 
        
        #turning continues for the amount of secons calculated previously.
        time.sleep(seconds) #Seconden!
        
        #turning stops, motors disabled
        self.left_motor.disable()
        self.right_motor.disable()

#This method calibrates the basis parameter by moving the zeppelin up and down untill it stabilises around a random height        
#def calibrate(self, increment):
 #   if self.isRising():
  #      self.vert_motor.direction = -1
   # else:
    #    self.vert_motor.direction =  1
    #self.subCalibrate(increment)
    #self.basis = self.vert_motor.level

#def subCalibrate(self, increment, depth):
 #   if self.isRising():
  #      while self.isRising():
   #         self.vert_motor.level -= self.vert_motor.direction*increment
    #else:
     #   while not self.isRising():
      #      self.vert_motor.level += self.vert_motor.direction*increment
   # subCalibrate(increment/2, depth-1)

#Returns if the zeppelin is gaining altitude.
#def isRising(self):
 #   height1 = self.distance_sensor.getHeight()
  #  time.sleep(0.5)
   # height2 = self.distance_sensor.getHeight()
    #return height2 - height1 > 0
        
#def stabilize(self, height):
 #   error =  self.distance_sensor.height - height
            
  #  b = 1 # b is a parameter that has yet to be defined through testing
            
        
   # level = b*error*abs(error) + self.basis
        
    # Set the right direction for the vertical motor
    #if level < 0:
     #   self.vert_motor.direction = -1
    #else:
     #   self.vert_motor.direction = 1
            
            
def stop(self):#Maybe needs to spin engines in other directions based on speed. For now, just disable them
    self.LeftMotor.disable()
    self.RightMotor.disable()