
import ImageRecognition as IR
from subprocess import call

class ImageRecognitionClient(object):
    
    def __init__(self):
        pass
    
    def start_daemon(self):
        IR.start_daemon()
    
    def generate_image(self):
        return IR.generate_image()
    
    def generate_QR_code(self):
         #Start a timer
        tic = time.time()
        
        #Take picture
        IR.take_picture("/run/shm/QR.jpg")
        
        #Read text
        text = IR.decode_qrcode("/run/shm/QR.jpg")
        
        #Keep trying to take picture for 5 seconds if it is not found
        while text is None:
            IR.take_picture("/run/shm/QR.jpg")
            text = IR.decode_qrcode("/run/shm/QR.jpg")
            if time.time() - tic > 5:
                #Can't read QR code, stop trying
                return 0
        return text
