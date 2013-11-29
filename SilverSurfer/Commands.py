import time

'''
This module contains all the Command classes.
'''

'''
This class is the Command superclass. All the command classes are child classes from this class. This class defines an execute method
that must be implemented by all child classes.
'''
class Command(object):
    
    def __init__(self, has_priority):
        self.has_priority = has_priority
        self.is_executed = False
    
    '''
This method must be implemented by all child classes. In its current state, it does not do anything.
'''
    def execute(self, zeppelin):
        #This executes the command, sets the time necessary to execute it in the zeppelin object
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
    def __init__(self,has_priority, parameter):
        super(TermCommand, self).__init__(has_priority)
        self.parameter = parameter
        
    def execute(self, zeppelin):
        zeppelin.command_time = self.calculate_time()
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
    
    def __init__(self, has_priority, distance):
        super(Move, self).__init__(has_priority, distance)
    
    '''
This method will initiate the movement of the object that executes this command.
'''
    def execute(self, zeppelin):
        super(Move, self).execute(self, zeppelin)
        zeppelin.control.move(self.parameter)
    
    '''
this method calculates the time necessary to move the given distance based on the linear function a*self.parameter + b
@return: a*self.parameter + b
'''
    def calculate_time(self):
        
        a = 1 # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return (a*self.parameter + b) + time.time() #seconds is a function of angle
        

class Turn(TermCommand):
    
    def __init__(self, has_priority, parameter):
        super(Turn, self).__init__(has_priority, parameter)
    
    def execute(self, zeppelin):
        super(Turn, self).execute(self, zeppelin)
        zeppelin.control.turn(self.parameter)
        
    def calculate_time(self):
        
        a = 1 # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return a*self.parameter + b + time.time()#seconds is a function of angle
           

class Ascension(Command):
    
    def __init__(self, has_priority, height):
        super(Ascension, self).__init__(has_priority)
        self.height = height
        
    def execute(self, zeppelin):
        zeppelin.control.goal_height = zeppelin.height + self.height
        
    @property
    def is_executed(self):
        return True

class VertMove(Command):
    def __init__(self, has_priority, level):
        super(VertMove,self).__init__(has_priority)
        self.level = level
        
    def execute(self,zeppelin):
        zeppelin.control.vert_move(self.level)

class HorStop(Command):
    
    def __init__(self):
        super(HorStop, self).__init__(True)
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        
    @property
    def is_executed(self):
        return True
        
        

class VertStop(Command):
    
    def __init__(self):
        super(VertStop, self).__init__(True)
        
    def execute(self, zeppelin):
        zeppelin.control.vert_stop()
        
    @property
    def is_executed(self):
        return True
        

class Stop(Command):
    
    def __init__(self):
        super(Stop, self).__init__(True)
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        zeppelin.control.vert_stop()
        
    @property
    def is_executed(self):
        return True