from Tkinter import *
import cv2
from cv2 import cv
import numpy as np
import math

# Take image
img = cv2.imread("PiPics/1m4.jpg")

# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

screen_res = 1280, 720
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)


master = Tk()
h1 = Scale(master, from_=0, to=180, length = 600, orient=HORIZONTAL)
h1.pack()
s1 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
s1.pack()
v1 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
v1.pack()

h2 = Scale(master, from_=0, to=180, length = 600, orient=HORIZONTAL)
h2.pack()
s2 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
s2.pack()
v2 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
v2.pack()

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

def analyse_approx(approx):
    
    cosines = []
    for i in range(0, len(approx) + 1):
        cos = cosine(approx[i%len(approx)], approx[(i-2)%len(approx)], approx[(i-1)%len(approx)])
        cosines.append(cos)
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
    if jumps >= 2 and negatives/len(cosines) < 0.7:
        return "star"
    
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

def showHSV():
    lower = np.array([h1.get(), s1.get(), v1.get()], dtype=np.uint8)
    upper = np.array([h2.get(), s2.get(), v2.get()], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower,upper)

    res = cv2.bitwise_and(img,img, mask= mask)
    #mask = closing(mask)
    #mask = opening(mask)
    
    canny = cv2.Canny(mask, 0, 1)
    
    contours, h = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [contour for contour in contours if len(contour) >= 30]
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.025*cv2.arcLength(contour, True), True)
        M = cv2.moments(contour)        
        try:
            shape_name = analyse_approx(approx)
        except ZeroDivisionError:
            pass
        
        if M['m00'] == 0.0:
            continue
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
               
    
        cv2.putText(res, shape_name + '(' + str(len(approx)) + ') size' + (str(len(approx))), (centroid_x, centroid_y),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))   
        cv2.drawContours(res, approx, -1, (0,0,255), thickness = 3)
    
    
    
    
    cv2.imshow('feed',img)
    cv2.imshow('Canny', canny)
    cv2.imshow('Result',res)
    
    master.after(100, showHSV)   

master.after(2000,showHSV)
master.mainloop()
#Button(master, text='Show', command=show_values).pack()
