#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>	/* for clock_gettime */


// My include files
#include "functions.h"
#include "globals.h"


// ARM cycle counter readers
static inline uint32_t ccnt_read (void)
{
  uint32_t cc = 0;
  __asm__ volatile ("mrc p15, 0, %0, c9, c13, 0":"=r" (cc));
  return cc;
}



// handler for tasks routine

int task_function(int arg, int expmt) {


    /* Call task code here */



    if (expmt==0) {
        // FF allocation
        if (system(task_command_name_ff[arg]) == -1) {
            printf("Error starting Tasks!\n");
            exit(1);
    	}

        // printf("Task id: %d, command: %s\n", arg, task_command_name_ff[arg]);
    }

    else if (expmt==1) {
        // Proposed scheme
        if (system(task_command_name_prop[arg]) == -1) {
            printf("Error starting Tasks!\n");
            exit(1);
    	}
        // printf("Task id: %d, command: %s\n", arg, task_command_name_prop[arg]);
    }

    else if (expmt==2) {
        // Vanilla
        if (system(task_command_name_vanilla[arg]) == -1) {
            printf("Error starting Tasks!\n");
            exit(1);
    	}
        // printf("Task id: %d, command: %s\n", arg, task_command_name_vanilla[arg]);
    }



    // returns false (since we will quite using timeout)
    return 0;

}
