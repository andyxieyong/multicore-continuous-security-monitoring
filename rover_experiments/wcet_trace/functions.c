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

void clear_cache()
{
    if (system("sync; echo 1 > /proc/sys/vm/drop_caches") == -1) {
        printf("Error Clearing Caches!\n");
	}

}

// handler for tasks routine

void task_function(int arg, char* filename) {


    // clear_cache();

    uint32_t t0 = ccnt_read();

    /* Call task code here */

    if (system(task_command_name[arg]) == -1) {
        printf("Error starting Tasks!\n");
	}


    uint32_t t1 = ccnt_read();

    // printf("Time (nanosec) %Lf\n", (long double) (BILLION * (t1-t0)/CPU_FREQUENCY));

    FILE *fp;
    fp = fopen(filename, "a");
    fprintf(fp, " %Lf\n", (long double) (BILLION * (t1-t0)/CPU_FREQUENCY));

    fclose(fp);

}
