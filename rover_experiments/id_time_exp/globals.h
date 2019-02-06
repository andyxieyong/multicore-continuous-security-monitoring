#ifndef GLOBALS_H_INCLUDED
#define GLOBALS_H_INCLUDED

/* Define global variables here. */


const int EXP_COUNT = 100;

#define BILLION 1E9
#define CPU_FREQUENCY 700000000  // 700 MHz

// const char *task_command_name_ff[] ={
//     "python ../rt_tasks/ab2_navigation.py forward",
//     "python ../rt_tasks/ab2_navigation.py backward",
//     "python ../rt_tasks/ab2_navigation.py left",
//     "python ../rt_tasks/ab2_navigation.py right",
//     "python ../rt_tasks/ab2_camera.py",
//     "python ../rt_tasks/ab2_sensor_log.py",
//     "sudo tripwire --check -s --rule-name \"Tripwire Binaries\" > twout.txt",
//     "sudo tripwire --check -s --rule-name \"Rover Logs\" > twout.txt",
//     "sudo tripwire --check -s --rule-name \"Root file-system executables\" > twout.txt"
// };


//
// const char *task_command_name_prop[] ={
//     "python ../rt_tasks/ab2_navigation.py forward",
//     "python ../rt_tasks/ab2_navigation.py backward",
//     "python ../rt_tasks/ab2_navigation.py left",
//     "python ../rt_tasks/ab2_navigation.py right",
//     "python ../rt_tasks/ab2_camera.py",
// 	"sudo tripwire --check -s --rule-name \"Tripwire Binaries\" > twout.txt",
//     "sudo tripwire --check -s --rule-name \"Rover Logs\" > twout.txt",
//     "sudo tripwire --check -s --rule-name \"Root file-system executables\" > twout.txt",
//     "python ../rt_tasks/ab2_sensor_log.py"
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
    // "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt && python ../cus_se_task/km_log.py > kmout.txt"
    "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
    "python ../cus_se_task/km_log.py > kmout.txt"
};


const int se_task_indx_1 = 2;
const int se_task_indx_2 = 3;


struct timespec start;
//struct timespec attack_point;  // the time instance when attack launched
int isAttackLaunched = 0;

//, end;
//uint64_t diff;


uint64_t attack_launch_time;
uint32_t attack_point; // the time instance when attack launched

int firstTime = 1;
int isSETerminate = 0;

int quit_1 = 0, quit_2 = 0;  // for se tasks

long double t2detect_1, t2detect_2;


#endif /* GLOBALS_H */
