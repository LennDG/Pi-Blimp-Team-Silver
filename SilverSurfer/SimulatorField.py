from __future__ import division
from math import sqrt, pi
from Vector import Vector
from Figure import Figure
import time

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
        return (self.position == Vector(9999999999, 9999999999))
    
    
    """
    Determines the position of this node if it were to be added at the relative position
    on the given node. 
    """    
    def determine_position(self, reference_node, relative_position):
        
        # Assign the coordinates of the reference node
        reference_xcoord = reference_node.position.xcoord
        reference_ycoord = reference_node.position.ycoord
        
        # Calculate the differences that will have to be added to the reference position.
        differences = {     0 : (-DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            1 : (DISTANCE*1/2, -DISTANCE*sqrt(3)/2),
                            2 : (DISTANCE,0),
                            3 : (DISTANCE*1/2, DISTANCE*sqrt(3)/2),
                            4 : (-DISTANCE*1/2, DISTANCE*sqrt(3)/2),
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
            pass
            #print "This node already has a neighbour in the given position." 
        
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
        
        self.tablets = []
        
        parsed_csv_file, number_of_rows = parsed_csv_file
        # convert the lists of tuples into lists of nodes
        rows = []
        for x in range(0, number_of_rows):
            line = []
            for element in parsed_csv_file[x]:
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
        
        # Tablets
        for x in range (number_of_rows, len(parsed_csv_file)):
            print parsed_csv_file
            tablet = Vector(float(parsed_csv_file[x][0])/10.0, float(parsed_csv_file[x][1])/10.0)
            print tablet.xcoord
            self.tablets.append(tablet)
        print len(self.tablets)
    
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
        
        key = hor_direction, vert_direction
        
        directions = {  (1,1)  : 0,
                        (1,-1) : 4,
                        (-1,1) : 1,
                        (-1,-1): 3
                        }
        
        # Determines the relative position to find a node on the row above/below this row
        relative_position = directions[key]
        
        # Return the outer node of the row or 0 if there is no row above/below this one.
        return self.row_extreme(node_in_row.neighbours[relative_position], hor_direction)
    
    
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
            current_node = self.next_row(current_node, direction)
            direction = direction*-1
            
            
        
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
            delta_y = current_ycoord - ycoord
            if abs(delta_y) > sqrt(3)/2*DISTANCE/2 and not right_height:
                x_parameter = sign(delta_x)  # 1 right, -1 left
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
    
    
   
    
    @classmethod
    def calculate_minimal_distance(cls, positions):
        side_length = 99999999999999999999999.0
        for x in range(0, len(positions)):
            for y in range(x+1, len(positions)):
                length = (positions[x] - positions[y]).norm
                if length < side_length:
                    side_length = length
        return side_length
    
   
    # getest
    @classmethod    
    def define_structure(cls, figures, vectors):
        
        
        length = cls.calculate_minimal_distance(vectors)
        
        nodes = []
        
        for figure in figures:
            node = 0
            node = Node(figure)
            nodes.append(node)
            
        if len(nodes) == 0:
            return nodes
            
        nodes[0].position = Vector(0,0)
            
        cls.add_to_structure(vectors, nodes, length, 0, 0)
        
        return nodes
        
    
    # getest    
    @classmethod
    def add_to_structure(cls, positions, nodes, length, own_index, reference_angle):
        
        allowable_error = length*0.3
        current_position = positions[own_index]
        current_node = nodes[own_index]
        
        for x in range(0, len(positions)):
            position = positions[x]
            node = nodes[x]
            stop = False
            for y in range(0,6):
                if node.neighbours[y] != 0:
                    stop = True
            if node == current_node or stop == True:
                pass
            
            elif (position - current_position).norm  - length < allowable_error:
                angle = (position - current_position).angle
                
                if isinstance(reference_angle, (int, long)):
                    reference_angle = float(angle)
                    
                angle = angle - reference_angle
                
                # Normalize angle
                while angle < 0:
                    angle = angle + 2*pi
                while angle >= 2*pi:
                    angle = angle - 2*pi
                    
                # transform angle into 6 integer space
                relative_position = angle/2/pi*6 + 0.3 # Adding some marge
                relative_position = int(relative_position)%6 # 0,1,2,3,4,5
                
                nodes[own_index].add_node(nodes[x], relative_position)
                
                cls.add_to_structure(positions, nodes, length, x, reference_angle)
                
    
    # Zou ook moeten werken.
    def match_partial_field(self, virtual_nodes, estimated_position, t):
 
        threshold_score = 2.4 #2.5 # For now
        
        real_node = 0
        corresponding_virtual_node= 0
        score = 0.0
        relative_direction = 0
        
        for node in virtual_nodes:
            temp_result, temp_score, direction = self.match_node_configuration(node, estimated_position, threshold_score, t)
            if temp_score > score:
                real_node = temp_result
                corresponding_virtual_node = node
                score = temp_score
                relative_direction = direction
        
        print score
        if score >= threshold_score and real_node != 0:
            return real_node, corresponding_virtual_node, relative_direction
        else:
            return 0
            
            
                
    def match_node_configuration(self, node_in_structure, estimated_position, threshold, t):
        
        # First, search all nodes in the field that match the given node.
        initials = self.search_field(node_in_structure.figure)
                
        result = 0
        score = 0.0
        relative_direction = 0
                
        # now start the matching
        for initial in initials:
            if time.time() - t > 4.0:
                print "position detection timed out."
                return result, score, relative_direction
            
            for x in range(0,6):
                if time.time() - t > 4.0:
                    print "position detection timed out."
                    return result, score, relative_direction
                try:
                    temp = self.match_recursively(initial, node_in_structure, Node(initial.figure), x, 0, threshold, t)
                    if temp > score:
                        score = temp
                        relative_direction = x
                        result = initial
                except RuntimeError:
                    pass
         
        return result, score, relative_direction
                
    
    def match_recursively(self, current_node, node_in_structure, check_node, direction_difference, score, threshold, t):
        
        time_limit = 4.0
        
        score = score + self.assign_score(current_node, node_in_structure)
        if time.time() - t > 4.0:
            print "position detection timed out."
            return score
        if score > threshold or score < 0:
            return score
        for x in range(0, 6):
            virtual_direction = (x + direction_difference)%6
            if time.time() - t > 4.0:
                print "position detection timed out."
                return score
            if score > threshold or score < 0:
                return score
            
            if  check_node.neighbours[virtual_direction] == 0 and node_in_structure.neighbours[virtual_direction] != 0:
                next_node = current_node.neighbours[x]
                next_node_in_partial_field = node_in_structure.neighbours[virtual_direction]
                new_check_node = Node(next_node_in_partial_field.figure)
                check_node.add_node(new_check_node, virtual_direction)
                if next_node == 0 or next_node.figure.color == 'x': # Als er in het echte veld geen node ligt, is deze configuratie onmogelijk.
                    return -1000.0
                score = self.match_recursively(next_node, next_node_in_partial_field, new_check_node, direction_difference, score, threshold, t)
        
        return score
    
    
    # to be implemented fully
    def assign_score(self, real_node, virtual_node):
        
        score = 0.0
        
        # add score based on color:
        real_color = real_node.figure.color
        virtual_color = virtual_node.figure.color
        if real_color == virtual_color:
            if real_color == 'blue':
                score = score + 0.5
            else:
                score = score + 0.5
        elif real_color == 'red' or real_color == 'yellow' or real_color == 'white' or real_color == 'blue' or (real_color == 'green' and virtual_color != 'blue'):
            score = score -10.0
            
        # add score based on shape
        real_shape = real_node.figure.shape
        virtual_shape = virtual_node.figure.shape
        if real_shape == virtual_shape:
            score = score + 0.3
            
        return score
        
    
    
    # lijkt op het eerst zicht geen fouten in te zitten
    def locate_nodes(self, figure_images):
        
        
        # Put the figures and images in their respective lists.
        t = time.time()
        
        positions = []
        figures = []
        
        # lists for indices.
        circles = []
        stars = []
        hearts = []
        rectangles = []
        undefineds = []
        
        for image in figure_images:
            figure = Figure(image[0], image[1])
            vector = Vector(image[2], image[3])
            
            # Withhold figures with y-values of 494 onwards, something wrong with the camera.
            # Make shapes on the edges undefined, as they don't provide information.
            figures.append(figure)
            positions.append(vector)
                
        for x in range(0,len(figures)):
            if figures[x].shape == 'circle':
                circles.append(x)
            elif figures[x].shape == 'star':
                stars.append(x)
            elif figures[x].shape == 'heart':
                hearts.append(x)
            elif figures[x].shape == 'rectangle':
                rectangles.append(x)
            else:
                undefineds.append(x)
        
        new_figures = []
        new_positions = []
        
        for x in circles:
            new_figures.append(figures[x])
            new_positions.append(positions[x])
        for x in stars:
            new_figures.append(figures[x])
            new_positions.append(positions[x])
        for x in hearts:
            new_figures.append(figures[x])
            new_positions.append(positions[x])
        for x in rectangles:
            new_figures.append(figures[x])
            new_positions.append(positions[x])
        for x in undefineds:
            new_figures.append(figures[x])
            new_positions.append(positions[x])
            
        figures = new_figures
        positions = new_positions
            
        virtual_nodes = self.define_structure(figures, positions)
        
        if len(virtual_nodes) == 0:
            return 0
        
        estimated_position = Vector(0,0) # for now, radius in method above allows this.
        
        try:
            real_node, corresponding_virtual_node, relative_direction = self.match_partial_field(virtual_nodes, estimated_position,t)
        except TypeError:
            return 0
        
        virtual_neighbour = 0
        index = 0 
        
        while virtual_neighbour == 0 and index < 6:
            virtual_neighbour = corresponding_virtual_node.neighbours[index]
            index += 1
            
        assert virtual_neighbour != 0
        
        real_neighbour = real_node.neighbours[- relative_direction + index - 1]
        
        assert real_neighbour != 0
        
        index_1 = virtual_nodes.index(corresponding_virtual_node)
        index_2 = virtual_nodes.index(virtual_neighbour)
        position_1 = positions[index_1]
        position_2 = positions[index_2]
        
        print "Position found in " + str(t - time.time()) + ' seconds.'
        
        return real_node, real_neighbour, position_1, position_2