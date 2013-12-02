import time, threading

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
    def run(self, zeppelin):
        #This runs the command, sets the time necessary to run it in the zeppelin object
        pass
    
    def stop(self):
        self.stop = True
    
    '''
    A sleep method that checks every 0.1s whether or not the thread has to stop.
    '''
    def sleep(self, time):
        i = 0
        rest = time % 0.1
        j = time / 0.1
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
    
    def __init__(self, has_priority, distance):
        super(Move, self).__init__(has_priority)
        self.distance = distance
    
    '''
This method will initiate the movement of the object that runs this command.
'''
    def run(self, zeppelin):
        resting_time = 0
        one_length = 0
        a = 0
        i = 0
        rest = self.distance % one_length
        j = int(self.distance / one_length)
        while(i!=j):
            zeppelin.control.move(self.distance) #distance points to the direction the zeppelin has to move
            self.sleep(a*one_length)
            zeppelin.control.hor_stop
            self.sleep(resting_time)
            i = i+1
        zeppelin.control.move(self.distance)
        self.sleep(a*rest)
        zeppelin.control.hor_stop
        self.sleep(resting_time)
        self.is_executed = True
        

class Turn(Command):
    
    def __init__(self, has_priority, parameter):
        super(Turn, self).__init__(has_priority, parameter)
    
    def run(self, zeppelin):
        resting_time = 0
        unit = 0
        a = 0
        i = 0
        rest = self.distance % unit
        j = int(self.distance / unit)
        while(i!=j):
            zeppelin.control.turn(self.distance) #distance points to the direction the zeppelin has to turn
            self.sleep(a*unit)
            zeppelin.control.hor_stop
            self.sleep(resting_time)
            i = i+1
        zeppelin.control.move(self.distance)
        self.sleep(a*rest)
        zeppelin.control.hor_stop
        self.sleep(resting_time)
        self.is_executed = True
           

class Ascension(Command):
    
    def __init__(self, has_priority, height):
        super(Ascension, self).__init__(has_priority)
        self.height = height
        
    def run(self, zeppelin):
        zeppelin.control.goal_height = zeppelin.height + self.height
        while(zeppelin.height < self.height - 10 or zeppelin.heigth > self.height +10):
            self.sleep(0.1)
        self.is_executed = True
        
    def stop(self, zeppelin):
        zeppelin.control.goal_height = zeppelin.height

class VertMove(Command):
    def __init__(self, has_priority, level):
        super(VertMove,self).__init__(has_priority)
        self.level = level
        
    def run(self,zeppelin):
        zeppelin.control.vert_move(self.level)
        self.sleep(1000)
        zeppelin.control.vert_stop()