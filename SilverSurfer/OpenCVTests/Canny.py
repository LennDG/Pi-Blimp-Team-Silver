import numpy as np
import cv2
import time
import math


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
lower_blue = np.array([90, 20, 10], dtype=np.uint8)
upper_blue = np.array([145, 180, 255], dtype=np.uint8)
blue = [lower_blue, upper_blue, 'blue']

#Define Yellow
lower_yellow = np.array([17, 100, 160], dtype=np.uint8)
upper_yellow = np.array([40, 255, 255], dtype=np.uint8)
yellow = [lower_yellow, upper_yellow, 'yellow']

#Define White
lower_white = np.array([0, 0, 200], dtype=np.uint8)
upper_white = np.array([180, 90, 255], dtype=np.uint8)
white = [lower_white, upper_white ,'white']

#Define Eliminated
lower_elim = np.array([0, 0, 0], dtype=np.uint8)
upper_elim = np.array([45, 255, 190], dtype=np.uint8)
elim = [lower_elim, upper_elim]

colors = [red_low, red_high, green, blue, yellow, white]



def closing(mask):
    kernel = np.ones((5,5),np.uint8) 
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return closing

def opening(mask):
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return opening

def cosine(point1, point2, point0):
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

def tuple_length(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    
    length = math.sqrt(dx**2 + dy**2)
    return length

def approx_length(point1, point2):
    dx = point1.item(0) - point2.item(0)
    dy = point1.item(1) - point2.item(1)
    
    length = math.sqrt(dx**2 + dy**2)
    return length

def analyse_approx(approx):
    
    cosines = []
    for i in range(0, len(approx) + 1):
        cos = cosine(approx[i%len(approx)], approx[(i-2)%len(approx)], approx[(i-1)%len(approx)])
        cosines.append(cos)
            
    
    
    duplicates = 0
    for i in range(0, len(approx)):
        for j in range(i+1, len(approx)):
            if approx_length(approx[i], approx[j]) <= 2:
                duplicates += 1
                if duplicates == 3:
                    return "Star"
                
    #Check for rectangles
    perp_count = 0.
    for cos in cosines:
        if abs(cos) < 0.1:
            perp_count += 1
    if perp_count > 2:
        return "Rectangle"
    
    #Count negatives
    negatives = 0. 
    for cos in cosines:
        if cos < 0:
            negatives += 1
            
    #Check star
    jumps = 0        
    for i in range(0, len(cosines) - 1):
        if abs(cosines[i] - cosines[i+1]) >= 0.6:
            jumps += 1
    if jumps >= 1 and negatives/len(cosines) < 0.7:
        return "Star"
    
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
    
    return "Undefined"

def canny(img_loc):
    
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
        contours = [contour for contour in contours if len(contour) >= 25]
        #Iterate over contours
        for contour in contours:
            #Approximate the contour, 0.025 is the magic value here
            approx = cv2.approxPolyDP(contour, 0.025*cv2.arcLength(contour, True), True)
            #Calculate area of enclosing circle
            center, radius = cv2.minEnclosingCircle(approx)
            area = radius**2*math.pi
            shape_name = analyse_approx(approx)            
            #Center locations
            M = cv2.moments(contour)
            if M['m00'] == 0.0:
                continue
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            
            valid = True
            if shape_name == "undefined":
                valid = False
            if area <= 1000:
                valid = False
            for figure in figures:
                if not valid:
                    break
                if abs(figure[2] - centroid_x) <= 50 and abs(figure[3] - centroid_y) <= 50:
                    if figure[4] > area:
                        valid = False
                        break
                    else:
                        figures.remove(figure)
                        break
            
            if valid:
                figure = (color[2], shape_name, centroid_x, centroid_y, area)
                figures.append(figure)
                cv2.drawContours(img, approx, -1, (0,0,0), thickness = 3)
            
    for figure in figures:
        cv2.putText(img, figure[0] + ' ' + figure[1] , (int(figure[2]), int(figure[3])),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    
    print figures
    
      
    cv2.namedWindow("image", 1)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    return figures
        
canny("qr2.jpg")
def cannytest(times):
    time_avg = []
    for i in range(0, times):
        tic = time.time()
        canny("test2.jpeg")
        toc = time.time()
    time_avg.append(toc-tic)      
    print np.mean(time_avg)

#cannytest(100)

    
    