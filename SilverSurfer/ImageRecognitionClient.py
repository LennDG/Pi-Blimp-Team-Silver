
import ImageRecognition as IR
from subprocess import call

class ImageRecognitionClient(object):
    
    def __init__(self):
        pass
    
    def start_daemon(self):
        IR.start_daemon()
    
    def generate_image(self):
        IR.generate_image()