#!/usr/bin/env python2.7
# Marvin, The Raspberry Pi Controlled Go-Kart!
# 2-wheeled robot control software
# with wireless PS3 controller interface
# Based on MicroPiNoon robots
# Modified for golf trolley controller

import RPi.GPIO as GPIO # Import the GPIO Library
import pygame
import time
import os
import sys

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GolfTrolley interface
PinMotorCtrl1 = 27
PinMotorCtrl2 = 10
PinMotorCtrl3 = 11
PinMotorCtrl4 = 5
PinMotorCtrl5 = 19

# Setup I/O for GolfTrolley interface
GPIO.setup(PinMotorCtrl1, GPIO.OUT)
GPIO.setup(PinMotorCtrl2, GPIO.OUT)
GPIO.setup(PinMotorCtrl3, GPIO.OUT)
GPIO.setup(PinMotorCtrl4, GPIO.OUT)
GPIO.setup(PinMotorCtrl5, GPIO.OUT)
GPIO.output(PinMotorCtrl1, False)
GPIO.output(PinMotorCtrl2, False)
GPIO.output(PinMotorCtrl3, False)
GPIO.output(PinMotorCtrl4, False)
GPIO.output(PinMotorCtrl5, False)

interval = 0.00                         # Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
global hadEvent
global LeftStickUp
global LeftStickDown
global LeftStickLeft
global LeftStickRight
global RightStickUp
global RightStickDown
global RightStickLeft
global RightStickRight
global HatStickUp
global HatStickDown
global HatStickLeft
global HatStickRight
global TriangleButton
global SquareButton
global CircleButton
global XButton
global HomeButton
global StartButton
global SelectButton
global R1Button
global R2Button
global R3Button
global L1Button
global L2Button
global L3Button
global moveQuit
hadEvent = True
LeftStickUp = False
LeftStickDown = False
LeftStickLeft = False
LeftStickRight = False
RightStickUp = False
RightStickDown = False
RightStickLeft = False
RightStickRight = False
HatStickUp = False
HatStickDown = False
HatStickLeft = False
HatStickRight = False
TriangleButton = False
SquareButton = False
CircleButton = False
XButton = False
HomeButton = False
StartButton = False
SelectButton = False
R1Button = False
R2Button = False
R3Button = False
L1Button = False
L2Button = False
L3Button = False
moveQuit = False

# Needed to allow PyGame to work without a monitor
os.environ["SDL_VIDEODRIVER"]= "dummy"

#Initialise pygame & controller(s)
pygame.init()
print 'Waiting for joystick... (press CTRL+C to abort)'
while True:
    try:
        try:
            pygame.joystick.init()
            # Attempt to setup the joystick
            if pygame.joystick.get_count() < 1:
                # No joystick attached, toggle the LED
                #ZB.SetLed(not ZB.GetLed())
                pygame.joystick.quit()
                time.sleep(0.1)
            else:
                # We have a joystick, attempt to initialise it!
                joystick = pygame.joystick.Joystick(0)
                break
        except pygame.error:
            # Failed to connect to the joystick, toggle the LED
            #ZB.SetLed(not ZB.GetLed())
            pygame.joystick.quit()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # CTRL+C exit, give up
        print '\nUser aborted'
        #ZB.SetLed(True)
        sys.exit()
print 'Joystick found'
joystick.init()

print 'Initialised Joystick : %s' % joystick.get_name()

if "Rock Candy" in joystick.get_name():
    print ("Found Rock Candy Wireless PS3 controller")
    # pygame controller constants (Rock Candy Controller)
    JoyButton_Square = 0
    JoyButton_X = 1
    JoyButton_Circle = 2
    JoyButton_Triangle = 3
    JoyButton_L1 = 4
    JoyButton_R1 = 5
    JoyButton_L2 = 6
    JoyButton_R2 = 7
    JoyButton_Select = 8
    JoyButton_Start = 9
    JoyButton_L3 = 10
    JoyButton_R3 = 11
    JoyButton_Home = 12
    axisUpDown = 1                          # Joystick axis to read for up / down position
    axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
    axisLeftRight = 0                       # Joystick axis to read for left / right position
    axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
else:
    print (" The other cheap Wireless PS3 controller")
    # pygame controller constants (ShanWan PC/PS3/Android)
    JoyButton_A = 0
    JoyButton_B = 1
    JoyButton_X = 3
    JoyButton_Y = 4
    JoyButton_R1 = 7
    JoyButton_L1 = 6
    JoyButton_R2 = 9
    JoyButton_L2 = 8
    JoyButton_Select = 10
    JoyButton_Start = 11
    JoyButton_L3 = 13
    JoyButton_R3 = 14
    axisUpDown = 1                          # Joystick axis to read for up / down position
    axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
    axisLeftRight = 0                       # Joystick axis to read for left / right position
    axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
    JoyButton_Circle = 999                  # Not supported on this controller
    JoyButton_Home = 999                    # Not supported on this controller


