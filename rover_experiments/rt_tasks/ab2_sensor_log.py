import sys
import TRSensors as sensor

# reads sensor values and log to /roverlog/sensorlog.txt
if __name__ == '__main__':
    TR = sensor.TRSensor()
    sensor_val = str(TR.AnalogRead())

    filename = '../roverlog/sensorlog.txt'


    with open(filename, "a") as f:
        f.write(sensor_val + '\n')

    # print sensor_val
