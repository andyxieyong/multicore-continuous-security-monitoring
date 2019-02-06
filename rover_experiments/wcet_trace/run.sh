#!/bin/bash

echo "Running code..."

rm twout.txt

sudo insmod ../arm_cc_km/enable_arm_cc.ko

# RT tasks
./wcet_cc_main 0 traces/navigation.txt
./wcet_cc_main 1 traces/sensor.txt
./wcet_cc_main 2 traces/camera.txt
./wcet_cc_main 3 traces/coretemp.txt
./wcet_cc_main 4 traces/location.txt

#  Security tasks
./wcet_cc_main 5 traces/tw_ownbin.txt
./wcet_cc_main 6 traces/tw_rootbin.txt
./wcet_cc_main 7 traces/tw_roverlogscan.txt
./wcet_cc_main 8 traces/cus_kmlog.txt
./wcet_cc_main 9 traces/tw_rovlog_cus_kmlog.txt
