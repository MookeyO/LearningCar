#!/usr/bin/env python3
import gpiod
import time

# Define GPIO chip number
GPIO_CHIP = "/dev/gpiochip2"

# Define GPIO lines (pins)
GPIO_LINES = [11, 12, 13, 15]

# Define delay between steps (in seconds)
DELAY = 0.01

# Open GPIO chip
chip = gpiod.Chip(GPIO_CHIP)

# Request GPIO lines
lines = [chip.get_line(line) for line in GPIO_LINES]

# Set GPIO lines direction to output
for line in lines:
    line.request(consumer="stepper_motor", type=gpiod.LINE_REQ_DIR_OUT)

# Define the sequence of steps for the stepper motor
sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Function to rotate the stepper motor
def rotate(steps):
    for step_num in range(steps):
        print(f"Step {step_num + 1}: {sequence[step_num % len(sequence)]}")
        step = sequence[step_num % len(sequence)]
        for i, value in enumerate(step):
            lines[i].set_value(value)
        time.sleep(DELAY)

# Rotate the stepper motor 200 steps
rotate(200)

# Release GPIO lines
for line in lines:
    line.release()

# Close GPIO chip
chip.close()
