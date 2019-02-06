# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

from collections import defaultdict
import numpy as np
import math
import random
import copy
import helper_functions as hf
from config import *
import task as tsk


def get_periods(n, low, high):
    """ Returns n periods (integers) for a given range  """

    # periods = np.random.choice(range(low, high+1), n, replace=False)

    # returns using log-uniform distribution
    # See the paper: Techniques For The Synthesis Of Multiprocessor Tasksets, WATERS 2010
    tg = 1
    periods = np.random.uniform(np.log(low), np.log(high+tg), n)
    periods = [math.floor(np.exp(ti)/tg) * tg for ti in periods]

    # shorter index higher priority
    return np.sort(periods)


def get_utils(n, base_util):
    """ Returns the n utilization values using Stafford Rand Fixed Sum Algorithm """
    return hf.get_util_by_rand_fixed_sum(n, base_util)


def get_wcets(utils, periods):
    """ Returns WCET """
    return [ui * ti for ui, ti in zip(utils, periods)]
    # return [math.ceil(ui * ti) for ui, ti in zip(utils, periods)]


def get_rt_taskset(n, total_rt_util):
    """ Returns RT takset (a list of n RT task) """

    periods = get_periods(n, PARAMS.RT_PERIOD_MIN, PARAMS.RT_PERIOD_MAX)
    utils = get_utils(n, total_rt_util)
    wcets = get_wcets(utils, periods)

    rt_taskset = []
    for i in range(0, n):
        rt_taskset.append(tsk.RT_Task(wcets[i], periods[i], utils[i], periods[i], tid=i))

    return rt_taskset


def get_se_taskset(n, total_se_util):
    """ Returns SE takset (a list of n SE task) """

    periods = get_periods(n, PARAMS.SE_PERIOD_MAX_LO, PARAMS.SE_PERIOD_MAX_HI)
    utils = get_utils(n, total_se_util)
    wcets = get_wcets(utils, periods)

    se_taskset = []
    for i in range(0, n):
        se_taskset.append(tsk.SE_Task(wcet=wcets[i],
                                       period=periods[i],
                                       period_max=periods[i],
                                       util=utils[i],
                                       deadline=periods[i], tid=i))

    return se_taskset


def generate_taskset(n_core, n_rt_task, n_se_task, total_system_util):

    """ Generate RT and SE Taskset """

    # We assume lower index higher priority (and also lower index -> shorter period)

    total_se_util = total_system_util * PARAMS.SE_UTIL_PERCENTAGE  # at least X% of the Total Util
    total_rt_util = total_system_util - total_se_util

    rt_taskset = get_rt_taskset(n_rt_task, total_rt_util)
    se_taskset = get_se_taskset(n_se_task, total_se_util)

    return tsk.TaskSetConfig(n_core, total_system_util, total_rt_util, total_se_util, n_rt_task, n_se_task, rt_taskset, se_taskset)


def get_rt_se_util_by_total_util(total_system_util):
    """ Returns RT and SE Util given total util """
    total_se_util = total_system_util * PARAMS.SE_UTIL_PERCENTAGE  # at least X% of the Total Util
    total_rt_util = total_system_util - total_se_util

    return total_rt_util, total_se_util


def generate_all_tasksets():
    """ Generate the all taskset for all core configurations """

    all_task_set_dict = defaultdict(lambda: defaultdict(dict))

    for core in PARAMS.CORE_LIST:
        util_list = get_util_list_by_core(core)
        for util in util_list:
            print "Core:", core, "System Utilization:", util
            for ntc in range(0, PARAMS.N_TASKSET_EACH_CONF):

                # print "Core:", core, "System Utilization:", util, "Taskset Index:", ntc

                n_rt_task = random.randint(PARAMS.N_RT_TASK_MIN * core, PARAMS.N_RT_TASK_MAX * core)
                n_se_task = random.randint(PARAMS.N_SE_TASK_MIN * core, PARAMS.N_SE_TASK_MAX * core)

                taskset = generate_taskset(core, n_rt_task, n_se_task, util)
                all_task_set_dict[core][util][ntc] = copy.deepcopy(taskset)

    return all_task_set_dict


def generate_all_tasksets_base_util():
    """ Generate the all taskset for all core configurations (using base utilization) """

    all_task_set_dict = defaultdict(lambda: defaultdict(dict))

    for core in PARAMS.CORE_LIST:
        total_grp = PARAMS.N_BASE_UTIL_GRP
        for u in range(total_grp):

            # print "Core:", core, "Group", u

            for ntc in range(0, PARAMS.N_TASKSET_EACH_CONF):

                util = random.uniform((0.02 + 0.1 * u)*core, (0.08 + 0.1 * u)*core)
                print "Core:", core, "Group", u, "Taskset Index:", ntc, "System Utilization:", util

                # print "Core:", core, "System Utilization:", util, "Taskset Index:", ntc

                n_rt_task = random.randint(PARAMS.N_RT_TASK_MIN * core, PARAMS.N_RT_TASK_MAX * core)
                n_se_task = random.randint(PARAMS.N_SE_TASK_MIN * core, PARAMS.N_SE_TASK_MAX * core)

                taskset = generate_taskset(core, n_rt_task, n_se_task, util)
                all_task_set_dict[core][u][ntc] = copy.deepcopy(taskset)

    return all_task_set_dict


def get_basegrp_util_list_by_core(n_core):
    """ return utilization based on the concept of utilization groups """

    total_grp = n_core * PARAMS.N_BASE_UTIL_GRP
    util_list = []
    for i in range(PARAMS.N_TASKSET_EACH_CONF):
        for u in range(total_grp):
            base_util = random.uniform(0.02 + 0.1 * u, 0.08 + 0.1 * u)
            util_list.append(base_util)
    return util_list




def get_util_list_by_core(core):
    """ Return the list of total utilization values we analyze based on Multi-core paper """

    return np.arange(PARAMS.UTIL_RANGE_MIN * core, PARAMS.UTIL_RANGE_MAX * core, PARAMS.UTIL_RANGE_STEP * core)
