from __future__ import division
from math import sqrt
from Vector import Vector
from Figure import Figure

"""
This file contains the field class which is constructed out of node objects, whose class this file
also contains.

@author: Rob Coekaerts
@version 1.0
"""

DISTANCE = 40


"""
This method returns 1 if the given number is positive, -1 when negative.
"""
def sign(number):
    if number == 0:
        return 1
    else:
        return abs(number)/number



""""
The class Node represents a node in a field. A node is defined by the position it occupies
and it holds information about all its neighbouring nodes and the figure that is placed
on the node.
"""
class Node(object):
    
    
    # By default, a standard vector is assigned to a node.
    def __init__(self, figure, position=Vector(9999999999, 9999999999)):
        self.figure = figure
        self.neighbours = [0,0,0,0,0,0]
        self._position = position
    
    
    @property    
    def position(self):
        return self._position
    
    
    """
    The position of a node can only be changed if its current position is still
    the standard position.
    """
    @position.setter
    def position(self, position):
        if self.has_default_position():
            self._position = position
        elif self.position == position:
            pass # The node is already at the right position.
        else:
            raise Exception("You cannot change the position of a node that has already been placed on a grid.")
    
    
    """
    Returns whether this node's position is still the default position, given to it
    by its constructor
    Return self.position == Vector(9999999999, 9999999999)
    """    
    def has_default_position(self):
        return self.position == Vector(9999999999, 9999999999)
    
    
    """
    Determines the position of this node if it were to be added at the relative position
    on the given node. 
    """    
    def determine_position(self, reference_node, relative_position):
        
        # Assign the coordinates of the reference node
        reference_xcoord = reference_node.position.xcoord
        reference_ycoord = reference_node.position.ycoord
        
        # Calculate the differences that will have to be added to the reference position.
        differences = {     0 : (-DISTANCE*1/2, DISTANCE*sqrt(3)/2),
                            1 : (DISTANCE*1/2, DISTANCE*sqrt(3)/2),
                            2 : (DISTANCE,0),
                            3 : (DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            4 : (-DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            5 : (-DISTANCE, 0)
                         }
        
        # Assign delta x and delta y, the increments that will have to be added to
        # the reference position.
        delta_x, delta_y = differences[relative_position]
        
        # Construct and return the position vector.
        xcoord = reference_xcoord + delta_x
        ycoord = reference_ycoord + delta_y
        return Vector(xcoord, ycoord)
    
    
    """
    This method adds the given node to self at the given relative position. It also adds
    the given node to the direct neighbours of self at the appropriate relative position
    as to obtain a consistent field.
    """
    def add_node(self, new_node, relative_position):
        
        if self.neighbours[relative_position] == new_node:
            pass  #This node is already a neighbour.
            
        elif (not self.neighbours[relative_position] == 0):
            print "This node already has a neighbour in the given position." 
        
        else: 
            
            # Determine the position the new node will occupy in the field
            new_node.position = new_node.determine_position(self, relative_position)
            
            # Assign the node to the correct position on self and vice versa
            self.neighbours[relative_position] = new_node
            new_node.neighbours[(relative_position + 3)%6] = self 
            
            # Calculate the indices of the neighbours on self that are also neighbours
            # to the new node and get those nodes.
            index_left_neighbour = (relative_position - 1)%6 
            index_right_neighbour = (relative_position + 1)%6
            left_neighbour = self.neighbours[index_left_neighbour]
            right_neighbour = self.neighbours[index_right_neighbour]
            
            # Add the new node to the appropriate positions on these neighbours with
            # this method so that possible neighbours of these neighbours will also add
            # the new node.
            if left_neighbour != 0:
                left_neighbour.add_node(new_node, (relative_position + 1)%6)
            if right_neighbour != 0:
                right_neighbour.add_node(new_node, (relative_position - 1)%6)
 
 
        
"""
The class field represents a field object that is implicitely defined by its top left corner node and the
internodal relations between this node and other nodes.
"""
class Field(object):
    
    
    """
    This constructor constructs a field given a list, that contains a distinct list for 
    each row in the field. These row lists contain tuples with colors and shapes to define 
    the figures to be placed on the field. Positions are automaticly assigned. The top
    left corner node lies at position (0,0).
    """
    def __init__(self, parsed_csv_file):
        
        # convert the lists of tuples into lists of nodes
        rows = []
        for row in parsed_csv_file:
            line = []
            for element in row:
                node = Node(Figure(element[0], element[1]))
                line.append(node)
            rows.append(line)
            
        #Set the position of the top left node to (0,0)
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
    
    
    """
    This auxiliairy method will return the outer node of the row the given node lies in, 
    given the parameter direction.
    
    Direction = 1 to find the outer node on the right
              = -1 to find the outer node on the left
    """    
    def row_extreme(self, node_in_row, direction):
        
        if node_in_row == 0:
            return 0
        
        # Determine the appropriate relative direction, based on whether
        # we are looking for the left or right row_extreme
        relative_direction = int(0.5 + 1.5*direction)%6
        
        # Start at the given node.
        current_node = node_in_row
        
        # Advance through the nodes until there is no node on the left/right anymore.
        while current_node.neighbours[relative_direction] != 0:
            current_node = current_node.neighbours[relative_direction]
        
        # At this point, the current node will be the outer node of the row.
        return current_node
    
    
    """
    This auxiliairy method returns the outer node in the given horizontal direction on the next row,
    defined by a vertical direction or 0 if there is no next row.
    
    hor_direction    1 for the righter outer node on the next row
                    -1 for the left outer node on the next row
    vert_direction   1 for the outer node on the row above the row the given node lies in.
                    -1 for the outer node on the row below the row the given node lies in.
    """
    def next_row(self, node_in_row, hor_direction, vert_direction=-1):
        
        # Determines the relative position to find a node on the row above/below this row
        # If you wonder how this came about, ask Rob.
        relative_position = int(2 + -3*vert_direction/2.0 - hor_direction*vert_direction/2.0)
        
        # Return the outer node of the row or 0 if there is no row above/below this one.
        if self.row_extreme(node_in_row, hor_direction).neighbours[relative_position] == 0:
            return 0 #There is no next row.
        else:
            return self.row_extreme(node_in_row.neighbours[relative_position],hor_direction)
    
    
    """
    This auxiliary method searches the given figure among the nodes in the row of the given node. 
    It starts at the given node in the specified direction. This method uses the method row_extreme
    to find the initial node of the row to be searched. It returns a tuple consisting of a list with
    the results and the last node that has been visited.
    
    direction    1 searches from left to right
                -1 searches from right to left
    """    
    def search_row(self, node_of_row, target_figure, direction=1):
        
        # Determine the relative position based on the direction.
        relative_position = int(0.5 + 1.5*direction)%6
        
        # initialize current_node and previous_node and the result list
        previous_node = self.row_extreme(node_of_row, -1*direction)
        current_node = previous_node
        results = []
        
        # Search until the end of the row has been reached.
        while current_node != 0:
            if current_node.figure == target_figure:
                results.append(current_node)
                previous_node = current_node
            current_node = current_node.neighbours[relative_position]
            
        # Return the results and the node that has last been visited.
        return results, previous_node
    
    
    """
    This method searches the field row by row to find all the nodes that have the given
    figure. The search starts at the top left corner node and goes left to right, right
    to left on the next row and so on untill the end of grid has been reached.
    """    
    def search_field(self, target_figure):
        
        # Start at the top left corner node, from left to right.
        current_node = self.top_left_node
        direction = 1
        
        # Initialize the result lists.
        intermediate_results = []
        results = []
        
        # Search until the end of the grid has been reached.
        while current_node != 0:
            
            # search the current row and add all results to the result list.
            intermediate_results, current_node = self.search_row(current_node, target_figure, direction)
            for result in intermediate_results:
                results.append(result)
            
            # Move on to the next row.
            direction = direction*-1
            current_node = self.next_row(current_node, direction)
            
        
        # Return all the results.    
        return results
    
    
    """
    This method finds the node on the field that is closest to the position that
    is specified by the given coordinates.
    """
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
    
    
    """
    This method returns the trio of nodes that form the same triangle of figures as
    the given figures in clockwise direction or 0 if no such triangle is found on the
    field.
    
    figures    A tuple of three figures that define a triangle, covered in clockwise
               direction
    """
    def find_triangle(self, figures):
        
        # Find all the nodes on the field that have the first figure on them and
        # hence could be the initial node of the triangle.
        possible_initials = self.search_field(figures[0])
        
        for initial in possible_initials:
            # For all neighbours of this potential initial node, check whether it
            # has the second figure on it.
            for x in range(0,6):
                first_neighbour = initial.neighbours[x]
                if first_neighbour != 0 and first_neighbour.figure == figures[1]:
                    # If the neighbour of the first neighbour in position x+2(check for yourself)
                    # has the third figure on it, we have found the triangle
                    second_neighbour = first_neighbour.neighbours[(x+2)%6]
                    if second_neighbour != 0 and second_neighbour.figure == figures[2]:
                        return initial, first_neighbour, second_neighbour
                    
        # If no results are found, return 0
        return 0
    
    
    """
    This method finds all the pairs of nodes whose figures form the given pair
    of figures, and returns them as a list of tuples.
    """    
    def find_pairs(self, figure_1, figure_2):
        
        # Initialize the list of results.
        results = []
        
        # Find all the nodes on the field that have the first figure on it, and hence
        # could be half of the pair to be found.
        possible_initials = self.search_field(figure_1)
        
        # For each of these possible initial nodes, check whether one of the neighbours
        # contains the second figure. If so, append this pair to the list of results.
        for initial in possible_initials:
            for x in range(0,6):
                neighbour = initial.neighbours[x]
                if neighbour != 0 and neighbour.figure == figure_2:
                    results.append((initial, neighbour))
        
        # Return the list
        return results   
    
    @classmethod
    def calculate_minimal_distance(cls, positions):
        side_length = 99999999999999999999999.0
        for x in range(0, len(positions)):
            for y in range(x+1, len(positions)):
                length = (positions[x] - positions[y]).norm
                if length < side_length:
                    side_length = length
        return side_length
    
   
    @classmethod
    def extract_pairs(cls, positions):
        allowable_error = 40
        results = []
        side_length = cls.calculate_minimal_distance(positions)
        for x in range(0, len(positions)):
            for y in range(x+1, len(positions)):
                distance = (positions[x] - positions[y]).norm
                if abs(distance - side_length) < allowable_error:
                    result = (x,y)
                    results.append(result)
                    
        return results
   
    
    
    """
    This method checks whether the 3 given duos form a triangle. The duos are defined by the positions
    of its endpoints.
    """   
    @classmethod
    def check_for_triangle(cls, positions, index_1, index_2, index_3, index_4, index_5, index_6):
        if positions[index_1] == positions[index_6] and positions[index_2] == positions[index_3] and positions[index_4] == positions[index_5]:
            return (index_1, index_2, index_4)
        else:
            return 0
                
    
    @classmethod    
    def extract_triangles(cls, figure_images):
        
        
        # Initialise results
        final_result = []
        positions = []
        figures = []
        
        # Make a list of figures and a list of positions where the indices link them together?
        for image in figure_images:
            print image[0], image[1]
            figure = Figure(image[0], image[1])
            position = Vector(image[2], image[3])
            figures.append(figure)
            positions.append(position)
            
        # Get all the pairs of nodes which are neighbours from this collection.    
        
        pairs = cls.extract_pairs(positions)
        
        if pairs == 0:
            return 0
        else:
            index_1, index_2 = pairs[0]
            for y in range(1, len(pairs)):
                index_3, index_4 = pairs[y]
                for z in range(y+1, len(pairs)):
                    results = []
                    index_5, index_6 = pairs[z]
                    results.append(cls.check_for_triangle(positions, index_1, index_2, index_3, index_4, index_5, index_6))
                    results.append(cls.check_for_triangle(positions, index_1, index_2, index_3, index_4, index_6, index_5))
                    results.append(cls.check_for_triangle(positions, index_1, index_2, index_4, index_3, index_5, index_6))
                    results.append(cls.check_for_triangle(positions, index_1, index_2, index_4, index_3, index_6, index_5))
                    results.append(cls.check_for_triangle(positions, index_2, index_1, index_3, index_4, index_5, index_6))
                    results.append(cls.check_for_triangle(positions, index_2, index_1, index_3, index_4, index_6, index_5))
                    results.append(cls.check_for_triangle(positions, index_2, index_1, index_4, index_3, index_5, index_6))
                    results.append(cls.check_for_triangle(positions, index_2, index_1, index_4, index_3, index_6, index_5))
                    for result in results:
                        if result != 0:
                            final_result.append(result)
                            
        if final_result == 0:
            return 0
        else:
            for result in final_result:
                result = figures[result[0]], figures[result[1]], figures[result[2]]
            return final_result
    