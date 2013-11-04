

class Command():
    
    def __init__(self):
        pass
    
    def execute(self, zeppelin):
        pass


class TermCommand(Command):
    
    def __init__(self, parameter):
        Command()
        self.parameter = parameter
    
    def calculate_time(self):
        return -1
        print "this method hasn't been implemented yet."
    

class Move(TermCommand):
    
    def __init__(self, parameter):
        TermCommand(parameter)
        
    def execute(self, zeppelin):
        zeppelin.control.move(self.parameter)
        
    def calculate_time(self):
        
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return a*self.parameter + b  #seconds is a function of angle
        

class Turn(Command):
    
    def __init__(self, parameter):
        TermCommand(parameter)
    
    def execute(self, zeppelin):
        
        zeppelin.control.turn(self.parameter)
        
    def calculate_time(self):
        
        a = 1  # to be determined through heavy testing
        b = 1
        
        #Calculate values for engines and amount of time necessary here...
        return a*self.parameter + b  #seconds is a function of angle
           

class Ascension(Command):
    
    def __init__(self, height):
        Command()
        self.height = height
        
    def execute(self, zeppelin):
        zeppelin.control.goal_height = self.height
        

class HorStop(Command):
    
    def __init__(self):
        Command()
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        

class VertStop(Command):
    
    def __init__(self):
        Command()
        
    def execute(self, zeppelin):
        zeppelin.control.vert_stop()
        

class Stop(Command):
    
    def __init__(self):
        Command()
        
    def execute(self, zeppelin):
        zeppelin.control.hor_stop()
        zeppelin.control.vert_stop()
    