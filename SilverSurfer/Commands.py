'''
This module contains all the Command classes.
'''

'''
This class is the Command superclass. All the command classes are child classes from this class. This class defines an execute method
that must be implemented by all child classes.
'''
class Command(object):
    
    def __init__(self):
        pass
    
    '''
    This method must be implemented by all child classes. In its current state, it does not do anything.
    '''
    def execute(self, zeppelin):
        pass

'''
This class inherits from Command and is the superclass of all classes that need a certain time to be carried out. During this time,
other commands should be able to be executed.
'''
class TermCommand(Command):
    
    '''
    The constructor of this superclass demands a parameter. This parameter will be converted into the time necessary to carry out the
    command.
    '''
    def __init__(self, parameter):
        super(TermCommand, self).__init__()
        self.parameter = parameter
    
    '''
    This method calculates the time necessary to perform the command based on the parameter given to the constuctor. This method
    must be implemented by all subclasses.
    '''
    def calculate_time(self):
        return -1
        print "this method hasn't been implemented yet."
    
'''
This class describes the move command. A parameter can be supplied which will represent the distance the object that executes 
this command should move.
'''
class Move(TermCommand):
    
    def __init__(self, distance):
        super(Move, self).__init__(distance)
    
    '''
    This method will initiate the movement of the object that executes this command.
    '''    
    def execute(self, zeppelin):
        zeppelin.control.move(self.parameter)
    
    '''
    this method calculates the time necessary to move the given distance based on the linear function a*self.parameter + b
    @return: a*self.parameter + b
    '''  
    def calculate_time(self):
        
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return a*self.parameter + b  #seconds is a function of angle
        

class Turn(TermCommand):
    
    def __init__(self, parameter):
        super(Turn, self).__init__(parameter)
    
    def execute(self, zeppelin):
        zeppelin.control.turn(self.parameter)
        
    def calculate_time(self):
        
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return a*self.parameter + b  #seconds is a function of angle
           

class Ascension(Command):
    
    def __init__(self, height):
        super(Ascension, self).__init__()
        self.height = height
        
    def execute(self, zeppelin):
        zeppelin.control.goal_height = self.height

class VertMove(Command):
    def __init__(self,level):
        super(VertMove,self).__init__()
        self.level = level
        
    def execute(self,zeppelin):      
        zeppelin.control.vert_move(self.level)  

class HorStop(Command):
    
    def __init__(self):
        super(HorStop, self).__init__()
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        

class VertStop(Command):
    
    def __init__(self):
        super(VertStop, self).__init__()
        
    def execute(self, zeppelin):
        zeppelin.control.vert_stop()
        

class Stop(Command):
    
    def __init__(self):
        super(Stop, self).__init__()
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        zeppelin.control.vert_stop()
    