# Check number of joysticks in use...
joystick_count = pygame.joystick.get_count()
print("joystick_count")
print(joystick_count)
print("--------------")

# Check number of axes on joystick...
numaxes = joystick.get_numaxes()
print("numaxes")
print(numaxes)
print("--------------")

# Check number of buttons on joystick...
numbuttons = joystick.get_numbuttons()
print("numbuttons")
print(numbuttons)

# Pause for a moment...
time.sleep(2)


# Turn all motors off
def StopMotors():
    print("StopMotors")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, False)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, False)
    GPIO.output(PinMotorCtrl5, False)

def AccForwards():
    print("AccForwards")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, True)
    GPIO.output(PinMotorCtrl5, False)

    time.sleep(0.3)
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, False)
    GPIO.output(PinMotorCtrl5, False)

    time.sleep(0.3)

def AccBackwards():
    print("AccBackwards")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, True)
    GPIO.output(PinMotorCtrl5, False)

    time.sleep(0.3)    
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, False)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, True)
    GPIO.output(PinMotorCtrl5, False)

    time.sleep(0.3)    

def Forwards():
    print("Forwards")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, False)
    GPIO.output(PinMotorCtrl5, False)

def Backwards():
    print("Backwards")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, False)
    GPIO.output(PinMotorCtrl3, True)
    GPIO.output(PinMotorCtrl4, True)
    GPIO.output(PinMotorCtrl5, False)

def Left():
    print("Left")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, False)
    GPIO.output(PinMotorCtrl4, True)
    GPIO.output(PinMotorCtrl5, False)

def Right():
    print("Right")
    GPIO.output(PinMotorCtrl1, True)
    GPIO.output(PinMotorCtrl2, True)
    GPIO.output(PinMotorCtrl3, False)
    GPIO.output(PinMotorCtrl4, False)
    GPIO.output(PinMotorCtrl5, False)


# Pause for a moment...
time.sleep(2)


def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global LeftStickUp
    global LeftStickDown
    global LeftStickLeft
    global LeftStickRight
    global RightStickUp
    global RightStickDown
    global RightStickLeft
    global RightStickRight
    global HatStickUp
    global HatStickDown
    global HatStickLeft
    global HatStickRight
    global TriangleButton
    global SquareButton
    global CircleButton
    global XButton
    global HomeButton
    global StartButton
    global SelectButton
    global R1Button
    global R2Button
    global R3Button
    global L1Button
    global L2Button
    global L3Button
    global moveQuit

    # Handle each event individually
    for event in events:
        #print ("Event: ", event)
        if event.type == pygame.QUIT:
            print ("QUIT")
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.JOYHATMOTION:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            print ("Hat Motion: ", event.value)
            hat = joystick.get_hat(0)
            # Hat up/down
            if hat[0] == -1:
                HatStickLeft = True
            elif hat[0] == 1:
                HatStickRight = True
            else:
                HatStickLeft = False
                HatStickRight = False
            # Hat left/right
            if hat[1] == -1:
                HatStickDown = True
            elif hat[1] == 1:
                HatStickUp = True
            else:
                HatStickDown = False
                HatStickUp = False
            
        elif event.type == pygame.JOYBUTTONDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            print ("Button Down: ", event.button)
            if event.button == JoyButton_Square:
                SquareButton = True
            elif event.button == JoyButton_X:
                XButton = True
            elif event.button == JoyButton_Circle:
                CircleButton = True
            elif event.button == JoyButton_Triangle:
                TriangleButton = True
            elif event.button == JoyButton_L1:
                L1Button = True
            elif event.button == JoyButton_R1:
                R1Button = True
            elif event.button == JoyButton_L2:
                L2Button = True
            elif event.button == JoyButton_R2:
                R2Button = True
            elif event.button == JoyButton_L3:
                L3Button = True
            elif event.button == JoyButton_R3:
                R3Button = True
            elif event.button == JoyButton_Select:
                SelectButton = True
            elif event.button == JoyButton_Start:
                StartButton = True
            elif event.button == JoyButton_Home:
                HomeButton = True
        elif event.type == pygame.JOYBUTTONUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            #print ("Button Up: ", event.button)
            if event.button == JoyButton_Square:
                SquareButton = False
            elif event.button == JoyButton_X:
                XButton = False
            elif event.button == JoyButton_Circle:
                CircleButton = False
            elif event.button == JoyButton_Triangle:
                TriangleButton = False
            elif event.button == JoyButton_L1:
                L1Button = False
            elif event.button == JoyButton_R1:
                R1Button = False
            elif event.button == JoyButton_L2:
                L2Button = False
            elif event.button == JoyButton_R2:
                R2Button = False
            elif event.button == JoyButton_L3:
                L3Button = False
            elif event.button == JoyButton_R3:
                R3Button = False
            elif event.button == JoyButton_Select:
                SelectButton = False
            elif event.button == JoyButton_Start:
                StartButton = False
            elif event.button == JoyButton_Home:
                HomeButton = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            # Invert any axes which are incorrect
            if axisUpDownInverted:
                upDown = -upDown
            if axisLeftRightInverted:
                leftRight = -leftRight
            # Determine Up / Down values
            if upDown < -0.1:
                print ("LeftStickUp")
                LeftStickUp = True
                LeftStickDown = False
            elif upDown > 0.1:
                print ("LeftStickDown")
                LeftStickUp = False
                LeftStickDown = True
            else:
                LeftStickUp = False
                LeftStickDown = False
            # Determine Left / Right values
            if leftRight < -0.1:
                print ("LeftStickLeft")
                LeftStickLeft = True
                LeftStickRight = False
            elif leftRight > 0.1:
                print ("LeftStickRight")
                LeftStickLeft = False
                LeftStickRight = True
            else:
                LeftStickLeft = False
                LeftStickRight = False

        
