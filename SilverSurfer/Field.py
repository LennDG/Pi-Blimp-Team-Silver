from __future__ import division
from math import sqrt
from Vector import Vector
from Figure import Figure


DISTANCE = 0.4

def sign(number):
    if number == 0:
        return 1
    else:
        return abs(number)/number

class Node(object):
    
    def __init__(self, figure, position=Vector(9999999999, 9999999999)):
        self.figure = figure
        self.neighbours = [0,0,0,0,0,0]
        self._position = position
    
    @property    
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        if self.has_default_position():
            self._position = position
        else:
            print "You cannot change the position of a node that has already been placed on a grid."
        
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
        

class Field(object):
    
    def __init__(self, parsed_csv_file):
        
        # convert the lists of tuples of numbers into lists of nodes
        rows = []
        for row in parsed_csv_file:
            line = []
            for element in row:
                node = Node(Figure(element[0], element[1]))
                line.append(node)
            rows.append(line)
            
        #Set the position of the first node to 0,0
        rows[0][0].position = Vector(0,0)
        
        # Add the first nodes of each row to each other.    
        relative_direction = 3
        increment = 1
        for x in range(0, len(rows)-1):
            current_element = rows[x][0]
            next_element = rows[x+1][0]
            current_element.add_node(next_element, relative_direction)
            relative_direction += increment
            increment = increment*-1
            
        # For each row, add the rest of the row to the first node, one by one.
        for row in rows:
            current_node = row[0]
            for x in range(1, len(row)):
                next_node = row[x]
                current_node.add_node(next_node, 2)
                current_node = next_node
        
        # Set the top left node to the correct node.    
        self.top_left_node = rows[0][0]
        
    def row_extreme(self, node_in_row, direction):
        if node_in_row == 0:
            return 0
        relative_direction = int(0.5 + 1.5*direction)%6
        current_node = node_in_row
        while current_node.neighbours[relative_direction] != 0:
            current_node = current_node.neighbours[relative_direction]
        return current_node
    
    def next_row(self, node_in_row, hor_direction, vert_direction=-1):  # 1 is up, -1 is down, 1 is left to right, -1 right to left
        relative_position = int(2 + -3*vert_direction/2.0 - hor_direction*vert_direction/2.0)
        #afgeleid van a*v**2 + b*v + c*h*v met de 4 vergelijkingen van wat de relative direction moet zijn.
        if self.row_extreme(node_in_row, hor_direction).neighbours[relative_position] == 0:
            return 0 #There is no next row.
        else:
            return self.row_extreme(node_in_row.neighbours[relative_position],hor_direction) 
        
    def search_field(self, target_figure):
        current_node = self.top_left_node
        direction = 1
        intermediate_results = []
        results = []
        while current_node != 0:
            intermediate_results, current_node = self.search_row(current_node, target_figure, direction)
            for result in intermediate_results:
                results.append(result)
            current_node = self.next_row(current_node, direction)
            direction = direction*-1
        return results
    
    def search_row(self, first_node_of_row, target_figure, direction=1):
        relative_position = int(0.5 + 1.5*direction)%6
        previous_node = first_node_of_row
        current_node = first_node_of_row
        results = []
        while current_node != 0:
            if current_node.figure == target_figure:
                results.append(current_node)
                previous_node = current_node
            current_node = current_node.neighbours[relative_position]
        return results, previous_node
    
    def find_node(self, xcoord, ycoord):
        current_node = self.top_left_node
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
    
    def find_triangle(self, figure_1, figure_2, figure_3):
        results = []
        possible_initials = self.search_field(figure_1)
        print("length of initials = " + str(len(possible_initials)))
        print possible_initials[0].figure.shape
        for initial in possible_initials:
            for x in range(0,6):
                first_neighbour = initial.neighbours[x]
                if first_neighbour != 0 and first_neighbour.figure == figure_2:
                    second_neighbour = first_neighbour.neighbours[x+2]
                    if second_neighbour != 0 and second_neighbour.figure == figure_3:
                        results.append((initial, first_neighbour, second_neighbour))
                else:
                    pass
        else:
            pass
        return results
        
    def find_lines(self, figure_1, figure_2):
        results = []
        possible_initials = self.search_field(figure_1)
        for initial in possible_initials:
            for x in range(0,6):
                neighbour = initial.neighbours[x]
                if neighbour != 0 and neighbour.figure == figure_2:
                    results.append((initial, neighbour))
        return results        
    

    
        
    
            