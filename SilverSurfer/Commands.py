

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
        zeppelin.control.move()
        
    def calculate_time(self):
        return -1 #moeten nog bedenken hoe we die time gaan berekenen
        print "dummy-implementation"
        

class Turn(Command):
    
    def __init__(self, parameter):
        TermCommand(parameter)
    
    def execute(self, zeppelin):
        zeppelin.control.turn()
        
    def calculate_time(self):
        return -1 #moeten nog bedenken hoe we die time gaan berekenen
        print "dummy-implementation"
        

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
    