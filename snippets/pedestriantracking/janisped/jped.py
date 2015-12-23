# good refs -
#https://github.com/julierthanjulie/PedestrianTracking

import cv2
import numpy as np
import sys
import math
from requests_futures.sessions import FuturesSession
import threading
from random import randint
# the cascade for pedistrians (in same directory)
cascPath = 'hogcascade_pedestrians.xml'
pedCascade = cv2.CascadeClassifier(cascPath)
# start a video capture using default camera
video_capture = cv2.VideoCapture(0)
#add globals for lights
light_x = 0
light_y = 0
lightsON = False


# A timer which sends xy coords to the light
def SendXY():
    # make sure variables aren't NoneTypes and if they are change that
    # if finger_x is None:
    #     finger_x = 55 #assign a number inbetween range
    # if finger_y is None:
    #     finger_y = 80
    # convert to strings
    xsend = str(int(light_x))
    ysend = str(int(light_y))
    Channel[0] = xsend
    Channel[2] = ysend
    
    if lightsON is True:
        Channel[5] = '255'
    else:
        Channel[5] = '0'

    Channel[7] = '255'
    Channel[8] = '0'#str(randint(0,255))
    Channel[9] = '0' #str(randint(0,255))
    Channel[10] = '0' #str(randint(0,255))
    # print Channel
    myString = ",".join(Channel)
    payload={'u':'0','d': myString}
    future_one = session.post("http://raspberrypi.local:9090/set_dmx", data=payload)
    t = threading.Timer(0.8, SendXY)
    t.daemon = True #this shit kills the thread when the program finishes..
    t.start()

#translate one value range to another
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# here will be where the aysnc posts will be initiated
def sequencers():
    SendXY()
    # pass
#start the posts
sequencers()
#do an infinite loop
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    screen = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)
    # convert to BW
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    people = pedCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # an empty list which will fill up with location of people
    points = []
    # for each person you see do something
    for i, (x, y, w, h) in enumerate(people):
        # draw a rectangle round them
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # draw a dot in the middle of them...
        cv2.circle(screen,(x+w/2,y+h/2), 5, (255,255,255), -1)
        # add their location to the list
        points.insert(i, (x+w/2,y+h/2))
    # if the list is empty
    if not points:
        # print "no people"
        pass
    else:
        # peoples locations
        #print points
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        #find centre of group of people
        centroid = (sum(x) / len(points), sum(y) / len(points))
        print centroid
        # find the person furthest from the centre
        furthest = max(points, key=lambda point: math.hypot(point[0]-centroid[0], point[1]-centroid[1]))
        #find the distance between the centroid and furthest person.
        radius = math.hypot(centroid[0] - furthest[0], centroid[1] - furthest[1])
        # draw a circle to the limit of cluster of people by the person who is furthest away
        cv2.circle(screen, (centroid[0],centroid[1]), int(radius), (0,0,255), 1)
        #deliver points to the program
        lightsON = True
        light_x = translate(centroid[0], 0, frame.shape[0], 0, 125)
        light_y = translate(centroid[1], 0, frame.shape[1], 0, 125)

    # Display the resulting frame
    cv2.imshow('Tracker', screen)
    # if i press q leave the infinite loop
    if cv2.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()