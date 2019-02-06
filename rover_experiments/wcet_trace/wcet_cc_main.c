

/*
 * File:   wcet_cc_main.c
 * Author: mhasan11
 *
 * Created on April 16, 2016, 6:17 PM
 */

 // to compile: gcc -o wcet_cc_main wcet_cc_main.c -lrt -Wall

#include <stdio.h>
#include <stdlib.h>


/*
 *
 */
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>


/* Threading */
#include <pthread.h>

// My include files
#include "functions.h"
// #include "globals.h"


#define MY_PRIORITY (98) /* we use 49 as the PRREMPT_RT use 50
                            as the priority of kernel tasklets
                            and interrupt handler by default */

#define MAX_SAFE_STACK (8*1024) /* The maximum stack size which is
                                   guaranteed safe to access without
                                   faulting */

#define NSEC_PER_SEC    (1000000000) /* The number of nsecs per sec. */

extern const char *task_command_name[];  // task command names
extern const int EXP_COUNT;  // number of traces we want

struct sched_param param;  // Schedular structure

void stack_prefault(void) {

    unsigned char dummy[MAX_SAFE_STACK];

    memset(dummy, 0, MAX_SAFE_STACK);
    return;
}

/* the struct timespec consists of nanoseconds
 * and seconds. if the nanoseconds are getting
 * bigger than 1000000000 (= 1 second) the
 * variable containing seconds has to be
 * incremented and the nanoseconds decremented
 * by 1000000000.
 */
static inline void tsnorm(struct timespec *ts) {
    while (ts->tv_nsec >= NSEC_PER_SEC) {
        ts->tv_nsec -= NSEC_PER_SEC;
        ts->tv_sec++;
    }
}

void intialize_rt_env() {

    /* Declare ourself as a real time task */

    param.sched_priority = MY_PRIORITY;
    if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
        perror("sched_setscheduler failed");
        exit(-1);
    }

    /* Lock memory */

    if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
        perror("mlockall failed");
        exit(-2);
    }

    /* Pre-fault our stack */

    stack_prefault();

}

void sanity_check(int taskcode_indx, int argc) {

    if (argc != 3) {
        printf("Invalid input (use codeindex and filenmae). Returning...\n");
        printf("Example: ./wcet_cc_main 0 traces\\forward.txt \n");
        exit(1);
    }

    int command_size;

    for (command_size = 0; task_command_name[command_size] != NULL; command_size++);

    // printf("Input size: %d\n", command_size);


    if (taskcode_indx <0 || taskcode_indx >= command_size) {
        printf("Invalid input (index size mismatch given number of commands). Returning...\n");
        exit(1);
    }

    printf("### Command name: %s ### \n", task_command_name[taskcode_indx]);

}

int main(int argc, char* argv[]) {
    struct timespec t;

    long long int interval = 1000000000;  // does not matter. How long task will generate

    intialize_rt_env();

    clock_gettime(CLOCK_MONOTONIC, &t);
    /* start after one second */
    t.tv_sec++;

    int i=0;
    int taskcode_indx=atoi(argv[1]);

    // some error checking
    sanity_check(taskcode_indx, argc);

    while (1) {

        /* wait untill next shot */
       clock_nanosleep(0, TIMER_ABSTIME, &t, NULL);
       /* do the stuff */

       // call RT and Secuirity tasks here

       task_function(taskcode_indx, argv[2]);

       /* calculate next shot */
       t.tv_nsec += interval;
       tsnorm(&t);

       printf("== Trace %d logged! == \n", i+1);
       if (++i == EXP_COUNT) {
           break;
       }



   }

    /* We will never reach here */



}
