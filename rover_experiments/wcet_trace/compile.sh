#!/bin/bash

echo "Compiling..."
gcc -o wcet_cc_main wcet_cc_main.c functions.c -lrt -Wall -pthread -O3
