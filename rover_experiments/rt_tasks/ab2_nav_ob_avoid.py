import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2

DR = 16
DL = 19
Ab = AlphaBot2()

def init():


    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

def do_navigate():

    try:

		DR_status = GPIO.input(DR)
		DL_status = GPIO.input(DL)
#		print(DR_status,DL_status)
		if((DL_status == 0) or (DR_status == 0)):
			# Ab.left()
			#Ab.right()
			# time.sleep(0.002)
			Ab.stop()
			# time.sleep(0.002)
			Ab.left()

			# print("object")
		else:
			Ab.forward()
			# print("forward")

    except KeyboardInterrupt:
    	GPIO.cleanup();

def run_in_loop():
    # init()
    max_val = 1
    # sleep_val = 0.002
    sleep_val = 0.1
    for i in range(max_val):
        init()
        do_navigate()
        time.sleep(sleep_val)

def run_one_instance():
    init()
    do_navigate()


# main navigation task (can avoid obstracles)
if __name__ == '__main__':

    run_in_loop()
    # run_one_instance()
