#ifndef GLOBALS_H_INCLUDED
#define GLOBALS_H_INCLUDED

/* Define global variables here. */


const int EXP_COUNT = 100;

#define BILLION 1E9
#define CPU_FREQUENCY 700000000  // 700 MHz

// const char *task_command_name_ff[] ={
//     "taskset -c 0 python ../rt_tasks/ab2_nav_ob_avoid.py",
//     "taskset -c 1 python ../rt_tasks/ab2_camera.py",
//     "taskset -c 2 python ../rt_tasks/ab2_sensor_log.py",
//     "taskset -c 3 python ../rt_tasks/ab2_coretemp_log.py",
//     "taskset -c 3 python ../rt_tasks/ab2_location_log.py",
//     "taskset -c 2 sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
//     "taskset -c 3 python ../cus_se_task/km_log.py > kmout.txt",
//     "taskset -c 1 sudo tripwire --check -s --rule-name \"Tripwire Binaries\" > twout.txt"
// };

//
// const char *task_command_name_prop[] ={
//     "taskset -c 0 python ../rt_tasks/ab2_nav_ob_avoid.py",
//     "taskset -c 1 python ../rt_tasks/ab2_camera.py",
//     "taskset -c 2 python ../rt_tasks/ab2_sensor_log.py",
//     "taskset -c 3 python ../rt_tasks/ab2_coretemp_log.py",
//     "taskset -c 3 python ../rt_tasks/ab2_location_log.py",
//     "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
//     "python ../cus_se_task/km_log.py > kmout.txt",
//     "sudo tripwire --check -s --rule-name \"Tripwire Binaries\" > twout.txt"
// };


const char *task_command_name_ff[] ={
    "taskset -c 0 python ../rt_tasks/ab2_nav_ob_avoid.py",
    "taskset -c 1 python ../rt_tasks/ab2_camera.py",
    "taskset -c 1 sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
    "taskset -c 0 python ../cus_se_task/km_log.py > kmout.txt"
};

const char *task_command_name_prop[] ={
    "taskset -c 0 python ../rt_tasks/ab2_nav_ob_avoid.py",
    "taskset -c 1 python ../rt_tasks/ab2_camera.py",
    //"sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt && python ../cus_se_task/km_log.py > kmout.txt"
    "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
    "python ../cus_se_task/km_log.py > kmout.txt"
};

const char *task_command_name_vanilla[] ={
    "taskset -c 0 python ../rt_tasks/ab2_nav_ob_avoid.py",
    "taskset -c 1 python ../rt_tasks/ab2_camera.py"
};

//
// const int camera_task_indx_opp = 4;
// const int camera_task_indx_prop = 7;

const int se_task_indx_opp = 7;
const int se_task_indx_prop = 6;


struct timespec start;
//struct timespec attack_point;  // the time instance when attack launched
int isAttackLaunched = 0;

//, end;
//uint64_t diff;


uint64_t attack_launch_time;
uint32_t attack_point; // the time instance when attack launched

int firstTime = 1;


#endif /* GLOBALS_H */
