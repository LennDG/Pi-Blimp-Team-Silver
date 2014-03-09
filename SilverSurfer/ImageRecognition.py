import numpy as np
import time
import cv2
import math
from subprocess import call

#Define location of the image, will probably change to memory instead of disk
img_loc = "/home/pi/image.jpg"

#Define high Red
lower_red = np.array([150, 70, 70], dtype=np.uint8)
upper_red = np.array([180, 255, 255], dtype=np.uint8)
red_high = [lower_red, upper_red, 'red']

#Define low Red
lower_red = np.array([0, 70, 70], dtype=np.uint8)
upper_red = np.array([10, 255, 255], dtype=np.uint8)
red_low = [lower_red, upper_red, 'red']

#Define Green
lower_green = np.array([40, 20, 0], dtype=np.uint8)
upper_green = np.array([90, 180, 255], dtype=np.uint8)
green = [lower_green, upper_green, 'green']

#Define Blue
lower_blue = np.array([90, 0, 10], dtype=np.uint8)
upper_blue = np.array([130, 180, 255], dtype=np.uint8)
blue = [lower_blue, upper_blue, 'blue']

#Define Yellow
lower_yellow = np.array([17, 100, 160], dtype=np.uint8)
upper_yellow = np.array([40, 255, 255], dtype=np.uint8)
yellow = [lower_yellow, upper_yellow, 'yellow']

#Define White
lower_white = np.array([0, 0, 200], dtype=np.uint8)
upper_white = np.array([180, 40, 255], dtype=np.uint8)
white = [lower_white, upper_white ,'white']

colors = [red_low, red_high, green, blue, yellow, white]

def start_daemon():
    call(["/home/pi/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/start_camd.sh " + img_loc], shell=True)  

def take_picture():
    call(["/home/pi/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/do_caputure.sh"], shell=True)
    return time.time()

def cosine(point1, point2, point0):
    #Math magic... works!
    dx1 = point1.item(0) - point0.item(0)
    dy1 = point1.item(1) - point0.item(1)
    dx2 = point2.item(0) - point0.item(0)
    dy2 = point2.item(1) - point0.item(1)
    
    size1 = math.sqrt(dx1*dx1 + dy1*dy1)
    size2 = math.sqrt(dx2*dx2 + dy2*dy2)
    
    vec1 = np.array([dx1/size1, dy1/size1])
    vec2 = np.array([dx2/size2, dy2/size2])
    
    cos = np.dot(vec1, vec2)
    return cos

def analyse_approx(approx):
    
    cosines = []
    #Calculate cosines of the corners
    for i in range(0, len(approx) + 1):
        cos = cosine(approx[i%len(approx)], approx[(i-2)%len(approx)], approx[(i-1)%len(approx)])
        cosines.append(cos)
    #Check for rectangles
    perp_count = 0.
    for cos in cosines:
        if abs(cos) < 0.1:
            perp_count += 1
    if perp_count >= 2:
        return "rectangle"
    
    #Count negatives
    negatives = 0. 
    for cos in cosines:
        if cos < 0:
            negatives += 1
    
    #Calculate variance
    avg_cos = np.mean(cosines)
    variance = 0
    for cos in cosines:
        variance += (avg_cos - cos) ** 2
    variance = variance/len(cosines)
    #Check circle or heart
    if negatives/len(cosines) >= 0.8:
        #Cirle or heart
        if variance < 0.01:
            return "circle"
        else:
            return "heart"        
    #Check star
    if 0.3 <= negatives/len(cosines) <= 0.7:
        if variance > 0.2:
            return "star"
    
    return "undefined"

def detect_targets():
    
    figures = []
    #Read image
    img = cv2.imread(img_loc)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Iterate over masks
    for color in colors:   
        mask = cv2.inRange(hsv, color[0], color[1]) 
        canny = cv2.Canny(mask, 0, 1)
        
        #Find outer contours and use only the larger ones
        contours, h = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [contour for contour in contours if len(contour) >= 30]
        #Iterate over contours
        for contour in contours:
            #Approximate the contour, 0.025 is the magic value here
            approx = cv2.approxPolyDP(contour, 0.025*cv2.arcLength(contour, True), True)
            shape_name = analyse_approx(approx)            
            #Center locations
            M = cv2.moments(contour)
            if M['m00'] == 0.0:
                continue
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])

            figure = (color[2], shape_name, centroid_x, centroid_y)
            figures.append(figure)
            
    #Remove duplicate figures
    for figure1 in figures:
        for figure2 in figures:
            if abs(figure1[2]-figure2[2]) <= 50 and abs(figure1[3]-figure2[3]) <= 50 and figure1 != figure2:
                figures.remove(figure2)
    for figure in figures:
        if figure[1] == 'undefined':
            figures.remove(figure)
    return figures


def generate_image():
    time_stamp = take_picture()
    targets = detect_targets()
    zeppelin_image = (250,250) # We'll have to program this a bit more flexible not hardcoded.
    return targets, zeppelin_image, time_stamp


    
    