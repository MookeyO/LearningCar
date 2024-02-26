#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print('Moving Backward!')

# GPIO pins for the first stepper motor
StepPins1 = [14, 15, 18, 23]  # Assuming you're using 4 pins for the stepper motor
# Define the sequence of steps for the first motor (reversed for backward motion)
Seq1 = [[0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]]

# GPIO pins for the second stepper motor
StepPins2 = [12, 16, 20, 21]  # Pins for the second motor
# Define the sequence of steps for the second motor (reversed for backward motion)
Seq2 = [[0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]]

# Initialize GPIO for both motors
GPIO.setmode(GPIO.BCM)
for pin in StepPins1 + StepPins2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Function to move both motors backward by a specified number of steps
def move_backward(steps):
    StepCounter1 = 0
    StepCounter2 = 0
    StepCount1 = len(Seq1)
    StepCount2 = len(Seq2)
    for _ in range(steps):
        for pin in range(4):
            # Control the first motor
            xpin1 = StepPins1[pin]
            if Seq1[StepCounter1][pin] != 0:
                GPIO.output(xpin1, True)
            else:
                GPIO.output(xpin1, False)
                
            # Control the second motor
            xpin2 = StepPins2[pin]
            if Seq2[StepCounter2][pin] != 0:
                GPIO.output(xpin2, True)
            else:
                GPIO.output(xpin2, False)

        StepCounter1 += 1
        StepCounter2 += 1

        # Reset counter to 0 when it reaches the end of the sequence
        if StepCounter1 >= StepCount1:
            StepCounter1 = 0
        if StepCounter2 >= StepCount2:
            StepCounter2 = 0

        # Delay to control motor speed
        time.sleep(0.009)  # Adjust this delay for your motor speed

# Move both motors backward by a specified number of steps
if __name__ == "__main__":
    move_backward(500)
    GPIO.cleanup()  # Cleanup GPIO pins after use

