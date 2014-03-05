

class CSV_parser(object):
    
    def __init__(self):
        pass
    
    def transform_code(self, code):
        
        color = code[0]
        shape = code[1]
        
        self.colors = {"B": "blue", 
                       "W": "white", 
                       "Y": "yellow", 
                       "R": "red", 
                       "G": "green",
                       "X": "x"}
        
        self.shapes = {"H": "heart", 
                       "O": "oval", 
                       "R": "rectangle", 
                       "S": "star",
                       "X": "x"}
        
        return (self.colors[color], self.shapes[shape])
    
    
    def parse(self, string):
        
        # Remove all spaces
        string = string.replace(" ", "")
        print string
        
        # Divide into rows
        rows = string.split("\n")
        for x in range(0, len(rows)):
            print rows[0]
        
        # Divide each row into words
        for x in range(0, len(rows)):
            rows[x] = rows[x].split(",")
            for word in rows[x]:
                print word
            
        # Turn the codes into tuples with meaningful values
        for x in range(0, len(rows)):
            for y in range(0, len(rows[x])):
                print rows[x][y]
                rows[x][y] = self.transform_code(rows[x][y])
                
        return rows
        
        
        