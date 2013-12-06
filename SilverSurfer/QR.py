#File for scanning QR codes

#TODO: test all the physical aspects, like resolution and what the zxing library returns

import zxing, threading, zbar, os, math, re
from subprocess import call
from PIL import Image

class Camera(object):
    
    def take_picture(self, img_file, width = 800, height = 600):
        call(["raspistill -w " + str(width) + " -h " + str(height) + " -q 75 " + " -t 0 -o " + img_file], shell=True)        
    

class QRScanner(object):
    
    def __init__(self):
        self.zxing_reader = zxing.BarCodeReader("/home/pi/zxing-1.6")
        
        self.zbar_reader = zbar.ImageScanner()
        self.zbar_reader.parse_config("enable")
        
        self.camera = Camera()  
        
        
    def scan(self):
        #Scans for a QR codes and returns a list of strings.
        tmp = "/home/pi/tmp.jpg"
        self.camera.take_picture(tmp)
        
        QR_strings = self.zbar_read(tmp)
        
        return QR_strings
        
    
    def zxing_read(self, img_file):
        QRcode = self.reader.decode(img_file)
        return QRcode
        
    def zbar_read(self, img_file):
        
        pil = Image.open(img_file).convert('L')
        width, height = pil.size
        raw = pil.tostring()
        
        image = zbar.Image(width, height, 'Y800', raw)
        
        self.zbar_reader.scan(image)
        
        symbols = []
        
        for symbol in image:
            symbols.append(symbol.data)
            
        return symbols
        
        

class QR(threading.Thread, object):
    
    def __init__(self, zeppelin):
        threading.Thread.__init__(self)
        
        self.QR_scanner = QRScanner()
        
        self.QR_codes = {} #Key is the number of the QR code, the values are the data strings.
        self.QR_images = {} #Key is number of the QR, values are the image files
        self.QR_points = {} #Key is the number of the QR, values are the points on the last image!
        self.QR_scanned = False #Tells if a QR is in the current vision
        self.zeppelin = zeppelin
        
    def run(self):
        while True:
            QR_strings = self.scanner.scan()
            if not QR_strings:
                self.QR_scanned = False
                continue
            elif len(QR_strings) is 1:
                self.QR_scanned = True
                
                QR_number = int(QR_strings[QR_strings.index('N')+ 2:])
                try: #Check for a new QR code
                    self.QR_points[QR_number]
                except KeyError:
                    #If it is a new one, calculate the points
                    self.calculate_points_QR(QR_number)
                
                self.QR_codes[QR_number] = QR_strings[0]
                
                img_file = self.new_file_name(QR_number)
                os.rename("/home/pi/tmp.jpg", img_file)
                self.QR_images[QR_number] = img_file
                
            elif len(QR_strings) > 1:
                #TODO: zoom stuff
                #This will probably not happen, leave it unimplemented
                continue
    
    def calculate_points_QR(self, number):
        #Returns the text string of the QR, is not very easy, it has to parse the .data output of the zxing QR objects.
        #This will call the zxing read function
        try:
            data = self.QRScanner.zxing_read(self.QR_images[number]).data 
            point_list = re.findall(r'[-+]?\d*\.\d+', data) #regex magic
            tuple_list = []
            for i in range(0,6,2):
                tuple_list[i/2] = (int(point_list[i]), int(point_list[i+1]))
            self.QR_points[number] = tuple_list
        except Exception as e:
            print e
    
    def calculate_angle(self,points,img):
        #On current QR
        (width, height) = img.size(img)
        x1,y1,x2,y2 = width/2, height, width/2, 0 #verticale lijn
        x3,y3,x4,y4 = points[1][0], points[1][1], points[0][0], points[0][1] #lijn tussen punten 0 en 1 
        dx1,dx2 = x2-x1,x4-x3
        dy1,dy2 = y2-y1,y4-y3
        d = dx1*dx2 + dy1*dy2
        l = (dx1*dx1 + dy1*dy1) * (dx2*dx2 + dy2*dy2)
        angle = math.degrees(math.acos(d/math.sqrt(l))) #hoek tussen de 2 rechte
        angle_zeppelin = 90 - angle 
        #snijpunt zoeken 
        c = dx1*dy2 - dy1*dx2
        a = x2*y1 - y2*x1
        b = x4*y3 - y4*x3
        x = (a * dx2 - b * dx1)/c
        if x > 300: 
            angle_zeppelin + 180
        return angle_zeppelin
        #TODO: Kijken of het snijpunt boven of onder het midden van de horizontale middelijn zit en in het ene geval +180
        
        
    
    def calculate_distance(self,points,img):
        (width_image, height_image) = img.size(img) 
        middle_x, middle_y = (points[0][0] + points[2][0])/2 , (points[0][1] + points[2][1])/2
        center_x, center_y = (points[1][0] + middle_x)/2 , (points[1][1] + middle_y)/2
        diff_x = ((400-center_x) * self.zeppelin.Heigth ) / 800 # - (neg) zeppling staat diff_x meters te ver naar rechts tov de QR-code
        diff_y = ((300-center_y) * self.zeppelin.Heigth * 1.33) / (600*2) # + (pos) zeppling staat te ver naar achter tov de QR-code
        return (diff_x,diff_y) 
    
    def new_file_name(self, number):
        img_file = "/home/pi/QR" + str(number) + ".jpg"
        return img_file
