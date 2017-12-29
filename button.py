#!/usr/bin/python3

import os
import threading
import time
import subprocess
from os.path import isfile, join
from os import listdir
import json
import RPi.GPIO as GPIO

# - - - - - - - - - - - - - - - - 
# - - BUTTON CONTROLLER CLASS - -
# - - - - - - - - - - - - - - - -
class Button:
    def __init__(self, pin, shortPressFun, longPressFun):
        self.buttonPin = pin
        self.buttonPressedFlag = False 
        self.helperFlag1 = False 
        self.buttonReleasedCounter = 0
        self.longPressTime = 1000;      # All time related properties in Millisecs 
        self.pressStartTime = 0;
        self.pressEndTime = 0;
        self.pressDuration = 0
        self.shortPressFun = shortPressFun
        self.longPressFun = longPressFun

    def update(self):
        buttonStatus = GPIO.input(self.buttonPin)
        if buttonStatus and not self.helperFlag1:
            # Trigger on positive flank of Button Input Signal
            self.buttonPressedFlag = True;
            self.helperFlag1 = True
            self.pressStartTime = self.getTimeStamp()
            # helperFlag1 needs to be resetted after the Buttonpress was registered correctly
        elif not buttonStatus and self.buttonPressedFlag:
            # We get in here when the button was pressed but isn't pressed anymore
            self.buttonReleasedCounter += 1;
            if self.buttonReleasedCounter >= 2:
                self.buttonPressedFlag = False
                self.helperFlag1 = False
                self.buttonReleasedCounter = 0
                self.pressEndTime = self.getTimeStamp()
                self.pressDuration = self.pressEndTime - self.pressStartTime
                if self.pressDuration >= self.longPressTime:
                    # Long Press!
                    self.longPress()
                else:
                    # Short Press!
                    self.shortPress()
        elif buttonStatus and self.buttonPressedFlag:
            # Reset the buttonReleasedCounter if the buttonStatus gets high again very fast
            self.buttonReleasedCounter = 0;

    def getTimeStamp(self):
        # returns the current TimeStamp in millisecs
        return int(time.time()*1000)

    def longPress(self):
        print("pin {0} long press".format(self.buttonPin))
        self.longPressFun()

    def shortPress(self):
        print("pin {0} short press".format(self.buttonPin))
        self.shortPressFun()