print("Starting PS3Bot - entering control loop...")

        
# Allow module to settle
time.sleep(0.5)


try:
    print 'Press Ctrl-C to quit'
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif HomeButton and CircleButton: # Shutdown
                print ("Halting Raspberry Pi...")
                GPIO.cleanup()
                bashCommand = ("sudo halt")
                os.system(bashCommand)
                break
            elif HomeButton and TriangleButton: # Reboot
                print ("Rebooting Raspberry Pi...")
                GPIO.cleanup()
                bashCommand = ("sudo reboot now")
                os.system(bashCommand)
                break
            elif HomeButton and XButton: # Exit
                print ("Exiting program...")
                break
            elif StartButton and CircleButton: 
                print ("Start Line-follower")
                #do_linefollower()
            elif StartButton and SquareButton: 
                print ("Start Proximity")
                #do_proximity()
            elif StartButton and XButton: 
                print ("Start Avoidance")
                #do_proximity()
            elif SelectButton:
                print ("Select")
            elif SquareButton:
                print ("Square")
            elif XButton:
                print ("X")
            elif CircleButton:
                print ("Circle")
            elif TriangleButton:
                print ("Triangle")
            elif L1Button:
                print ("L1")
            elif R1Button:
                print ("R1")
                AccForwards()
            elif L2Button:
                print ("L2")
            elif R2Button:
                print ("R2")
                AccBackwards()
            elif L3Button:
                print ("L3")
            elif R3Button:
                print ("R3")
            #elif LeftStickLeft and LeftStickUp:
            #    piz_moto.FLeft(1,0)
            #elif LeftStickLeft and LeftStickDown:
            #    piz_moto.BLeft(1,0)
            #elif LeftStickRight and LeftStickUp:
            #    piz_moto.FRight(1,0)
            #elif LeftStickRight and LeftStickDown:
            #    piz_moto.BRight(1,0)
            elif LeftStickLeft:
                Left()
            elif LeftStickRight:
                Right()
            elif LeftStickUp:
                Forwards()
            elif LeftStickDown:
                Backwards()
            elif RightStickLeft:
                print ("Right Stick Left")
            elif RightStickRight:
                print ("Right Stick Right")
            elif RightStickUp:
                print ("Right Stick Up")
            elif RightStickDown:
                print ("Right Stick Down")
            
            if HatStickLeft:
                #print ("Hat Left")
                Left()
            elif HatStickRight:
                #print ("Hat Right")
                Right()
            elif HatStickUp:
                #print ("Hat Up")
                Forwards()
            elif HatStickDown:
                #print ("Hat Down")
                Backwards()
            
            if not LeftStickLeft and not LeftStickRight and not LeftStickUp and not LeftStickDown and not HatStickLeft and not HatStickRight and not HatStickUp and not HatStickDown:
                StopMotors()
        time.sleep(interval)
    # Disable all drives
    StopMotors()
# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
            
