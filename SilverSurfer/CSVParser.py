

class CSVParser(object):
    
    def __init__(self):
        pass
    
    def transform_code(self, code):
            
        color = code[0]
        shape = code[1]
        
        colors = {     "B": "blue", 
                       "W": "white", 
                       "Y": "yellow", 
                       "R": "red", 
                       "G": "green",
                       "X": "x"}
        
        shapes = {     "H": "heart", 
                       "C": "oval", 
                       "R": "rectangle", 
                       "S": "star",
                       "X": "x"}
        
        return (colors[color], shapes[shape])
    
    
    def parse(self, csv_file="field.csv"):
        
        # Open the correct file and read its contents.
        f = open(csv_file, "r")
        string = f.read()
        
        # Remove all spaces
        string = string.replace(" ", "")
        
        # Divide into rows
        rows = string.split("\n")
        
        # Divide each row into words
        for x in range(0, len(rows)):
            rows[x] = rows[x].split(",")
                
        # Remove all empty strings
        for x in range(0, len(rows)):
            rows[x] = [y for y in rows[x] if y != ""]
            
        # Turn the codes into tuples with meaningful values
        for x in range(0, len(rows)):
            for y in range(0, len(rows[x])):
                rows[x][y] = self.transform_code(rows[x][y])
                
        return rows
        
        
        