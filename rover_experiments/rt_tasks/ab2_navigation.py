#!/usr/bin/python

import sys
import RPi.GPIO as GPIO
import AlphaBot2 as alphabot
import time


def navigation_task(MAX_LOOP, direction):
    """ Moving Alphabot """

    Ab = alphabot.AlphaBot2()

    try:
        count = 0
        while count < MAX_LOOP:
            time.sleep(0.300)
            if direction.lower() == 'forward':
                Ab.forward()
            if direction.lower() == 'backward':
                Ab.backward()
            if direction.lower() == 'left':
                Ab.left()
            if direction.lower() == 'right':
                Ab.right()

            count += 1
    except KeyboardInterrupt:
            GPIO.cleanup()

    GPIO.cleanup()


if __name__=='__main__':

    # How to run: python ab2_navigation.py forward
    # (or any other direction)

    if len(sys.argv) != 2:
        raise Exception("Invalid Arguments, use: python filename direction. == direction should be -> forward, backward, left, right ==")

    valid = False
    direction = sys.argv[1]  # direction
    if direction.lower() == 'forward' or direction.lower() == 'backward' or direction.lower() == 'left' or direction.lower() == 'right':
        valid = True

    if not valid:
        raise Exception("Invalid command in navigation task!")
        # return


    MAX_LOOP_FORWARD = 4
    MAX_LOOP_BACKWARD = 3
    MAX_LOOP_LEFT = 2
    MAX_LOOP_RIGHT = 2

    if direction.lower() == 'forward':
        navigation_task(MAX_LOOP=MAX_LOOP_FORWARD, direction=direction)
    elif direction.lower() == 'backward':
        navigation_task(MAX_LOOP=MAX_LOOP_BACKWARD, direction=direction)
    elif direction.lower() == 'left':
        navigation_task(MAX_LOOP=MAX_LOOP_LEFT, direction=direction)
    elif direction.lower() == 'right':
        navigation_task(MAX_LOOP=MAX_LOOP_RIGHT, direction=direction)
