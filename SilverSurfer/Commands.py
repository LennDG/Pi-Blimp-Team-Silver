import time, threading

class ManualMove(object):

    def __init__(self, zeppelin, direction):
        self.zeppelin = zeppelin
        self.direction = direction

    def execute(self):
        self.zeppelin.control.move(self.direction)

class ManualTurn(object):
    
    def __init__(self, zeppelin, direction):
        self.zeppelin = zeppelin
        self.direction = direction

    def execute(self):
        self.zeppelin.control.turn(self.direction)

class Stop(object):
    
    def __init__(self, zeppelin):
        self.zeppelin = zeppelin

    def execute(self):
        self.zeppelin.control.hor_stop()
        self.zeppelin.control.vert_stop()

class ManualVertMove(object):
    def __init__(self, zeppelin, level):
        self.zeppelin = zeppelin
        self.level = level
        
    def execute(self):
        self.zeppelin.control.vert_move(self.level)
        

'''
This module contains all the Command classes.
'''

'''
This class is the Command superclass. All the command classes are child classes from this class. This class defines an run method
that must be implemented by all child classes.
'''
class Command(threading.Thread, object):
    
    def __init__(self, has_priority):
        threading.Thread.__init__(self)
        self.has_priority = has_priority
        self.is_executed = False
        self.stop = False
    
    '''
This method must be implemented by all child classes. In its current state, it does not do anything.
'''
    def run(self):
        #This runs the command, sets the time necessary to run it in the zeppelin object
        pass
    
    def stop(self):
        self.stop = True
        self.is_executed = True
    
    '''
    A sleep method that checks every 0.1s whether or not the thread has to stop.
    '''
    def sleep(self, sleeptime):
        i = 0
        rest = sleeptime % 0.1
        j = sleeptime / 0.1
        j = int(j)
        while(i!=j):
            if(self.stop == True):
                return
            else:
                time.sleep(0.1)
            i = i + 1
        time.sleep(rest)
    
'''
This class describes the move command. A parameter can be supplied which will represent the distance the object that runs
this command should move.
'''
class Move(Command):
    
    def __init__(self, has_priority, distance, zeppelin):
        super(Move, self).__init__(has_priority)
        self.distance = distance
        self.zeppelin = zeppelin
    
    '''
This method will initiate the movement of the object that runs this command.
'''
    def run(self):
        p_1 = 0.55
        p_2 = 0.3
        resting_time = 5.92
        one_length = 0.5
        if(self.distance < 0.5):
            pass
        else:
            self.zeppelin.control.move(self.distance) #distance points to the direction the zeppelin has to move
            self.sleep(p_1)
            self.zeppelin.control.hor_stop()
            self.sleep(resting_time)
            j = int(self.distance / one_length)
            for i in range(0, j-1):
                self.zeppelin.control.move(self.distance) #distance points to the direction the zeppelin has to move
                self.sleep(p_2)
                self.zeppelin.control.hor_stop()
                self.sleep(resting_time)
        self.sleep(resting_time)
        self.is_executed = True
        

class Turn(Command):
    
    def __init__(self, has_priority, distance, zeppelin): # 1 = clockwise, -1 = counterclockwise
        
        super(Turn, self).__init__(has_priority)
        self.zeppelin = zeppelin
        self.distance = distance    #"distance" is een foute naam, dit staat voor de hoek in aantal graden, maar ik wist niet of dit via overerving wel ging. Anyways this one works. -Peter
        
    #deze methode is NOG NIET GEKALIBREERD
    def run(self):
        resting_time = 3    #tijd tussen impulsen
        unit = 20           #hoeveel graden draaien we per impuls, MOET EEN DELER ZIJN VAN HET TOTAAL AANTAL GRADEN
        a = 0.02            #Multiplier: hoe lang moeten we stroom zetten per impuls om unit aantal graden te draaien
        brake_puls = 0.7*a*unit
        rest = self.distance % unit  
        j = int(self.distance / unit)
        for i in range(0, j-1):
            self.zeppelin.control.turn(self.distance)
            self.sleep(a*unit)
            self.zeppelin.control.hor_stop()
            self.sleep(resting_time)
        self.sleep(rest)
        self.zeppelin.control.turn(self.distance)
        self.sleep(brake_puls)
        self.zeppelin.control.hor_stop()
        self.is_executed = True
           

class Ascension(Command):
    
    def __init__(self, has_priority, height, zeppelin):
        super(Ascension, self).__init__(has_priority)
        self.height = height
        self.zeppelin = zeppelin
        
    def run(self):
        self.zeppelin.goal_height = self.zeppelin.height + self.height
        while(self.zeppelin.height < self.height - 10 or self.zeppelin.heigth > self.height +10):
            self.sleep(0.1)
        self.is_executed = True
        
    def stop(self):
        self.zeppelin.goal_height = self.zeppelin.height

class VertMove(Command):
    def __init__(self, has_priority, level):
        super(VertMove,self).__init__(has_priority)
        self.level = level
        
    def run(self,zeppelin):
        zeppelin.control.vert_move(self.level)
        self.sleep(1000)
        zeppelin.control.vert_stop()