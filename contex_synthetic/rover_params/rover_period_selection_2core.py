# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"


from __future__ import division

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import copy

import task as tsk
import experiment_handler as eh
import sched_functions as schf

# time units are millisecond

def get_rover_rt_tasket():
    # task order: navigation, camera

    n_rt_task = 2

    rt_task_tid = ['navigation', 'camera']

    wcets = [240.0, 1120.0]
    periods = [500, 5000]

    utils = [wcet / period for wcet, period in zip(wcets, periods)]

    print "== RT TASK STAT =="
    print "WCET:", wcets
    print "PERIOD:", periods
    print "UTIL:", utils
    print "Total RT Util:", sum(utils)
    print "==================="

    rt_taskset = []
    for i in range(0, n_rt_task):
        rt_taskset.append(tsk.RT_Task(wcets[i], periods[i], utils[i], periods[i], tid=rt_task_tid[i]))

    return rt_taskset, utils


def get_rover_se_taskset():

    n_se_task = 2

    # task order: tw_roverlogscan, cus_kmlog, tw_onwbin

    se_task_tid = ['tw_roverlogscan', 'cus_kmlog']

    wcets = [5342.0, 223.0]
    periods_max = [10000, 10000]
    utils = [wcet / period for wcet, period in zip(wcets, periods_max)]

    print "== SE TASK STAT =="
    print "WCET:", wcets
    print "PERIOD_MAX:", periods_max
    print "(Min) UTIL:", utils
    print "Total SE Min Util:", sum(utils)
    print "==================="

    se_taskset = []
    for i in range(0, n_se_task):
        se_taskset.append(tsk.SE_Task(wcet=wcets[i],
                                      period=periods_max[i],
                                      period_max=periods_max[i],
                                      util=utils[i],
                                      deadline=periods_max[i], tid=se_task_tid[i]))

    return se_taskset, utils


def prepare_rover_taskset():

    n_core = 2

    rover_rt_taskset, total_rt_util = get_rover_rt_tasket()
    rover_se_taskset, total_se_util = get_rover_se_taskset()

    n_rt_task = len(rover_rt_taskset)
    n_se_task = len(rover_se_taskset)

    total_system_util = total_rt_util + total_se_util

    tc = tsk.TaskSetConfig(n_core, total_system_util, total_rt_util, total_se_util, n_rt_task, n_se_task,
                           rover_rt_taskset, rover_se_taskset)

    return tc


def get_rt_core_assignement(n_rt_task, n_core):
    x = np.zeros((n_rt_task, n_core))

    x[0][0] = 1
    x[1][1] = 1

    return x


def prepare_rt_taskset(tcconfig):

    """Set core assignment and check schedulability of RT tasks"""

    core_assignment = get_rt_core_assignement(tcconfig.n_rt_task, tcconfig.n_core)
    is_sched = schf.check_rt_schedulability(rt_taskset=tcconfig.rt_taskset, core_assignment=core_assignment)
    if is_sched:
        # print "RT Tasks schedulable!"
        # update the wcrt variable in RT taskset
        schf.set_wcrt_all_rt_task(rt_taskset=tcconfig.rt_taskset, core_assignment=core_assignment)
        tcconfig.rt_core_assignment = copy.deepcopy(core_assignment)
        return True
    else:
        return False


if __name__ == "__main__":

    tcconfig = prepare_rover_taskset()

    prt = prepare_rt_taskset(tcconfig)

    if prt:
        print "=== RT TASKSET SCHEDULABLE ==="
        for rt_tsk in tcconfig.rt_taskset:
            print rt_tsk.tid, "-> wcet:", rt_tsk.wcet, "wcrt:", rt_tsk.wcrt, "period:", rt_tsk.period

        print "== RT TASK ALLOCATION == "
        print tcconfig.rt_core_assignment

        tcconfig_proposed = copy.deepcopy(tcconfig)
        tcconfig_ff = copy.deepcopy(tcconfig)

        # proposed scheme
        is_se_sched_prop = schf.get_se_periods_proposed(tcconfig=tcconfig_proposed)

        if is_se_sched_prop:
            print "\n PROP: Taskset is schedulable. Printing periods and WCRT.."
            for se_tsk in tcconfig_proposed.se_taskset:
                print se_tsk.tid, "-> wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max


        # now test with best-fit scheme
        is_se_sched_ff = schf.get_se_periods_bestfit(tcconfig=tcconfig_ff)

        if is_se_sched_ff:
            print "\n FF: Taskset is schedulable. Printing periods and WCRT.."
            for se_tsk in tcconfig_ff.se_taskset:
                print se_tsk.tid, "-> wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max
            print "FF SE Core Alloc:\n", tcconfig_ff.ff_se_core_assignment
    print "Script finished!"
