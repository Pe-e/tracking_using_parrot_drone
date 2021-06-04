import cv2
from cv2.data import haarcascades
import numpy as np
cars_cascade = cv2.CascadeClassifier('cars.xml') 
'''haarcascades + "haarcascade_fullbody.xml"''' 
current_click = []
bbox_target = []

last_flow = []

def detect(frame):
    targets = cars_cascade.detectMultiScale(frame, 1.15, 4)
    return targets

def track_object_with_detection(bbox,frame):
    for (x, y, w, h) in bbox:
        center = (x+int(w/2),y+int(h/2))
        cv2.circle(frame,center,3,(255, 0, 0), -1) 
        if(current_click != []):
            if(current_click[0] > x and current_click[0] < x+w):
                if(current_click[1] > y and current_click[1] < y+h):
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0, 255, 0),3)
                    cv2.putText(frame,'Target_detection',(x,y-2),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),2)
                    current_click.clear()
                    current_click.append(x+int(h/2))
                    current_click.append(y+int(w/2))
                    bbox_target.clear()
                    bbox_target.append(x)
                    bbox_target.append(y)
                    bbox_target.append(w)
                    bbox_target.append(h)



                    
    return frame


def click_on_target(event, x, y, flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        current_click.clear()
        current_click.append(x)
        current_click.append(y)
       


def get_optical_flow(frame_prev,frame):
    gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
    gray_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    prevPts =  cv2.goodFeaturesToTrack(gray_prev, mask = None,maxCorners = 50, qualityLevel = 0.2, minDistance = 5, blockSize = 7)
    next, status, error = cv2.calcOpticalFlowPyrLK(gray_prev, gray_frame,prevPts, None, winSize = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    print("next: ",next,"\n status: ",status,"error: ",error)
    return next, status, error, prevPts 

def track_object_with_optical_flow(next,status,frame,prev):
  
    good_old = prev[status == 1]
    good_new = next[status == 1]
    close_point = [0,0]
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        print(c,d)
        cv2.line(frame, (a, b), (c, d), (0,0,255), 2)
        cv2.circle(frame, (a, b), 3, (0,0,255), -1)
        if(bbox_target != []):
            if(a > bbox_target[0] and a < bbox_target[0]+ bbox_target[2]):
                if(b > bbox_target[1] and b < bbox_target[0] + bbox_target[3]):
                    
    
                    if((abs(bbox_target[0] - a), abs(bbox_target[1] - b)) < (abs(bbox_target[0] - close_point[0]), abs(bbox_target[1] - close_point[1]))):
                        close_point.clear()
                        close_point.append(a)
                        close_point.append(b)
                        close_point.append(c)
                        close_point.append(d)
    if( close_point != [0,0]):                           
        cv2.rectangle(frame,(int(close_point[0]-bbox_target[2]/2),int(close_point[1]-bbox_target[3]/2)),(int(close_point[0]+bbox_target[2]/2),int(close_point[1]+bbox_target[3]/2)),(0, 0, 255),3)
        cv2.putText(frame,'Target_optical_flow',(int(close_point[0]-bbox_target[2]/2),int(close_point[1]-bbox_target[3]/2)-2),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)
        current_click.clear()
        current_click.append(close_point[2])
        current_click.append(close_point[3])
        bbox_target[0] = close_point[2] -int(bbox_target[2]/2)
        bbox_target[1] = close_point[3] -int(bbox_target[3]/2)
                    
    return frame
            
 # soit target n'est pas detecte. return target
 # Sinon, on va retourner la boite anglobante la plus proche dans bbox
 # retourner mis a jour de target
 


if __name__ == '__main__' :
    print(0)
