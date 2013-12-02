#File for scanning QR codes

#TODO: test all the physical aspects, like resolution and what the zxing library returns

import zxing, threading
from subprocess import call
from PIL import Image

class Camera(object):
    
    def __init__(self):
        self.width = 800 #must always be in a 4:3 ratio
        self.height = 600

    def take_picture(self, img_file):
        call (["raspistill -w " + str(self.width) + " -h " + str(self.height) + " -q 75 " + " -t 0 -o " + img_file], shell=True)        
    

class QRScanner(object):
    
    def __init__(self):
        self.reader = zxing.BarCodeReader("/home/pi/zxing-1.6")
        self.camera = Camera()
        self.index = 1 #follows number
        self.current_img = ''
        
        
        
    def new_file_name(self):
        img_file = "/home/pi/img" + str(self.index) + ".jpg"
        self.index += 1
        
        return img_file
        
    def scan(self):
        #Scans for a QR code and returns the object, it is NONE when there isn't one found
        img_file = self.new_file_name()
        self.camera.take_picture(img_file)
        return self.read(img_file)
    
    def read(self, img_file):
        QRcode = self.reader.decode(img_file)
        return QRcode
        
    def zoom(self, number):
        img_file = "/home/pi/img" + str(number) + ".jpg"
        cropped_file = "/home/pi/cropped_img" + str(number) + ".jpg"
        
        img = Image.open(img_file)
        (width, height) = img.size(img)
        
        cropped_image = img.crop((50,50, width - 50, height - 50))
        cropped_image.save(cropped_file)
        
        QRcode = self.read(cropped_file)
        return QRcode
        

class QR(threading.Thread, object):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.QRcodes = {} #Key is the number of the QR code, the values are the objects.
        self.scanner = QRScanner()
        self.currentQR = 1
        
    def run(self):
        #take a picture every x seconds, scan it and 
        pass

        
    def scan_QR(self):
        QR = self.scanner.scan()
        #TODO: check for NONE and parse correctly!!!
        #Parse here, then for the number do: number = int(test[test.index("N")+ 2:])
        #TODO: check for right N, if not zoom pic by doing self.scanner.zoom(number), transfer new coordinates back to original height and width!
        pass
    
    def parseQR(self):
        #Returns the text string of the QR, this may be very easy depending on what the zxing library returns
        pass
    
    def calculate_angle(self):
        #On current QR
        pass
    
    def calculate_distance(self):
        #On current QR. When X meters in height, the width of the picture is X meters assuming 4:3 ratio
        pass