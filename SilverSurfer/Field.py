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
            self.neighbours[relative_position].add_node(new_node, relative_position) #Als de node niet kan toegevoegd worden aan deze node, wordt
            #die gewoon ene verder toegevoegd.   
        else:
            
            if relative_position == 0:
                xcoord = self.position.xcoord - DISTANCE*1/2
                ycoord = self.position.ycoord + DISTANCE*sqrt(3)/2
            elif relative_position == 1:
                xcoord = self.position.xcoord + DISTANCE*1/2
                ycoord = self.position.ycoord + DISTANCE*sqrt(3)/2
            elif relative_position == 2:
                xcoord = self.position.xcoord + DISTANCE
                ycoord = self.position.ycoord
            elif relative_position == 3:
                xcoord = self.position.xcoord + DISTANCE*1/2
                ycoord = self.position.ycoord - DISTANCE*sqrt(3)/2
            elif relative_position == 4:
                xcoord = self.position.xcoord - DISTANCE*1/2
                ycoord = self.position.ycoord - DISTANCE*sqrt(3)/2
            elif relative_position == 5:
                xcoord = self.position.xcoord - DISTANCE
                ycoord = self.position.ycoord
            else:
                print "This is not a valid relative position, please use a value ranging from 0 to 5." #throw hier een exception aub.
            
            new_position = Position.Position(xcoord, ycoord)
            if new_node.position == 0:    
                new_node.position = new_position
                
            if not new_node.position.equals(new_position):
                print "This not cannot be placed in this place of the grid, as it already has another place." #hier ook een exception
                
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
            