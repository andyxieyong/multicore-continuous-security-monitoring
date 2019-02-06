

// to compile: gcc -o wcet_cc_main wcet_cc_main.c -lrt -Wall -pthread
#define _GNU_SOURCE
#include <sched.h>

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/mman.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>


/* Threading */
#include <pthread.h>

// my functions
#include "functions.h"

extern long double t2detect_1, t2detect_2;

#define MY_PRIORITY (49) /* we use 49 as the PRREMPT_RT use 50
                            as the priority of kernel tasklets
                            and interrupt handler by default */

#define MAX_SAFE_STACK (8*1024) /* The maximum stack size which is
                                   guaranteed safe to access without
                                   faulting */

#define NSEC_PER_SEC    (1000000000) /* The number of nsecs per sec. */


#define NTASK 4 /* Number of Tasks */
//
// #define N_RT_TASK 2  // number of RT Tasks
// #define N_SE_TASK 1
//
// const int RT_CORE_ASS[N_RT_TASK] = {0, 1};
// const int FF_SE_CORE_ASS[N_SE_TASK] = {1};

pthread_t tid[NTASK];


long long int period_prop[NTASK] = {500000000, 5000000000, 7583000000, 2784000000};
long long int period_ff[NTASK] = {500000000, 5000000000, 8328000000, 891000000};


int priority[NTASK] = {46, 45, 40, 39};



enum EXPTYPE {
    FF,
    PROP
} exp_type;



// const uint64_t EXP_TIMEOUT_DURATION = 1000;  // in second

int isHPTerminate = 0;
int isExpTerminate = 0;

int camera_count = 0;

// int camidxFF = 4;
// int camidxprop = 7;

// int camera_indx;

int max_hp_count = 50;
int hp_count = 0;

int loopcount = 25;

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


int bind_thread_to_core(int core_id) {
   int num_cores = sysconf(_SC_NPROCESSORS_ONLN);
   if (core_id < 0 || core_id >= num_cores)
      return EINVAL;

   cpu_set_t cpuset;
   CPU_ZERO(&cpuset);
   CPU_SET(core_id, &cpuset);

   pthread_t current_thread = pthread_self();
   return pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset);
}


void* task_handler(void *arg) {
    // unsigned long i = 0;
    int indx = (int) arg;
    // int indx = atoi(arg);

    struct timespec t;
    struct timespec dt;


    int cnt = 0;


    pthread_t id = pthread_self();

    struct sched_param param;


    /* Declare ourself as a real time task */

    /* Bind to Core (RT Tasks) */

    // if (indx < N_RT_TASK) {
    //     if (bind_thread_to_core(RT_CORE_ASS[indx]) != 0) {
    //         printf("Unable to bind RT task %d", indx);
    //         exit(-1);
    //     }
    //     printf("Bind sussessful for RT task %d!\n", indx);
    // }
    //
    //
    //
    // if (exp_type == FF) {
    //     if (bind_thread_to_core(FF_SE_CORE_ASS[indx]) != 0) {
    //         printf("Unable to bind RT task %d", indx);
    //         exit(-1);
    //     }
    //     printf("FF Bind sussessful for SE task %d!\n", indx);
    // }


    param.sched_priority = priority[indx];
    if (pthread_setschedparam(id, SCHED_FIFO, &param)) {
        perror("sched_setscheduler failed");
        exit(-1);
    }





    /* Lock memory */

    if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
        perror("mlockall failed");
        exit(-2);
    }



    // printf("attack_code/./sh_attack <<< $\'sudo insmod attack_code/mhasan_rootkit.ko\\ntar xfP ../roverlog/imagelog.tar\\nexit\\n\'");


    /* Pre-fault our stack */

    stack_prefault();

    /* Wait some time to make sure all threads create finishing*/
    //clock_gettime(CLOCK_MONOTONIC ,&t);
    //clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &t, NULL);

    //sleep(5);

    if (pthread_equal(id, tid[indx])) {
        printf("Task %d initialization completed \n", indx);
    }

    clock_gettime(CLOCK_MONOTONIC, &t);
    clock_gettime(CLOCK_MONOTONIC, &dt);
    /* start after one second */
    t.tv_sec++;
    // dt.tv_sec++;

    int expmt = -1;

    if (exp_type == FF) {
        expmt = 0;
    }
    else if (exp_type == PROP) {
        expmt = 1;
    }


    while(1) {
    //while (cnt < loopcount) {
        /* wait until next shot */
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &t, NULL);



        // deicide to terminate

        if (isExpTerminate==1) {
            int ret  = 100;
            pthread_exit(&ret);
        }

        /* do the stuff */

        int quit = task_function(indx, expmt);


        if (quit == 1) {

            // printf("Teminate True\n");
            isExpTerminate = 1;

        }


        /* Task finished */
        // printf("Task %d finished\n", indx);

        /* calculate next shot */

        if (exp_type == FF) {
            t.tv_nsec += period_ff[indx];
        }
        else if (exp_type == PROP) {
            t.tv_nsec += period_prop[indx];
        }



        cnt++;
        if (indx==0) {
            // if (cnt > max_hp_count) {
            //     isHPTerminate = 1;  // time to quite
            // }

            hp_count++;
        }

        /* Normalize time counter */
        tsnorm(&t);



    }


    /* We will never reach here */



    return NULL;
}

