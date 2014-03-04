from Vector import Vector
import MotorControl
import threading
import time

'''
This file contains the class Navigator.

@author: Rob
@Version: 1.0
'''

MAXIMUM_SPEED = 1
SLOW_DOWN_DISTANCE = 1.5

'''
    This class keeps track of the position and physical direction of the zeppelin.
    It also contains the map of the playfield and other useful information in
    regards to the position such as velocity, closest node etc.
'''
class Navigator(object):
    

    '''
    This constructor initializes the object with a distance sensor and the node at which the zeppelin
    starts.
    '''
    def __init__(self, distance_sensor, starting_node):
        
        self.motor_control = MotorControl.MotorControl()
        self.distance_sensor = distance_sensor
        self.closest_node = starting_node
        self.goal_position = Vector(1, -1)
        self.angle = 0
        self.angular_velocity = 0 # Testing purposes only.
        self.position = Vector(0,0)
        self.velocity = Vector(0,0)
        self.last_updated = 0
        self.flying = False
        self.goal_height = 0.0
        self.PID = PID(self, Kp = 0.8, Kd = 2.5, Ki =0.0)
    
    """
    This method updates all the properties of the zeppelin, based on the supplied information.
    """
    def update(self, node_1, node_image_1, node_2, node_image_2, zeppelin_image, time):
        time_lapsed = float(time - self.last_updated)
        self.last_updated = time
        node_difference = node_2.position - node_1.position
        node_image_1 = Vector(node_image_1[0], node_image_1[1])
        node_image_2 = Vector(node_image_2[0], node_image_2[1])
        zeppelin_image = Vector(zeppelin_image[0], zeppelin_image[1])
        image_difference = node_image_2 - node_image_1
        
        new_angle = (image_difference - node_difference).angle
        self.angular_velocity = (self.angle - new_angle)/time_lapsed
        self.angle = new_angle
        
        enlargement_factor = float(node_difference.norm/image_difference.norm)
        relative_position = zeppelin_image - node_image_1
        relative_position = relative_position/enlargement_factor
        relative_position = relative_position.turn(- new_angle)
        new_position = node_1.position + relative_position
        self.velocity = (new_position - self.position)/time_lapsed
        self.position = new_position
        
        self.closest_node = node_1
        
    def calculate_goal_velocity(self):
        
        path = self.goal_position - self.position
        goal_velocity = 0
        
        if path.norm() >= SLOW_DOWN_DISTANCE:
            goal_velocity = Vector(MAXIMUM_SPEED,0).turn(path.angle())
        else:
            goal_velocity = Vector(path.norm()/SLOW_DOWN_DISTANCE).turn(path.angle())
            
        return goal_velocity
            
        
    def update_motors(self):
        
        goal_velocity = self.calculate_goal_velocity
        velocity = goal_velocity - self.velocity
        
        scaling_factor = 100/MAXIMUM_SPEED
        acceleration = Vector(velocity.xcoord*scaling_factor, velocity.ycoord*scaling_factor)
        
        # The angle with which the zeppelin moves is the angle the acceleration makes with the x-axis
        # added to the angle the front of the zeppelin makes with the x-axis.
        self.motor_control.move(acceleration.angle + self.angle, acceleration.norm())
        
    def lift_off(self):
        self.goal_height = 1.5
        self.PID.PID_On = True
        self.PID.start()
        
    def land(self):
        self.goal_height = 0.0
        while self.height > 0.3:
            pass
        self.PID.PID_On = False
        self.motor_control.all_off()
        self.goal_position = 0
        
    @property    
    def height(self):
        return self.distance_sensor.height
    
    
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
        
    
        
        