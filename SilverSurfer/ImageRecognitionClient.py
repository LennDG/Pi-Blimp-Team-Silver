
import ImageRecognition as IR
from subprocess import call

class ImageRecognitionClient(object):
    
    def __init__(self):
        pass
    
    def start_daemon(self):
        IR.start_daemon()
    
    def generate_image(self):
        return IR.generate_image()
    
    def take_picture(self, img_loc):
        IR.take_picture(img_loc)
        
    def decode_qrcode(self, img_loc):
        return IR.decode_qrcode(img_loc)
        