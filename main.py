#!/usr/bin/env python3
print("Hello World")

import time
import sys

# Define GPIO pin numbers
MOTOR_PINS = (12, 13, 16, 20)  # Your specified pin numbers

# GPIO file paths
EXPORT_PATH = "/sys/class/gpio/export"
UNEXPORT_PATH = "/sys/class/gpio/unexport"
DIRECTION_PATH = "/sys/class/gpio/gpio{}/direction"
VALUE_PATH = "/sys/class/gpio/gpio{}/value"

# Function to export GPIO pin
def export_gpio(pin):
    print("Exporting GPIO pin", pin)
    with open(EXPORT_PATH, 'w') as f:
        f.write(str(pin))

# Function to set GPIO direction
def set_gpio_direction(pin, direction):
    print("Setting GPIO direction for pin", pin, "to", direction)
    with open(DIRECTION_PATH.format(pin), 'w') as f:
        f.write(direction)

# Function to set GPIO value
def set_gpio_value(pin, value):
    print("Setting GPIO value for pin", pin, "to", value)
    with open(VALUE_PATH.format(pin), 'w') as f:
        f.write(str(value))

# Export motor pins
for pin in MOTOR_PINS:
    export_gpio(pin)

# Set motor pins direction to output
for pin in MOTOR_PINS:
    set_gpio_direction(pin, 'out')

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
    try:
        print("Rotating the stepper motor...")
        for _ in range(steps):
            for step in sequence:
                for i, pin in enumerate(MOTOR_PINS):
                    set_gpio_value(pin, step[i])
                print("Step:", step)
                time.sleep(delay)
    except KeyboardInterrupt:
        print("Exiting due to KeyboardInterrupt...")
        cleanup()

# Cleanup function to unexport GPIO pins
def cleanup():
    print("Cleaning up GPIO pins...")
    for pin in MOTOR_PINS:
        with open(UNEXPORT_PATH, 'w') as f:
            f.write(str(pin))
    sys.exit(0)

# Rotate the stepper motor 200 steps with a delay of 0.01 seconds between steps
rotate(200, 0.01)
