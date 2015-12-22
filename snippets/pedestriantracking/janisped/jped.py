import cv2
import numpy as np
import sys
import math
# the cascade for pedistrians (in same directory)
cascPath = 'hogcascade_pedestrians.xml'
pedCascade = cv2.CascadeClassifier(cascPath)
# start a video capture using default camera
video_capture = cv2.VideoCapture(0)
#add globals for lights
# here will be where the aysnc posts will be initiated
def sequencers():
    pass
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
    # Display the resulting frame
    cv2.imshow('Tracker', screen)
    # if i press q leave the infinite loop
    if cv2.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()