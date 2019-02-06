#!/bin/bash

echo "Running experiments..."

# enable cycle counter kernle module
sudo insmod ../arm_cc_km/enable_arm_cc.ko



for ((n=1;n<36;n++))
do

    # generate a random number between 10 and 35
    ATTACK_TIME=$(( RANDOM % (25 - 10 + 1 ) + 10 ))


    echo "===================="
    echo "Experiment No. # $n"
    echo "===================="

    echo
    echo "======== Proposed ($n) ============"

    # Run Experiments (Proposed)
    echo "Removing twout.txt, kmout.txt ..."
    rm twout.txt
    rm kmout.txt

    echo "Removing kernel module..."
    sudo rmmod mhasan_rootkit

    echo "Removing imagelog.tar..."
    touch ../roverlog/imagelog.tar

    echo "Running experiments..."
    ./id_time_main 1 $ATTACK_TIME


    echo "Removing attack trace and run control code..."
    python ../rt_tasks/ab2_nav_ob_avoid.py
    rm ../roverlog/dummyimage.jpg
    sudo rm -r ../roverlog/*.tar

    echo
    echo "======== Best-Fit ($n) ============"

    # Run Experiments (Proposed)
    echo "Removing twout.txt, kmout.txt ..."
    rm twout.txt
    rm kmout.txt

    echo "Removing kernel module..."
    sudo rmmod mhasan_rootkit

    echo "Removing imagelog.tar..."
    touch ../roverlog/imagelog.tar

    echo "Running experiments..."
    ./id_time_main 0 $ATTACK_TIME

    echo "Removing attack trace and run control code..."
    python ../rt_tasks/ab2_nav_ob_avoid.py
    rm ../roverlog/dummyimage.jpg
    sudo rm -r ../roverlog/*.tar


done




echo "==== EXPERIMENT DONE! ===="
