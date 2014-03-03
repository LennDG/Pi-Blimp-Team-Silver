from Vector import Vector
import MotorControl

'''
Created on 13-feb.-2014

@author: Peter
'''

MAXIMUM_SPEED = 1
SLOW_DOWN_DISTANCE = 1.5

class Navigator(object):
    '''
    This class keeps track of the position and physical direction of the zeppelin.
    It also contains the map of the playfield and other useful information in
    regards to the position such as velocity, closest node etc.
    '''

    '''
    This constructor initializes the object with a distance sensor and the top left node of the map.
    '''
    def __init__(self, distance_sensor, starting_node):
        self.motor_control = MotorControl.MotorControl()
        self.distance_sensor = distance_sensor
        self.starting_node = starting_node
        self.closest_node = starting_node
        self.goal_position = Vector(0,0)
        self.angle = 0
        self.angular_velocity = 0 # Testing purposes only.
        self.position = Vector(0,0)
        self.velocity = Vector(0,0)
        self.last_updated = 0
    
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
        
        
    @property    
    def height(self):
        return self.distance_sensor.height
        
    
        
        