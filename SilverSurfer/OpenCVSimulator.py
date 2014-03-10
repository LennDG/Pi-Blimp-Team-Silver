from Vector import Vector
from math import pi
import random
import time

class OpenCVSimulator(object):
    
    # The height of a picture in pixels.
    IMAGE_PIXEL_HEIGHT = 500

    # The width of a picture in pixels.
    IMAGE_PIXEL_WIDTH = 500 

    # The scope of a picture at 1m altitude.
    IMAGE_WIDTH = 0.4
    
    def __init__(self, error_level, velocity_error, angular_instability):
        
        self.navigator = 0
        
        # The mean deviation of the image coordinates form their supposed position in pixels.
        self.ERROR_LEVEL = error_level
        self.VELOCITY_ERROR = velocity_error
        self.ANGULAR_INSTABILITY = angular_instability
        self.height = 1.5
        self.last_updated = time.time()
    
      
    def scaling_factor(self):
        return OpenCVSimulator.IMAGE_PIXEL_WIDTH/(OpenCVSimulator.IMAGE_WIDTH*(self.height+0.01))
    
    def calculate_next_state(self):
        
        velocity = self.navigator.calculate_goal_velocity().turn(random.gauss(self.VELOCITY_ERROR, self.VELOCITY_ERROR/3))
        time_stamp = time.time()
        decoding_time = random.gauss(0.9, 0.05)
        time_since_last_image = time_stamp - self.last_updated
        time.sleep(decoding_time)
        new_position = self.navigator.position + velocity*time_since_last_image
        print "intended position: " + str(new_position.xcoord) + ", " + str(new_position.ycoord)
        new_angle = self.simulate_new_angle(time_since_last_image)
        
        return new_position, new_angle, time_stamp
        
    def find_triangle(self, x, y):
        
        first_node = self.navigator.field.find_node(x,y)
        
        zeppelin_vector = Vector(x,y) - first_node.position
        
        # Normalize angle
        angle = zeppelin_vector.angle
        while angle < 0:
            angle = angle + 2*pi
        while angle > 2*pi:
            angle = angle - 2*pi
        
        # transform angle into 6 integer space
        angle = angle/2/pi*6 # maximum angle =  6
        angle = int(angle)
        angle = (6 - angle)%6
        angle = (angle + 2)%6
        
        second_node = 0
        third_node = 0
        
        while True:
            second_node = first_node.neighbours[angle]
            third_node = first_node.neighbours[(angle - 1)%6]
            angle = (angle + 1)%6
            if second_node != 0 and third_node != 0:
                break
        
        return first_node, second_node, third_node
        
    def generate_image(self):
        
        zeppelin_position, angle, time_stamp = self.calculate_next_state()
        self.height = self.navigator.distance_sensor.height/100
        
        nodes = self.find_triangle(zeppelin_position.xcoord, zeppelin_position.ycoord)
        
        # On the image the zeppelin always lies in the middle
        zeppelin_image = Vector(OpenCVSimulator.IMAGE_PIXEL_WIDTH/2, OpenCVSimulator.IMAGE_PIXEL_HEIGHT/2)
        
        # Calculate the relative positions of the nodes to the zeppelin.
        node_1_vector = nodes[0].position - zeppelin_position
        node_2_vector = nodes[1].position - zeppelin_position
        node_3_vector = nodes[2].position - zeppelin_position
        
        # Transform these vectors into the image space.
        node_1_vector = node_1_vector.turn(-1*angle)*self.scaling_factor()
        node_2_vector = node_2_vector.turn(-1*angle)*self.scaling_factor()
        node_3_vector = node_3_vector.turn(-1*angle)*self.scaling_factor()
        
        # Calculate position in the image space, adding some error
        node_1_position = zeppelin_image + node_1_vector + Vector(self.ERROR_LEVEL, 0).turn(random.uniform(0, 2*pi))
        node_2_position = zeppelin_image + node_2_vector + Vector(self.ERROR_LEVEL, 0).turn(random.uniform(0, 2*pi))
        node_3_position = zeppelin_image + node_3_vector + Vector(self.ERROR_LEVEL, 0).turn(random.uniform(0, 2*pi))
        
        # Construct the image information
        image_1 = nodes[0].figure.color, nodes[0].figure.shape, node_1_position.xcoord, node_1_position.ycoord
        image_2 = nodes[1].figure.color, nodes[1].figure.shape, node_2_position.xcoord, node_2_position.ycoord
        image_3 = nodes[2].figure.color, nodes[2].figure.shape, node_3_position.xcoord, node_3_position.ycoord
        zeppelin_image = zeppelin_image.xcoord, zeppelin_image.ycoord
        
        # Return result
        return image_1, image_2, image_3, zeppelin_image, time_stamp
    
    def simulate_angular_velocity(self):
        return self.navigator.angular_velocity + self.ANGULAR_INSTABILITY*random.gauss(0,1)
    
    def simulate_new_angle(self, interval):
        angular_velocity = self.simulate_angular_velocity()
        new_angle = self.navigator.angle + angular_velocity*interval
        return new_angle
    
    def start_daemon(self):
        pass
        
    
    

        
        