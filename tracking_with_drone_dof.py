import cv2
from first_detection_dof   import *
import numpy as np
CarVideo = cv2.VideoCapture('cars.mp4')
first = CarVideo.read()[1]
prev_frame = first
velocity = False
flow = []
frame_optical_flow = []
mask = np.zeros_like(first)
mask[..., 1] = 255
while CarVideo.isOpened():
    
    
    ret, frame = CarVideo.read()
    controlkey = cv2.waitKey(1)

    if ret:
        
        detected_targets = detect(frame)  
        detected_frame = track_object_with_detection(detected_targets,frame)
        cv2.setMouseCallback('frame',click_on_target)
        if(velocity == True):
            flow = get_optical_flow(prev_frame,frame)                   
            if(flow != []):
                frame_optical_flow = track_object_with_optical_flow(flow,mask,detected_frame)
        if(frame_optical_flow == []):
            cv2.imshow('frame',detected_frame)
        else:
            cv2.imshow('frame',frame_optical_flow)

        
                        
        prev_frame = frame.copy()
        velocity = True
        if controlkey == ord('q'):
            break 
        
        
        
    else:
        break
    
    
    
    
        
    
CarVideo.release()
cv2.destroyAllWindows()
   
                              