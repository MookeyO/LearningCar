#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import activeBuzzer







state = 'Start'

while True:

    if state == 'Start':
        activeBuzzer.activate_buzzer
        state = 'Stop'
        continue
    elif state == 'Stop':
        print("Stopping")
        break
print("Come again later!")