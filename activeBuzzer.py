#!/usr/bin/env python3
#activeBuzzer.py
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO_Buzzer = 26

def activate_buzzer(beeps):
    for _ in beeps:
        GPIO.setup(GPIO_Buzzer, GPIO.OUT)
        time.sleep(.3)
        GPIO.output(GPIO_Buzzer, True)
        time.sleep(.1)
        GPIO.output(GPIO_Buzzer, False)

if __name__ == "__main__":
    activate_buzzer()
    GPIO.cleanup()
