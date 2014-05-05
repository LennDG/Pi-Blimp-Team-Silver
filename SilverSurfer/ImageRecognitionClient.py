
import ImageRecognition as IR
from subprocess import call
import time, urllib

class ImageRecognitionClient(object):
    
    def __init__(self):
        pass
    
    def start_daemon(self):
        IR.start_daemon()
    
    def generate_image(self):
        return IR.generate_image()
    
    def generate_QR_code(self, private_key, filename = '/run/shm/QR.jpg'):
        #Start a timer
        tic = time.time()
        
        if filename == '/run/shm/QR.jpg':
            #Take picture
            IR.take_picture(filename)
        else:
            filename = urllib.urlretrieve(filename)[0]
        
        #Read text
        text = IR.decode_qrcode(filename,private_key)
        
        #Keep trying to take picture for 5 seconds if it is not found
        while text is None:
            time.sleep(0.8)
            IR.take_picture(filename)
            text = IR.decode_qrcode(filename, private_key)
            if time.time() - tic > 5:
                #Can't read QR code, stop trying
                return 0            
        return text
