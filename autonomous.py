#!/usr/bin/env python3
# autonomous.py
#import requirements
import RPi.GPIO as GPIO
import time
import activeBuzzer
import us_sensor
import moveForward
import moveBackward
import turnLeft
import turnRight
import random

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

def autonomous():
    # Set the initial state
    state = 'Start'
    errorActions = 0
    while True:
        distance = us_sensor.distance()
        print(distance)
        #buzz once at start of each loop
        activeBuzzer.activate_buzzer(1)
        #start state
        if state == 'Start':
            print('Starting')
            if distance > 100:
                moveForward.move_forward(400)
                state = 'Forward'
                continue
            elif distance < 100:
                activeBuzzer.activate_buzzer(2)
                state = 'Stop'
                continue
        #stop state if getting too close to an obstacle
        elif state == 'Stop':
            print("Stopped")
            if distance > 100:
                state = 'Forward'
                continue
            elif 60 < distance < 100:
                state = 'Turn'
                continue
            elif distance < 60:
                moveBackward.move_backward(200)
                continue
            else:
                #action if the device is in the stopped state more than three times in a row
                print("stopped", distance, "errorActions:", errorActions)
                errorActions += 1
                if errorActions > 3:
                    print("Too many errors")
                    #kills process if too many errors
                    break
                continue
        #move forward if there are no obstacles
        elif state == 'Forward':
            print('Move forward')
            if distance > 100:
                moveForward.move_forward(200)
                continue
            elif distance < 60:
                state = 'Stop'
                continue
            elif 60 < distance < 100:
                state = 'Turn'
                continue
        #turn if there is an obstacle between 60 and 100cm
        elif state == 'Turn':
            direction = random.choice(["Left", "Right"])
            activeBuzzer.activate_buzzer(2)
            print("Turning", direction)
            if direction == "Right":
                turnRight.turn_right(400)
            elif direction == "Left":
                turnLeft.turn_left(400)
            #send it back to start state after a turn
            state = 'Start'
            continue
        #cleanup pins
    GPIO.cleanup()
if __name__ == "__main__":
    autonomous()
    #ensure pins are cleaned up at the end
    GPIO.cleanup()
