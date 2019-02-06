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


// helper functions for launching attacks
void setAttackTime(char* arg2)
{
    int attack_time;
    attack_time = atoi(arg2); // in second
    attack_launch_time = (long long unsigned int) attack_time; // in seconds

    printf("Attack launch Delta: %llu \n", attack_launch_time);
}

void setAttackTimer() {
    /* mark start time */
    clock_gettime(CLOCK_MONOTONIC, &start);

}

int lunch_attack() {

    // printf("attack_code/./sh_attack <<< $\'sudo insmod attack_code/mhasan_rootkit.ko\\ntar xfP ../roverlog/imagelog.tar\\nexit\\n\'");
    int errorflag = 0;
    if (system("attack_code/./attack.sh") == -1) {
        errorflag = -1;
    }

    return errorflag;

}

// handler for tasks routine

int task_function(int arg, int expmt) {


    // index for se tasks
    int logindx_1=se_task_indx_1;
    int logindx_2=se_task_indx_2;
    // uint32_t t0 = ccnt_read();
    int quit = 0;



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


    // uint32_t t1 = ccnt_read();

    // printf("Time (nanosec) %Lf\n", (long double) (BILLION * (t1-t0)/CPU_FREQUENCY));
    if ((arg == logindx_1 && !quit_1) || (arg == logindx_2 && !quit_2)) {
        //printf("%Lf\n", (long double) (BILLION * (t1-t0)/CPU_FREQUENCY));
        // FILE *fp=NULL;
        // if (expmt==0) {
        //     fp = fopen("res_time_trace/restime_trace_opp.txt", "a");
        // }
        // else if (expmt==1) {
        //     fp = fopen("res_time_trace/restime_trace_prop.txt", "a");
        // }
        // fprintf(fp, " %Lf\n", (long double) (BILLION * (t1-t0)/CPU_FREQUENCY));
        //
        // fclose(fp);

        // detect intrusion
        if (isAttackLaunched) {

            // int checkError = system("grep -q \"Total violations found:  0\" twout.txt");

            int checkError = 0;

            // printf("Arg: %d, logindx_1: %d, logindx_2:%d\n", arg, logindx_1, logindx_2);

            if (arg == logindx_1) {
                checkError = system("grep -q \"Total violations found:  0\" twout.txt");
            }


            else if (arg == logindx_2) {
                checkError = system("grep -q \"Total violations found:  0\" kmout.txt");
            }


            // printf("Checkerror %d!\n", checkError);
            // printf("Checkerror %d!, arg=%d\n", checkError, arg);
            if (checkError != 0) {

                uint64_t t2 = ccnt_read();
                uint64_t time2detect = t2 - attack_point;

                if (arg == se_task_indx_1){
                    quit_1 = 1;
                    t2detect_1 = (long double) (BILLION * time2detect/CPU_FREQUENCY);
                }


                else if (arg == se_task_indx_2) {
                    quit_2 = 1;
                    t2detect_2 = (long double) (BILLION * time2detect/CPU_FREQUENCY);
                }


                // write to the file (in ns)


                // FILE *fp=NULL;
                // if (expmt==0) {
                //     if (arg == se_task_indx_1)
                //         fp = fopen("id_time_trace/id_trace_ff_1.txt", "a");
                //     else if (arg == se_task_indx_2)
                //         fp = fopen("id_time_trace/id_trace_ff_2.txt", "a");
                // }
                // else if (expmt==1) {
                //     if (arg == se_task_indx_1)
                //         fp = fopen("id_time_trace/id_trace_prop_1.txt", "a");
                //     else if (arg == se_task_indx_2)
                //         fp = fopen("id_time_trace/id_trace_prop_2.txt", "a");
                // }
                // fprintf(fp, " %Lf\n", (long double) (BILLION * time2detect/CPU_FREQUENCY));
                //
                // fclose(fp);

                // printf("We have got violations by %d! Time to detect: %Lf (nanosec)\n", arg, (long double) (BILLION * time2detect/CPU_FREQUENCY));
                // printf("Detection task ID %d", arg);
                // printf("Exiting applications...");
                // end of experiment

                // if (quit_1 && quit_2)
                //     quit =1;
                // isSETerminate = 1;
                // // end of experiment
                //
                // quit =1;
                // return quit;

            }
            // printf("\n\n\nSecurity tasks %d detecting intrusion... \n\n\n", arg);
            //
            // uint64_t t2 = ccnt_read();
            // uint64_t time2detect = t2 - attack_point;
            //
            // printf("Detec Time (nanosec) %Lf\n", (long double) (BILLION * time2detect/CPU_FREQUENCY));
            //
            // quit =1;
            // return quit;
        }

    }

    // launch attack from HP task
    if (arg == 0) {
        struct timespec end;
        uint64_t diff;
        clock_gettime(CLOCK_MONOTONIC, &end);	/* mark the end time */
        diff = BILLION * (end.tv_sec - start.tv_sec) + end.tv_nsec - start.tv_nsec;

        // printf("elapsed time = %llu nanoseconds\n", (long long unsigned int) diff);
        // printf("elapsed time = %lf seconds\n", (double) diff/BILLION);
        // printf("Attack launch time: %llu \n", attack_launch_time);

        if (firstTime) {
            attack_launch_time = (uint64_t) (diff/BILLION) + attack_launch_time;
            firstTime = 0;
            // printf("Attack launch time: %llu \n", attack_launch_time);
        }

        if (diff > BILLION * attack_launch_time) {

            if(!isAttackLaunched) {

                if (lunch_attack() == -1) {
                    printf("Error Launching Attack!\n");
                    exit(1);
                } else {
                    isAttackLaunched = 1;  // set the flag
                    /* mark attack launch instance */
                    attack_point = ccnt_read();
                    // launced actual attack code
                    // printf("\n\n\n==== @@@@@ Attack launched! @@@@@ ===== \n\n\n");
                }

            }
            else {
                // printf("\n\n\n==== Already launched attack! ===== \n\n\n");
            }

        }

    }

    if (quit_1 && quit_2) {
        quit = 1;

        // FILE *fp=NULL;
        // if (expmt==0) {
        //     fp = fopen("id_time_trace/id_trace_ff.txt", "a");
        // }
        // else if (expmt==1) {
        //     fp = fopen("id_time_trace/id_trace_prop.txt", "a");
        // }
        // fprintf(fp, "%Lf,  %Lf\n", t2detect_1, t2detect_2);
        //
        // fclose(fp);
    }
        // quit =1;

    return quit;

}
