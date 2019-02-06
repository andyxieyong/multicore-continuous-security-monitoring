# import sys
import os
# reads core temp and log to /roverlog/coretemplog.txt
def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        # print "temp is:", temp
        return (temp.replace("temp=",""))


if __name__ == '__main__':

    temp_val = measure_temp()

    # print "temp:", temp_val

    filename = '../roverlog/coretemplog.txt'


    with open(filename, "a") as f:
        f.write(temp_val + '\n')
