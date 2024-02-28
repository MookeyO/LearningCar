#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

def distance():
    # Set GPIO pin mode
    GPIO.setmode(GPIO.BCM)
    # Set GPIO pin numbers
    GPIO_TRIGGER = 19
    GPIO_ECHO = 13
    # Set GPIO pin direction
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    try:
        #send trigger signal to the sensor
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        #record the time the signal is sent
        StartTime = time.time()
        StopTime = time.time()
        #record the time the signal is received
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        #calculate the time it took for the signal to return
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        #return the distance as an integer
        distance = int(distance)
        return distance
    #catch any errors and return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        # cleanup pins
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist is not None:
                print("Measured Distance = %.1f cm" % dist)
            else:
                print("Failed to get distance measurement.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()

