import Commands, threading, Queue


class Parser():
    
    def parse_string(self, string):
        string = string.replace(' ','')
        temp = string.split(';')
        return temp

class Compiler():
    
    def __init__(self, zeppelin):
        self.command_constructors = {"V":Commands.Move, 
                                     "A":Commands.Move, 
                                     "S":Commands.Ascension, 
                                     "D":Commands.Ascension, 
                                     "L":Commands.Turn, 
                                     "R":Commands.Turn, 
                                     "VM":Commands.VertMove}
        
        self.command_sign = {"V":1, 
                             "A":-1, 
                             "S":1, 
                             "D":-1, 
                             "L":-1, 
                             "R":1, 
                             "VM":1}
        
        self.non_parameter_commands=["VS","HS","STOP"]
        
        self.zep = zeppelin
    
    def make_command(self, command_type, parameter, priority = False):
        if command_type in self.non_parameter_commands:
            return self.command_constructors[command_type]()
        else:
            return self.command_constructors[command_type](priority,self.command_sign[command_type]*parameter, self.zep)
        
            
        
    def compile(self, code):
        
        temp = []
        for c in code:
            command = c
            com = command.split(':')
            try:
                temp = temp + [self.make_command(com[0], com[1], code.index(c)==0)]
            except (KeyError,IndexError,ValueError): #Happens when command is N
                pass
                    
                    
        return temp
    
class Commandfactory(object):
    
    def __init__(self, zeppelin):
        self.parser = Parser()
        self.compiler = Compiler(zeppelin)
        
    def create_commands(self,code_string):   
        code = self.parser.parse_string(code_string)
        return self.compiler.compile(code)
                
 

