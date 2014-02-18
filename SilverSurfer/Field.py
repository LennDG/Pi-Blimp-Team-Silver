from math import sqrt
import Position

DISTANCE = 0.4

class Node(object):
    
    def __init__(self, value):
        self.value = value
        self.neighbours = [0,0,0,0,0,0]
        self.position = 0
        
    def add_node(self, new_node, relative_position):
        
        if self.neighbours[relative_position] == new_node:
            pass
            # Do Nothing
            
        elif (not self.neighbours[relative_position] == 0):
            self.neighbours[relative_position].add_node(new_node, relative_position) #Als de node niet
                            # kan toegevoegd worden aan deze node, wordt die gewoon ene verder toegevoegd.   
        else:
            basis_x = self.position.xcoord
            basis_y = self.position.ycoord
            delta_x = 0
            delta_y = 0
            
            differences = { 0 : (-DISTANCE*1/2, DISTANCE*sqrt(3)/2),
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
                
            xcoord = basis_x + delta_x
            ycoord = basis_y + delta_y
            
            new_position = Position.Position(xcoord, ycoord,0)
            if new_node.position == 0:    
                new_node.position = new_position
                
            if not new_node.position.equals(new_position):
                print "This not cannot be placed in this place of the grid, as it already has another place." 
                #hier ook een exception
                
            else:
                self.neighbours[relative_position] = new_node  #add the node to the correct position on self.
                new_node.neighbours[(relative_position + 3)%6] = self  #Add self to the correct position on the node
                left_neighbour = (relative_position - 1)%6  #Calculate the index of the left neighbour of the new node
                right_neighbour = (relative_position + 1)%6 #Calculate the index of the right neighbour of the new node
                self.neighbours[left_neighbour].add(new_node, relative_position + 2)  #add the node to the correct position on the left neighbour.
                self.neighbours[right_neighbour].add(new_node, relative_position - 2)  #add the node to the correct position on the left neighbour.
      
      
    def iterate_row(self, value, direction=1):
        relative_position = int(0.5 + 1.5*direction)%6
        current_node = self
        results = []
        while current_node.neighbours[relative_position] != 0:
            current_node = current_node.neighbours[relative_position]
            if current_node.value == value:
                results.append(current_node)
        return results, current_node
        
    def row_extreme(self, direction):
        relative_position = int(0.5 + 1.5*direction)%6
        current_node = self
        while current_node.neighbours[relative_position] != 0:
            current_node = current_node.neighbours[relative_position]
        return current_node
    
    def next_row(self, vert_direction):  # 1 is up, -1 is down
        relative_position = int(4.5 + vert_direction*1.5)%6
        if self.neighbours[relative_position] == 0:
            relative_position += 1
        return self.neighbours[relative_position]  # If there is still no neighbour, it will
    # return 0 and there is no next row.
        
    def iterate_field(self, value, vert_direction, hor_direction):
        current_node = self
        intermediate_results = []
        results = []
        while current_node.next_row(vert_direction) != 0 or current_node == self:
            intermediate_results, current_node = current_node.iterate_left_right(value, hor_direction)
            for result in intermediate_results:
                results.append(result)
            current_node = current_node.next_row(-1).row_extreme(hor_direction)
            hor_direction = hor_direction*-1
        return results
    
    def iterate_concentrically(self, relative_direction, value):
        current_node = self
        
            
            
            
                
                

def create_field():
    starting_node = Node(10)
    #maak hier een veld aan op basis van de starting node.
            