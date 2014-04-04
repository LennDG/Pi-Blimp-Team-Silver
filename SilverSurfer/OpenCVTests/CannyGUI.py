from Tkinter import *
import cv2
from cv2 import cv
import numpy as np
import math

# Take image
img = cv2.imread("image.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
screen_res = 1280, 720
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)


master = Tk()
thr1 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
thr1.pack()
thr2 = Scale(master, from_=0, to=255, length = 600, orient=HORIZONTAL)
thr2.pack()

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
    
    #Calculate variance
    avg_cos = np.mean(cosines)
    variance = 0
    for cos in cosines:
        variance += (avg_cos - cos) ** 2
    variance = variance/len(cosines)
    #Check circle or heart
    if negatives/len(cosines) >= 0.8:
        #Cirle or heart
        if variance < 0.02:
            return "circle"
        else:
            return "heart"        
    #Check star
    if 0.3 <= negatives/len(cosines) <= 0.7:
        if variance > 0.2:
            return "Star"
    
    return "Undefined"

def showCanny():
    res = img.copy()
    blur = cv2.blur(img, (3,3))
    canny = cv2.Canny(gray, thr1.get(), thr2.get())
    kernel = np.ones((3,3), dtype= np.uint8)
    canny = cv2.dilate(canny, kernel)
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w +2), np.uint8)
    cv2.floodFill(canny, mask, (40,300), (255, 255, 255))
    
    contours, h = cv2.findContours(canny.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [contour for contour in contours if len(contour) >= 50]
    for contour in contours:    
        approx = cv2.approxPolyDP(contour, 0.02*cv2.arcLength(contour, True), True)
        try:
            shape_name = analyse_approx(approx)
        except ZeroDivisionError:
            pass
        M = cv2.moments(contour)
        if M['m00'] == 0.0:
            continue
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
        
        cv2.putText(res, shape_name + '(' + str(len(approx)) + ')', (centroid_x, centroid_y),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))   
        cv2.drawContours(res, approx, -1, (0,0,255), thickness = 3)
    
    cv2.imshow("result", res)    
    cv2.imshow('gray',gray)
    cv2.imshow('Canny', canny)
    
    master.after(100, showCanny)
    
master.after(1000,showCanny)
master.mainloop()
    
    