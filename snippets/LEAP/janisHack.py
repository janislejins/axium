################################################################################
# Copyright (C) 2015 Janis Lejins, Inc. All rights reserved.                   #
# This is a calibration program for an upcoming artwork
# It is used to map the data from a leap motion controller to a DMX light via OLA
################################################################################
 
import Leap, sys, thread, time
import threading
from random import randint
from requests_futures.sessions import FuturesSession
import struct
#global variables
finger_x = 0
finger_y = 0
lightsON = True
# X & Y for the channel
Channel = ['0','0','0','0','0','0','0','0','0','0','0','0','0']
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        if frame.hands.is_empty:
            #Process hands...
            global lightsON
            lightsON = False
        else:
            global lightsON
            lightsON = True
        # Get hands
        for hand in frame.hands:
            #find the left hand
            if hand.is_left:
                # Get fingers
                for finger in hand.fingers:
                    # find the index finger 0 = thumb, 4 = pinky
                    if finger.type is 1:
                        # Get the distal phalanx (the tip of the finger)
                        bone = finger.bone(3) 
                        # BONE.DIRECTION RETURNS AN XYZ  VALUE FOR THE FINGER FROM THE CENTER OF THE CONTROLLER
                        # ATM WE DON'T NEED Z (HOW FAR FORWARD OR BACK IT IS) - Could do brightness
                        # print "x="+str(translate(bone.direction[0], -1.0, 1.0, 125, 255))
                        # print "y="+str(translate(bone.direction[1], -1.0, 1.0, 125, 255))
                        global finger_x
                        global finger_y
                        # map the range of movement of finger to light
                        #the bone direction is mapped relative to the hand so the light is tip of finger...
                        finger_x = translate(bone.direction[0], -1.0, 1.0, 0, 66)
                        finger_y = translate(bone.direction[1], -1.0, 1.0, 100, 10)


def SendXY():
    # make sure variables aren't NoneTypes and if they are change that
    # if finger_x is None:
    #     finger_x = 55 #assign a number inbetween range
    # if finger_y is None:
    #     finger_y = 80
    # convert to strings
    xsend = str(int(finger_x))
    ysend = str(int(finger_y))
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

while True:
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    # create future session for async requests
    session = FuturesSession()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    #send the coordinates async
    SendXY()
    infinity = float("inf")
# time.sleep(10000000)
# Remove the sample listener when done
controller.remove_listener(listener)
# quit the program, kills all threads - if they are set to Thread.daemon = True
quit()
