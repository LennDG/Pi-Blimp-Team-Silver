import threading
import time
 
"""
The class PID ensures the zeppelin remains stable at a given height by
continually comparing the current height supplied by the distance sensor to
the goal height.
"""    
class PID(threading.Thread, object):
   
    Kp = 1.0
    Kd = 0.0
    Ki = 0.0
    BIAS = 0.0
    MAX_PID_OUTPUT = 40.0
    MAX_Ci = 50.0
    tipping_point = 50.0
    MAX_SPEED = 20.0
   
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
        self.prev_height = 0.0
        self.prev_speed = 0.0
               
        # Initialize the result variables
        self.Ci = 0
        self.Cd = 0
   
   
    """
    This methods starts the thread.
    """
    def run(self):
       
        # Set the running condition to True.
        self.stabilizing = True
       
        # Start the loop of calculating errors and adjusting the motor accordingly.
        while self.stabilizing:
           
            # Calculate the height.
            height = self.navigator.height
           
            # Set the vertical motor accordingly.
            self.navigator.motor_control.vert_motor.level = self.motor_output(height)
           
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
    def motor_output(self, height):
       
        height_error = self.navigator.goal_height - height
       
        # Calculate dt
        self.current_time = time.time()
        dt = self.current_time - self.prev_time
       
        # Determine the goal speed.
        goal_speed = 0.0
       
        if height_error > self.tipping_point:
            goal_speed = self.MAX_SPEED
        elif height_error < -1* self.tipping_point:
            goal_speed = -1*self.MAX_SPEED
        else:
            goal_speed = height_error/self.tipping_point*self.MAX_SPEED
           
       
        # Determine the current speed.
       
        # Start by determining the average speed over the interval.
        average_speed = (height - self.prev_height)/dt
       
        # We approximate the change in speed as a linear process, the current
        # speed can be calculated as follows.
        speed = 2*average_speed - self.prev_speed
       
       
        # Calculate the error we continue the work with.
        error = goal_speed - speed
             
       
#         # Rescale the error. Here I've taken 100 as 100% error.
#         if error > 100.0:
#             error = 100.0
#         elif error < -100.0:
#             error = -100.0
       
        # Calculate integral term
        self.Ci += error*dt
       
        # Check to see whether the accumulated error Ci isn't above or below the allowed boundaries
        if self.Ci > PID.MAX_Ci:
            self.Ci = PID.MAX_Ci
        elif self.Ci < -1*PID.MAX_Ci:
            self.Ci = -1*PID.MAX_Ci
       
        # Calculate the differential term, being careful not to divide by 0
        self.Cd = 0
        if dt > 0:
            self.Cd = (speed - self.prev_speed)/dt
           
        # Save the time and error for the next time the function runs
        self.prev_time = self.current_time
        self.prev_height = height
        self.prev_speed = speed
       
        # Calculate the PID value.
        PID_value = PID.Kp*error + PID.Ki*self.Ci + PID.Kd*self.Cd
       
        # Restrict the PID output so that the zeppelin will not move to fast.
        if PID_value > PID.MAX_PID_OUTPUT:
            PID_value = PID.MAX_PID_OUTPUT
        elif PID_value < -1*PID.MAX_PID_OUTPUT:
            PID_value = -1*PID.MAX_PID_OUTPUT
       
        # Add the BIAS to the result    
        output_value = PID.BIAS + PID_value
       
        return output_value