#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [14, 15, 18, 23]

# Set all pins as output
for pin in StepPins:
    print("Setup pins")
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1, 0, 0, 1],
       [1, 0, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [0, 0, 0, 1]]

StepCount = len(Seq)
StepDir = 1  # Set to 1 or 2 for clockwise
# Set to -1 or -2 for anti-clockwise

# Read wait time from command line
if len(sys.argv) > 1:
    WaitTime = 1 / 1000.0
else:
    WaitTime = 1 / 1000.0

# Initialise variables
StepCounter = 0

# Ultrasonic Sensor setup
GPIO_TRIGGER = 25
GPIO_ECHO = 7
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

# Start main loop
try:
    while True:
        dist = distance()
        if dist is not None:
            if dist > 10:
                for pin in range(0, 4):
                    xpin = StepPins[pin]
                    if Seq[StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                StepCounter += StepDir
                if StepCounter >= StepCount:
                    StepCounter = 0
                if StepCounter < 0:
                    StepCounter = StepCount + StepDir
                time.sleep(WaitTime)
            else:
                for pin in StepPins:
                    GPIO.output(pin, False)
        else:
            print("Failed to get distance measurement.")
        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    GPIO.cleanup()

