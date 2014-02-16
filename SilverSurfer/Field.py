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
                
                

def create_field():
    starting_node = Node(10)
    #maak hier een veld aan op basis van de starting node.
            