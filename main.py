#!/usr/bin/env python3
print("Hello World")

# Import the required modules
from gpiozero import Motor
import time

# Define the pins for the stepper motor
motor_pins = (2, 3, 4, 17)  # Replace with your actual pin numbers

# Create a Motor object
motor = Motor(forward=motor_pins[0], backward=motor_pins[1], enable=(motor_pins[2], motor_pins[3]))

# Define the sequence of steps for the stepper motor
sequence = [
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1)
]

# Function to rotate the stepper motor
def rotate(steps, delay):
    for _ in range(steps):
        for step in sequence:
            motor.value = step
            time.sleep(delay)

# Rotate the stepper motor 200 steps with a delay of 0.01 seconds between steps
rotate(200, 0.01)