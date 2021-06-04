import cv2
from cv2.data import haarcascades
import numpy as np
cars_cascade = cv2.CascadeClassifier("cars.xml")
current_click = []
last_targets = []

last_flow = []

def detect(frame):
    targets = cars_cascade.detectMultiScale(frame, 1.15, 4)
    return targets

def track_object_with_detection(bbox,frame):
    for (x, y, h, w) in bbox:
        center = (x+int(w/2),y+int(h/2))
        cv2.circle(frame,center,3,(255, 0, 0), -1) 
        if(current_click != []):
            if(current_click[0] > x and current_click[0] < x+w):
                if(current_click[1] > y and current_click[1] < y+h):
                    cv2.rectangle(frame,(x,y),(x+h,y+w),(0, 255, 0),2)
                    current_click.clear()
                    current_click.append(x+int(h/2))
                    current_click.append(y+int(w/2))

                    
    return frame

def click_on_target(event, x, y, flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        current_click.clear()
        current_click.append(x)
        current_click.append(y)
       


def get_optical_flow(frame_prev,frame):
    gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
    gray_frame= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #prevPts = cv2.goodFeaturesToTrack(gray_prev, mask = None,maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
    flow = cv2.calcOpticalFlowFarneback(gray_prev, gray_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    print(flow)
    return flow 

def track_object_with_optical_flow(flow,mask,frame):
    
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    output = cv2.add(frame, rgb)
    return output
            
 # soit target n'est pas detecte. return target
 # Sinon, on va retourner la boite anglobante la plus proche dans bbox
 # retourner mis a jour de target
 


if __name__ == '__main__' :
    print(0)
