#!/usr/bin/env python3
#autonomous.py
import RPi.GPIO as GPIO
import time
import activeBuzzer
import us_sensor
import moveForward
import moveBackward
import turnLeft
import turnRight
import random


#set initial state
GPIO.setmode(GPIO.BCM)
def autonomous():
    state = 'Start'
    errorActions = 0
    while True:
        distance = us_sensor.distance#measure distance at start
        print(distance)#print distance to console
        activeBuzzer.activate_buzzer(1)#beep once at start of each loop
        if state == 'Start':
            print('Starting')
            if distance > 100:
                moveForward.move_forward(400)#move 400 steps
                state = 'Forward'
                continue
            elif distance < 100:
                activeBuzzer.activate_buzzer(2)#beep twice
                state = 'Stop'
                continue
            else:
                print("state did not change")
                continue
        elif state == 'Stop':
            print("Stopped")
            if distance > 100:
                state = 'Forward'
                continue
            elif 60 < distance < 100:
                state == 'Turn'
                continue
            elif distance < 60:
                moveBackward.move_backward(200)
                continue
            else:
                print("state did not change")
                continue
        elif state == 'Forward':
            print('Move forward')
            if distance > 100:
                moveForward.move_forward(200)
                continue
            elif distance < 60:
                state == 'Stop'
                continue
            elif 60 < distance < 100:
                state == 'Turn'
                continue
            else:
                print("state did not change")
                continue
        elif state == 'Turn':
            direction = random.choice("Left","Right")
            activeBuzzer.activate_buzzer(2)
            print("Turning",direction)
            if direction == "Right":
                turnRight.turn_right(400)
            elif direction == "Left":
                turnLeft.turn_left(400)
            state == 'Start' #return to the start to see what to do next
            continue
    print("Come again later!")

if __name__ == "__main__":
    autonomous()