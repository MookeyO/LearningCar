#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time



# Function to move both motors forward by a specified number of steps
def move_forward(steps):
    print('Moving Forward!')

# GPIO pins for the first stepper motor
    StepPins1 = [14, 15, 18, 23] 
    # Define the sequence of steps for the first motor
    Seq1 = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

    # GPIO pins for the second stepper motor
    StepPins2 = [12, 16, 20, 21]  
    # Define the sequence of steps for the second motor
    Seq2 = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

    # Initialize GPIO for both motors
    GPIO.setmode(GPIO.BCM)
    for pin in StepPins1 + StepPins2:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
    #initialize step counters
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
        time.sleep(0.002)
    #cleanup pins at end of function
    GPIO.cleanup()

# Move both motors forward by a specified number of steps
if __name__ == "__main__":
    move_forward(500)
    #ensure pins are low before ending
    GPIO.cleanup()  

