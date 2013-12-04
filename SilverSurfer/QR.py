#File for scanning QR codes

#TODO: test all the physical aspects, like resolution and what the zxing library returns

import zxing, threading, zbar, os
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
        
    def zoom(self, img_file):
        cropped_file = "/home/pi/cropped_img.jpg"
        
        img = Image.open(img_file)
        (width, height) = img.size(img)
        
        cropped_image = img.crop((50,50, width - 50, height - 50))
        cropped_image.save(cropped_file)
        
        QRcode = self.read(cropped_file)
        return QRcode
        

class QR(threading.Thread, object):
    
    def __init__(self, zeppelin):
        threading.Thread.__init__(self)
        
        self.QR_codes = {} #Key is the number of the QR code, the values are the data strings.
        self.QR_images = {} #Key is number of the QR, values are the image files
        self.QR_points = {} #Key is the number of the QR, values are the points on the last image!
        self.scanner = QRScanner()
        self.currentQR = 1
        
        self.zeppelin = zeppelin
        
    def run(self):
        while True:
            QR_strings = self.scanner.scan()
            if not QR_strings:
                continue
            elif len(QR_strings) is 1:
                QR_number = int(QR_strings[QR_strings.index('N')+ 2:])
                self.QR_codes[QR_number] = QR_strings[0]
                
                img_file = self.new_file_name(QR_number)
                os.rename("/home/pi/tmp.jpg", img_file)
                self.QR_codes[QR_number] = img_file
                
            elif len(QR_strings) > 1:
                #TODO: zoom stuff
                pass  
            
            
            
        pass
    
    def get_points_QR(self, number):
        #Returns the text string of the QR, this may be very easy depending on what the zxing library returns
        pass
    
    def calculate_angle(self):
        #On current QR
        pass
    
    def calculate_distance(self):
        #On current QR. When X meters in height, the width of the picture is X meters assuming 4:3 ratio
        pass
    
    def new_file_name(self, number):
        img_file = "/home/pi/QR" + str(number) + ".jpg"
        return img_file