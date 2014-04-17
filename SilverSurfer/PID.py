import threading
import time

"""
The class PID ensures the zeppelin remains stable at a given height by
continually comparing the current height supplied by the distance sensor to
the goal height.
"""    
class PID(threading.Thread, object):
    
    
    
    def __init__(self, navigator):
        
        threading.Thread.__init__(self)
        
        # Initialize its parent navigator
        self.navigator = navigator
        
        # Set the running condition to False.
        self.stabilizing = False
        
        # Initialize the time parameters.
        self.current_time = time.time()
        self.prev_time = self.current_time
        
        #Initialize the previous error as 0, since there hasn't been one yet
        self.prev_error = 0.0
                
        # Initialize the result variables
        self.Ci = 0
        self.Cd = 0
        
        self.Kp = 0.8
        self.Kd = 2.5
        self.Ki = 0.0
        self.BIAS = 0.0
        self.MAX_PID_OUTPUT = 40.0
        self.MAX_Ci = 50.0
    
    
    """
    This methods starts the thread.
    """
    def run(self):
        
        # Set the running condition to True.
        self.stabilizing = True
        
        # Start the loop of calculating errors and adjusting the motor accordingly.
        while self.stabilizing:
            
            # Calculate the error.
            error =  self.navigator.goal_height - self.navigator.height
            
            # Set the vertical motor accordingly.
            self.navigator.motor_control.vert_motor.level = self.motor_output(error)
            
            # Wait until a new measurement is available
            time.sleep(0.6)
            
    """
    This method stops the thread in a controlled way.
    """    
    def stop(self):
        self.stabilizing = False
    
    
    """
    This method returns the required output of the vertical motor based on 
    the supplied error.
    """
    def motor_output(self, error):
        
        # Calculate dt
        self.current_time = time.time()
        dt = self.current_time - self.prev_time
        
        # Rescale the error. Here I've taken 100 as 100% error.
        if error > 100.0:
            error = 100.0
        elif error < -100.0:
            error = -100.0
        
        # Calculate the difference in error since last pass through the function
        de = error - self.prev_error
        
        # Calculate integral term
        self.Ci += error*dt
        
        # Check to see whether the accumulated error Ci isn't above or below the allowed boundaries
        if self.Ci > self.MAX_Ci:
            self.Ci = self.MAX_Ci
        elif self.Ci < -1*self.MAX_Ci:
            self.Ci = -1*self.MAX_Ci
        
        # Calculate the differential term, being careful not to divide by 0
        self.Cd = 0
        if dt > 0:
            self.Cd = de/dt
            
        # Save the time and error for the next time the function runs
        self.prev_time = self.current_time
        self.prev_error = error
        
        # Calculate the PID value, ensure soft landings.
        if self.navigator.height < 50 and self.navigator.goal_height == 0:
            self.Kp = self.Kp/2.0
            self.Ci = 0
        elif self.navigator.height < 20 and self.navigator.goal_height == 0:
            self.Kp = 0
            self.Cd = 0
            self.navigator.flying = False
        PID_value = self.Kp*error + self.Ki*self.Ci + self.Kd*self.Cd
        
        # Restrict the PID output so that the zeppelin will not move to fast.
        if PID_value > self.MAX_PID_OUTPUT:
            PID_value = self.MAX_PID_OUTPUT
        elif PID_value < -1*self.MAX_PID_OUTPUT:
            PID_value = -1*self.MAX_PID_OUTPUT
        
        # Add the BIAS to the result    
        output_value = self.BIAS + PID_value
        
        return output_value