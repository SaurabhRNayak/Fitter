import cv2
import numpy as np

def func(val):
    cap = cv2.VideoCapture(0)
    flg=True
    active=True
    count=0
    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low_ = np.array([25, 52, 72])
        high_ = np.array([102, 255, 255])
        mask = cv2.inRange(hsv_frame, low_, high_)
        layer = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("layer", layer)
        # print(np.shape(mask))
        points = cv2.findNonZero(mask)
        # print(points)
        avg = np.mean(points, axis=0)
        avg=avg[0]
        # print(avg)
        resImage = [640, 480]
        resScreen = [640, 480]

        # points are in x,y coordinates
        pointInScreen = ((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
        # print(pointInScreen[1])
        if pointInScreen[1]>330 and active==True:
            count+=1
            active=False
        if pointInScreen[1]<190 and active==False:
            active=True
        print(count)
        cv2.putText(frame,"Count"+str(count),(50, 50),cv2.FONT_HERSHEY_SIMPLEX , 1,(0, 255, 255),2,cv2.LINE_4) 
        cv2.imshow("video", frame)
        if count==val:
            return("Done")
        key = cv2.waitKey(1)
        if key == 27:
            break

if __name__=="__main__":
    print(func(15))
