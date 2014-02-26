from __future__ import division
from math import sqrt
from Vector import Vector


DISTANCE = 0.4

def sign(number):
    if number == 0:
        return 1
    else:
        return abs(number)/number
'''
Returns true if the values are equivalent in the given mode.
modes:
0 : total
1 : color
2 : shape
'''    
def equivalent_values(value_1, value_2, mode):
    if mode == 1:
        value_1 = value_1%10
        value_2 = value_2%10
    elif mode == 2:
        value_1 = int(str(value_1)[0])
        value_2 = int(str(value_2)[0])
    else:
        pass
    return value_1 == value_2

class Node(object):
    
    def __init__(self, value, position=Vector(9999999999, 9999999999)):
        self.value = value
        self.neighbours = [0,0,0,0,0,0]
        self.position = position
        
        
    
        
    def has_default_position(self):
        return self.position == Vector(9999999999, 9999999999)
        
    def determine_position(self, reference_node, relative_position):
        reference_position = reference_node.position
        reference_xcoord = reference_position.xcoord
        reference_ycoord = reference_position.ycoord
        differences = {     0 : (-DISTANCE*1/2, DISTANCE*sqrt(3)/2),
                            1 : (DISTANCE*1/2, DISTANCE*sqrt(3)/2),
                            2 : (DISTANCE,0),
                            3 : (DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            4 : (-DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            5 : (-DISTANCE, 0)
                            }
        try:
            delta_x, delta_y = differences[relative_position]
        except KeyError:
            print "The relative position must be between 0 and 5 inclusive."
        xcoord = reference_xcoord + delta_x
        ycoord = reference_ycoord + delta_y
        return Vector(xcoord, ycoord)
    
    
    def add_node(self, new_node, relative_position):
        
        if self.neighbours[relative_position] == new_node:
            pass  #This node is already a neighbour.
            
        elif (not self.neighbours[relative_position] == 0):
            print "This node already has a neighbour in the given position." 
        
        else: 
            
            new_position = new_node.determine_position(self, relative_position)
            
            if new_node.has_default_position():    
                new_node.position = new_position
                
            if not new_node.position == new_position:
                print "The new node cannot be placed in this place of the grid, as it already lies somewhere else."
                
            else:
                self.neighbours[relative_position] = new_node  #add the node to the correct position on self.
                new_node.neighbours[(relative_position + 3)%6] = self  #Add self to the correct position on the node
                
                index_left_neighbour = (relative_position - 1)%6  #Calculate the index of the left neighbour of the new node
                index_right_neighbour = (relative_position + 1)%6 #Calculate the index of the right neighbour of the new node
                left_neighbour = self.neighbours[index_left_neighbour]
                right_neighbour = self.neighbours[index_right_neighbour]
                
                if left_neighbour != 0:
                    left_neighbour.add_node(new_node, (relative_position + 1)%6)  #add the node to the correct position on the left neighbour.
                if right_neighbour != 0:
                    right_neighbour.add_node(new_node, (relative_position - 1)%6)  #add the node to the correct position on the left neighbour.
    
    
    def find_node(self, xcoord, ycoord):
        current_node = self
        right_height = False
        found = False
        while not found:
            current_xcoord = current_node.position.xcoord
            current_ycoord = current_node.position.ycoord
            delta_x = xcoord - current_xcoord
            delta_y = ycoord - current_ycoord
            if abs(delta_y) > sqrt(3)/2*DISTANCE/2 and not right_height:
                x_parameter = sign(delta_x)  # right, -1 left
                y_parameter = sign(delta_y)  # 1 up, -1 down
                relative_direction = int(2 + x_parameter*y_parameter/2 - 3/2*y_parameter)
                # again calculated by use of a table with all possible combinations and their respective outcomes.
                new_node = current_node.neighbours[relative_direction]
                if new_node != 0:
                    current_node = new_node
                else:
                    right_height = True
                    print "The closest node to this position lies on the edge of the field."
            elif abs(delta_x) > DISTANCE/2:
                new_node = current_node.neighbours[int(delta_x/abs(delta_x)*3/2 + 1/2)%6]
                if new_node != 0:
                    current_node = new_node
                else:
                    found = True
                    print "The closest node to this position lies on the edge of the field."
            else:
                found = True
        return current_node
    
    def find_triangle(self, node_1, node_2, node_3): # node = value, mode
        value_1, mode_1 = node_1
        value_2, mode_2 = node_2
        value_3, mode_3 = node_3
        results = []
        if equivalent_values(self.value, value_1, mode_1):
            for x in range(0,6):
                first_neighbour = self.neighbours[x]
                if first_neighbour != 0 and equivalent_values(first_neighbour.value, value_2, mode_2):
                    second_neighbour = first_neighbour.neighbours[x+2]
                if second_neighbour != 0 and equivalent_values(second_neighbour.value, value_3, mode_3):
                    results.append(self, first_neighbour, second_neighbour)
                else:
                    pass
        else:
            pass
        return results
        
    def find_line(self, node_1, node_2):
        results = []
        value_1, mode_1 = node_1
        value_2, mode_2 = node_2
        if equivalent_values(self.value, value_1, mode_1):
            for x in range(0,6):
                neighbour = self.neighbours[x]
                if neighbour != 0 and equivalent_values(neighbour.value, value_2, mode_2):
                    results.append(self, neighbour)
        return results        
        
      
    def iterate_row(self, value, direction=1):
        relative_position = int(0.5 + 1.5*direction)%6
        previous_node = self
        current_node = self
        results = []
        while current_node != 0:
            if current_node.value == value:
                results.append(current_node)
                previous_node = current_node
            current_node = current_node.neighbours[relative_position]
        return results, previous_node
        
    def row_extreme(self, direction):
        relative_position = int(0.5 + 1.5*direction)%6
        current_node = self
        while current_node.neighbours[relative_position] != 0:
            current_node = current_node.neighbours[relative_position]
        return current_node
    
    def next_row(self, vert_direction, hor_direction):  # 1 is up, -1 is down, 1 is left to right, -1 right to left
        relative_position = int(2.0 + -3.0*vert_direction/2.0 - hor_direction*vert_direction/2.0)
        #afgeleid van a*v**2 + b*v + c*h*v met de 4 vergelijkingen van wat de relative direction moet zijn.
        print relative_position
        if self.neighbours[relative_position] == 0:
            return 0 #There is no next row.
        else:
            return self.neighbours[relative_position].row_extreme(hor_direction) 
        
    def iterate_field(self, value, vert_direction=-1, hor_direction=1):
        current_node = self
        intermediate_results = []
        results = []
        while current_node != 0:
            intermediate_results, current_node = current_node.iterate_row(value, hor_direction)
            for result in intermediate_results:
                results.append(result)
            current_node = current_node.next_row(vert_direction, hor_direction)
            hor_direction = hor_direction*-1
        return results
    
    def iterate_concentrically(self, relative_direction, value, rotation, depth):
        previous_node = 0
        current_node = self 
        results = []
        intermediate_results = []
        i = 1
        print i
        while i <= depth:
            intermediate_results, current_node, previous_node, relative_direction, rotation = current_node.basic_concentric(previous_node, relative_direction, value, i, rotation)
            if current_node == 0:
                print "There is no more field to iterate."
                i = depth + 1
            else:
                for result in intermediate_results:
                    results.append(result)
                i += 1
            
        return results
            
            
    def resolve_boundary_encounter(self, previous_node, relative_direction, switch_direction, i, rotation):
        next_node = 0
        switch_direction = i - switch_direction
        rotation = rotation*-1
        while next_node == 0:
            relative_direction += rotation
            next_node = self.neighbours[relative_direction]
            if next_node == previous_node:
                while switch_direction != 0:
                    next_node = next_node.neighbours[relative_direction]
                    switch_direction -= 1
                if next_node == 0:
                    return 0,0,0,0,0,0
                else:
                    pass
            else:
                switch_direction -= 1
            if switch_direction == 0:
                switch_direction = i
        return next_node, self, relative_direction, switch_direction, i, rotation
            
        
        
    def basic_concentric(self, previous_node, relative_direction, value, i, rotation):
        results = []
        switch_direction = i - 1
        nodes_visited = 1
        current_node = self.neighbours[relative_direction]
        back_up_node = current_node
        back_up_direction = 0
        backed_up = False
        if current_node == 0:
            current_node, previous_node, relative_direction, switch_direction, i, rotation  = self.resolve_boundary_encounter(previous_node, relative_direction, switch_direction, i, rotation)
            if current_node == 0:
                return 0,0,0,0,0
            backed_up = True
        else:
            relative_direction = (relative_direction + rotation)%6
            back_up_direction = (relative_direction + 3)%6
            previous_node = self
        if current_node.value == value:
                results.append(current_node)
        print current_node.value
        
        while nodes_visited < 6*i:
            if switch_direction == 0:
                relative_direction = (relative_direction + rotation)%6
                switch_direction = i
            new_node = current_node.neighbours[relative_direction]
            if new_node == 0:
                if backed_up == True:
                    nodes_visited = 6*i
                else:
                    current_node = back_up_node
                    relative_direction = back_up_direction
                    previous_node = current_node.neighbours[(relative_direction + 3)%6]
                    switch_direction = 1
                    rotation = rotation*1
                    backed_up = True
            else:
                previous_node = current_node
                current_node = new_node
                nodes_visited += 1
                switch_direction -= 1
            if current_node.value == value:
                results.append(current_node)
            print current_node.value
        
        return results, current_node, previous_node, relative_direction, rotation
    
def calculate_side_length(top_left_node):
    side_length = 0
    current_node = top_left_node
    while current_node.neighbours[2] != 0:
        side_length += 1
        current_node = current_node.neighbours[2]
    return side_length
        
def first_meaningful(left_node):
    current_node = left_node
    first_meaningful = 0


        
def make_field(field):
    first_elements = []
    left_top_node = Node(field[0][0])
    for row in field:
        first_element_of_row = Node(row[0])
        current_node = first_element_of_row
        first_elements.append(first_element_of_row)
        for x in range(1, len(row)):
            next_node = Node(row[x])
            current_node.add_node(next_node)
            current_node = next_node
    relative_direction = 3
    increment = 1
    for x in range(0, len(first_elements)-1):
        current_element = first_elements[x]
        next_element = first_elements[x+1]
        current_element.add_node(next_element, relative_direction)
        relative_direction += increment
        increment = increment*-1
    

    
    return left_top_node
        
    
                
              
            
            
                
                

def create_field():
    iterating_node = 0
    starting_node = Node(1, Vector(0,0))
    high_1 = Node(6)
    high_2 = Node(10)
    low_1 = Node(13)
    low_2 = Node(17)  #Creating the first nodes of each row.
    starting_node.add_node(high_1, 1)
    high_1.add_node(high_2, 1)
    starting_node.add_node(low_1, 3)
    low_1.add_node(low_2, 3)
    current_node = starting_node
    for x in range(2, 6):
        new_node = Node(x)
        current_node.add_node(new_node, 2)
        current_node = new_node
        if x == 2:
            iterating_node = current_node
    current_node = high_1    
    for x in range(7, 10):
        new_node = Node(x)
        current_node.add_node(new_node, 2)
        current_node = new_node
    current_node = high_2
    for x in range(11, 13):
        new_node = Node(x)
        current_node.add_node(new_node, 2)
        current_node = new_node
    current_node = low_1
    for x in range(14, 17):
        new_node = Node(x)
        current_node.add_node(new_node, 2)
        current_node = new_node
    current_node = low_2
    for x in range(18, 20):
        new_node = Node(x)
        current_node.add_node(new_node, 2)
        current_node = new_node
    return iterating_node
        
def iterate_test(starting_node, rel_direction):
    results = starting_node.iterate_concentrically(rel_direction, 3, 1, 4)
    
starting_node = create_field()
iterate_test(starting_node, 1)
    
    
        
    
            