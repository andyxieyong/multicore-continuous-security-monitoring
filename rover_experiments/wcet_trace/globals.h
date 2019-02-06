#ifndef GLOBALS_H_INCLUDED
#define GLOBALS_H_INCLUDED

/* Define global variables here. */


const int EXP_COUNT = 200;

#define BILLION 1E9
#define CPU_FREQUENCY 700000000  // 700 MHz

const char *task_command_name[] ={
    "python ../rt_tasks/ab2_nav_ob_avoid.py",
    "python ../rt_tasks/ab2_sensor_log.py",
    "python ../rt_tasks/ab2_camera.py",
    "python ../rt_tasks/ab2_coretemp_log.py",
    "python ../rt_tasks/ab2_location_log.py ",
    "sudo tripwire --check -s --rule-name \"Tripwire Binaries\" > twout.txt",
    "sudo tripwire --check -s --rule-name \"Root file-system executables\" > twout.txt",
    "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt",
    "python ../cus_se_task/km_log.py > kmout.txt",
    "sudo tripwire --check -s --rule-name \"MC Rover Logs\" > twout.txt && python ../cus_se_task/km_log.py > kmout.txt"
};

#endif /* GLOBALS_H */
