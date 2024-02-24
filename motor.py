#!/usr/bin/python
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals for stepper motor
StepPins = [14, 15, 18, 23]

# Define GPIO pins for ultrasonic sensor
TRIG = 25
ECHO = 7

# Set all pins as output for stepper motor
for pin in StepPins:
    print("Setup pins")
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Set TRIG as output and ECHO as input for ultrasonic sensor
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Function to measure distance using ultrasonic sensor
def measure_distance():
    # Send pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Record time of pulse being sent
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Record time of pulse return
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert time to distance (in cm)
    distance = pulse_duration * 17150

    # Round distance to 2 decimal places
    distance = round(distance, 2)

    return distance

# Function to move stepper motor forward or backward by a specified number of steps
def move_stepper(steps):
    global StepCounter
    goal = 0
    while goal < steps:
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += StepDir

        # If we reach the end of the sequence
        # start again
        if StepCounter >= StepCount:
            StepCounter = 0
        if StepCounter < 0:
            StepCounter = StepCount + StepDir
        goal += 1
        # Wait before moving on
        time.sleep(WaitTime)


try:
    # Define advanced sequence for stepper motor
    Seq = [[1, 0, 0, 1],
           [1, 0, 0, 0],
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 0, 0, 1]]

    StepCount = len(Seq)
    StepDir = 1  # Set to 1 or 2 for clockwise, -1 or -2 for anti-clockwise

    # Read wait time from command line or set default
    if len(sys.argv) > 1:
        WaitTime = int(sys.argv[1]) / 1000.0
    else:
        WaitTime = 2 / 1000.0

    # Initialise variables
    StepCounter = 0

    # Start main loop
    while True:
        # Measure distance with ultrasonic sensor
        distance = measure_distance()
        print("Distance:", distance, "cm")

        # Check if distance is greater than 15cm
        if distance > 15:
            # Move stepper motor forward by 4096 steps
            move_stepper(4096)
        else:
            # Move stepper motor backward by 2048 steps
            time.sleep(5)

except KeyboardInterrupt:
    print("Goodbye!")
    GPIO.cleanup()