void set_experiment_mode(int arg) {
    if (arg == 0) {
        exp_type = FF;
    }
    else if (arg == 1) {
        exp_type = PROP;
    }
}

void sanity_check(int argc, int arg) {

    if (argc != 3) {
        printf("Invalid input (experiment mode should be only 0 and 1). Returning...\n");
        printf("Example: ./res_time_main 0 attack_time OR ./res_time_main 1 attack_time (0 for Best-fit, 1 for Porposed) \n");
        exit(1);
    }

    if (arg < 0 || arg > 1) {
        printf("Invalid input (experiment mode should be only 0 and 1). Returning...\n");
        printf("Example: ./res_time_main 0 attack_time OR ./res_time_main 1 attack_time (0 for Best-fit, 1 for Porposed) \n");
        exit(1);
    }

}

int main(int argc, char* argv[]) {
    struct timespec t;
    struct sched_param param;
    // int interval = 5000000; /* 5000us*/

    // int j = 0;
    // int max_hp_count = 10;

    int i = 0;
    int err;



    /* Some error checking */
    sanity_check(argc, atoi(argv[1]));

    /* Set experiment mode */
    set_experiment_mode(atoi(argv[1]));

    if (exp_type == FF) {
        printf("\n== Running Best-fit Scheme ==\n");
    }
    else if (exp_type == PROP) {
        printf("\n== Running Proposed Scheme ==\n");
    }



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

    /* Set attack time */
    setAttackTime(argv[2]);

    /* Set attack timer */


    /* Create threads */

    for (i = 0; i < NTASK; i++) {
        err = pthread_create(&(tid[i]), NULL, task_handler, (void*) i);

        /* Some error checking */

        if (err != 0)
            printf("Can't create thread :[%s]", strerror(err));
        else
            printf("Thread created successfully\n");
    }

    clock_gettime(CLOCK_MONOTONIC, &t);
    /* start after one second */
    t.tv_sec++;

    /* We will never reach here for actual while(1) task loops */

    for (i = 0; i < NTASK; i++) {
        pthread_join(tid[i], NULL);
    }

    // printf("Experiment teminate...\n");

    // write to file
    FILE *fp=NULL;
    if (exp_type == FF) {
        fp = fopen("id_time_trace/id_trace_ff.txt", "a");
    }
    else if (exp_type == PROP) {
        fp = fopen("id_time_trace/id_trace_prop.txt", "a");
    }
    fprintf(fp, "%Lf,  %Lf\n", t2detect_1, t2detect_2);

    fclose(fp);


}
