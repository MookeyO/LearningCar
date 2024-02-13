#!/usr/bin/env python3
print("Hello World")

import time

# Define GPIO pin numbers
MOTOR_PINS = (2, 3, 4, 17)  # Replace with your actual pin numbers

# GPIO file paths
EXPORT_PATH = "/sys/class/gpio/export"
UNEXPORT_PATH = "/sys/class/gpio/unexport"
DIRECTION_PATH = "/sys/class/gpio/gpio{}/direction"
VALUE_PATH = "/sys/class/gpio/gpio{}/value"

# Function to export GPIO pin
def export_gpio(pin):
    with open(EXPORT_PATH, 'w') as f:
        f.write(str(pin))

# Function to set GPIO direction
def set_gpio_direction(pin, direction):
    with open(DIRECTION_PATH.format(pin), 'w') as f:
        f.write(direction)

# Function to set GPIO value
def set_gpio_value(pin, value):
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
    for _ in range(steps):
        for step in sequence:
            for i, pin in enumerate(MOTOR_PINS):
                set_gpio_value(pin, step[i])
            time.sleep(delay)

# Rotate the stepper motor 200 steps with a delay of 0.01 seconds between steps
rotate(200, 0.01)

# Cleanup: Unexport GPIO pins
for pin in MOTOR_PINS:
    with open(UNEXPORT_PATH, 'w') as f:
        f.write(str(pin))
