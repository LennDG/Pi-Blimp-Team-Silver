#This is the file for the ZeppelinControl
import MotorControl, time, threading

class ZeppelinControl():
    
    def __init__(self, distance_sensor):
        
        self.motor_control = MotorControl.MotorControl()
        self.current_height = 0.0
        self.goal_height = 0.0
        self.PID = PID(self, Kp = 0.8, Kd = 2.5, Ki =0.0)
        self.bias = 0
        self.distance_sensor = distance_sensor
    
    @property
    def current_heigth(self):
        return self.distance_sensor.height
    
    def stabilize(self):
        self.PID.PID_On = True
        self.PID.start()
    
    def end_stabilize(self):
        self.PID.PID_On = False
    
    def move(self, direction):
        #1 for forward, -1 for backward
        print ("moving to forward " + str(direction))
        self.motor_control.move(direction)
    
    def turn(self, direction):
        #1 for left, -1 for right
        print ("turning to " + str(direction))
        self.motor_control.turn(direction)
        
    def vert_move(self, level):
        #Sets the vertical motor to a level, mostly used for testing purposes
        print ("Setting the vertical motor to " + str(level))
        self.motor_control.vert_motor.level = level
    
    def hor_stop(self): 
        #stops all horizontal movement (includes turning)
        print ("Horizontal stop")
        self.motor_control.stop()
    
    def vert_stop(self):
        #Sets the goal height at the current height, effectively stopping the zeppelin vertical movement
        self.goal_height = self.current_height
        
    def shutoff(self):
        #Stops all the engines, CAUTION: THIS WILL CAUSE ZEPPELIN CRASH
        self.motor_control.all_off()
        
    #This method calibrates the basis parameter by moving the zeppelin up and d$
    def calibrate(self):
        self.bias = 0
        while(not  self.isRising()):
            self.bias = self.bias + 1
            self.motor_control.vert_motor.level = self.bias
            print (self.bias)
    print "calibration finished"

    #Returns if the zeppelin is gaining altitude.
    def isRising(self):
        height = self.current_height
        print ("height :" + str(height))
        time.sleep(0.7)
        return height > 6
        

            
class PID(threading.Thread, object):
    #This is the PID object used for stabilizing the zeppelin
    
    def __init__(self, control, Kp = 1.0, Kd = 0.0, Ki =0.0): #These are values for now, will change. Experimental determination.
        threading.Thread.__init__(self)
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        
        self.control = control
        
        self.PID_On = False
        
        self.setup()
    @property
    def goal_height(self):
        return self.control.goal_height
    
    @property
    def current_height(self):
        return self.control.current_height
    
    @property
    def Kp(self):
        return self._Kp
    
    @Kp.setter
    def Kp(self, value):
        self._Kp = value
        
    @property
    def Kd(self):
        return self._Kd
    
    @Kd.setter
    def Kd(self, value):
        self._Kd = value
        
    @property
    def Ki(self):
        return self._Ki
    
    @Ki.setter
    def Ki(self, value):
        self._Ki = value
    
    def run(self):
        self.setup()
        while True and self.PID_On:
            error =  self.goal_height - self.current_height
            motor_level = self.PID(error)
            self.control.motor_control.vert_motor.level = motor_level
            time.sleep(0.6) #this is the time necessary for a new height
        
    def setup(self):
        self.current_time = time.time()
        self.prev_time = self.current_time
        
        #Initialize the previous error as 0, since there hasn't been one yet
        self.prev_error = 0.0
                
        #Make result variables zero, sort of a reset
        self.Ci = 0
        self.Cd = 0
        
        #Init max and min Ci values
        self.max_Ci = 50
        self.min_Ci = -50
    
    #The calculating part
    def PID(self, error):
        #This is the entire implementation. Parameters will be found through testing
        
        #Calculate dt
        self.current_time = time.time()
        dt = self.current_time - self.prev_time
        
        #Rescale the error. Here I've taken 100 as 100% error.
        if error > 100.0:
            error = 100.0
        elif error < -100.0:
            error = -100.0
        
        #Calculate the difference in error since last pass through the function
        de = error - self.prev_error
        
        #Calculate integral term
        self.Ci += error*dt
        
        #Check to see whether the accumulated error Ci isn't above or below the max and min values of it
        #This is to prevent integral windup
        if self.Ci > self.max_Ci:
            self.Ci = self.max_Ci
        elif self.Ci < self.min_Ci:
            self.Ci = self.min_Ci
        
        #Calculate the differential term, being careful not to divide by 0
        self.Cd = 0
        if dt > 0:
            self.Cd = de/dt
            
        #Save the time and error for the next time the function runs
        self.prev_time = self.current_time
        self.prev_error = error
        
        #Calculate the PID value
        #Because of the rescale, this can just be added to the bias
        PID = self.Kp*error + self.Ki*self.Ci + self.Kd*self.Cd
        
        #Set the output value to the appropriate scale
        if PID > 40.0:
            PID = 40.0
        elif PID < -40.0:
            PID = -40.0
            
        output_value = self.control.bias + PID
        
        return output_value