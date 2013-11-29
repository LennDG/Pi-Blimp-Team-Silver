import Commands, threading, Queue

class Parser():
    
    def parse_string(self, string):
        string = string.replace(' ','')
        temp = string.split(';')
        return temp

class Compiler():
    
    def __init__(self):
        self.command_words = ["V", "A", "S", "D", "L", "R", "VM", "VS", "HS", "STOP"]
     
    def make_command(self, type, parameter, priority):
        if type == 'V':
            return Commands.Move(priority, parameter)
        elif type == 'A':
            return Commands.Move(priority, -1*parameter)
        elif type == 'S':
            return Commands.Ascension(priority, parameter)
        elif type == 'D':
            return Commands.Ascension(priority, -1*parameter)
        elif type == 'L':
            return Commands.Turn(priority, parameter)
        elif type == 'R':
            return Commands.Turn(priority, -1*parameter)
        elif type == 'VM':
            return Commands.VertMove(priority, parameter)
        elif type == 'VS':
            return Commands.VertStop()
        elif type == 'HS':
            return Commands.HorStop()
        elif type == 'STOP':
            return Commands.Stop()
        else:
            print("I'm disappointed in you.")
            
        
    def compile(self, code):
        
        temp = []
        i = 0
        while i < len(code):
            command = code[i]
            command = command.split(':')
            if len(command) != 2:
                print("The command format was not respected")
            else:
                if not self.command_words.__contains__(command[0]):
                    print(command[0] + " is not a valid command")
                
                else:
                    try:
                        command[1] = float(command[1])
                    except ValueError:
                        print('The parameter supplied is not a number')
                    temp = temp + [self.make_command(command[0], command[1], i == 0)]
            i = i + 1
                    
        return temp
    
class Commandfactory(threading.Thread, object):
    
    def __init__(self, string_queue, zeppelin):
        threading.Thread.__init__(self)
        self.str_queue = string_queue
        self.parser = Parser()
        self.compiler = Compiler()
        self.zeppelin = zeppelin
        
         
    def run(self):
        while True:
            if  not self.str_queue.empty():
                string = self.str_queue.get(False)
                code = self.parser.parse_string(string)
                command = self.compiler.compile(code)
                self.zeppelin.add_command(command)
                
            else:
                pass