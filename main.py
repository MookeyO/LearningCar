#!/usr/bin/env python3
print("Hello World")

import time
import sys
import gpiod

# Define GPIO chip and lines
GPIO_CHIP = "/dev/gpiochip0"  # Modify based on your system
MOTOR_LINES = [12, 13, 16, 20]  # Your specified pin numbers

# Function to setup GPIO lines
def setup_gpio():
    chip = gpiod.Chip(GPIO_CHIP)
    lines = [chip.get_line(line) for line in MOTOR_LINES]
    for line in lines:
        line.request(consumer="stepper_motor", type=gpiod.LINE_REQ_DIR_OUT)

    return lines

# Function to set GPIO value
def set_gpio_value(lines, value):
    for line, val in zip(lines, value):
        line.set_value(val)

# Function to release GPIO lines
def cleanup(lines):
    for line in lines:
        line.release()

# Define the sequence of steps for the stepper motor
SEQUENCE = [
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
def rotate(steps, delay, lines):
    try:
        for _ in range(steps):
            for step in SEQUENCE:
                set_gpio_value(lines, step)
                time.sleep(delay)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        cleanup(lines)
        sys.exit(0)

# Setup GPIO lines
motor_lines = setup_gpio()

# Rotate the stepper motor 200 steps with a delay of 0.01 seconds between steps
rotate(200, 0.01, motor_lines)
