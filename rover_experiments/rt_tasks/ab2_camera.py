from picamera import PiCamera
import time
import os

# reads sensor values and log to /roverlog/sensorlog.txt
if __name__ == '__main__':

    dir_location = '../roverlog/'
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    image_filename = dir_location + timestamp + ".jpg"

    archive_filename = dir_location + 'imagelog.tar'

    # camera = PiCamera()
    # camera.capture(image_filename)
    #
    # command = "tar rfP " + archive_filename + " " + image_filename
    # # print command
    # os.system(command)
    # os.system("rm " + image_filename)
