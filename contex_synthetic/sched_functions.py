# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

from __future__ import division
import numpy as np
import itertools
import copy
import math
# import gc
import helper_functions as hf
import warnings
from config import *


class CINCPartition:
    def __init__(self, ci_idx_list, nc_idx_list):
        self.ci_idx_list = copy.deepcopy(ci_idx_list)
        self.nc_idx_list = copy.deepcopy(nc_idx_list)


def get_interference_core_m(rt_taskset, rt_task_indx, core_indx, core_assignment):

    # get interference for a given core (and the assignment)

    intf = 0
    for tindx in range(rt_task_indx):
        intf += core_assignment[tindx][core_indx] * (rt_taskset[rt_task_indx].period / rt_taskset[tindx].period + 1) * rt_taskset[tindx].wcet

        # print "Core", core_indx, "Task", tindx, "current interference", intf

    return intf


def get_all_rt_interference_core_m(rt_taskset, core_indx, core_assignment, se_period):

    # get interference from all RT tasks for a given core (and the assignment)

    intf = 0
    for tindx in range(len(rt_taskset)):
        intf += core_assignment[tindx][core_indx] * (se_period / rt_taskset[tindx].period + 1) * rt_taskset[tindx].wcet

        # print "Core", core_indx, "Task", tindx, "current interference", intf

    return intf


def get_se_interference_core_m(se_taskset, core_indx, se_core_assignment, se_task_indx, se_period):

    # get interference from se tasks for a given core (and the assignment) :: For best-fit SE method

    intf = 0
    for tindx in range(se_task_indx):
        intf += se_core_assignment[tindx][core_indx] * (se_period / se_taskset[tindx].period + 1) * se_taskset[tindx].wcet

        # print "Core", core_indx, "Task", tindx, "current interference", intf

    return intf


def check_sched_for_given_core(rt_taskset, rt_task_indx, core_indx, core_assignment):

    # check whether WCRT is less than deadline (e.g. period)

    intf = get_interference_core_m(rt_taskset=rt_taskset,
                                   rt_task_indx=rt_task_indx,
                                   core_indx=core_indx,
                                   core_assignment=core_assignment)

    wcrt = rt_taskset[rt_task_indx].wcet + intf

    if wcrt <= rt_taskset[rt_task_indx].period:
        return True
    return False


def get_feasible_core_index(rt_taskset, rt_task_indx, core_assignment, n_core):
    core_list = []

    # core index in from 0 to m-1
    for ci in range(n_core):

        is_sched = check_sched_for_given_core(rt_taskset=rt_taskset,
                                              rt_task_indx=rt_task_indx,
                                              core_indx=ci,
                                              core_assignment=core_assignment)

        if is_sched:
            core_list.append(ci)

    return core_list


def get_core_with_min_util(rt_taskset, n_rt_task, core_list, core_assignment):

    # return the core index with minimum utilization

    min_util = 100  # a large number
    min_m = -1  # init to a -ve value
    for m in core_list:
        util = [(rt_taskset[i].wcet/rt_taskset[i].period) * core_assignment[i][m] for i in range(0, n_rt_task)]
        util = sum(util)

        if min_util > util:
            min_util = util
            min_m = m

    return min_m


def get_rt_core_assignment(rt_taskset, n_core, strategy=PARAMS.RT_ALLOC_STRATEGY):
    """ Return the RT task assignment using Best FIT stategy
        Output: a 2D Matrix X: x[i,j] = i if task i assigned to core j"""

    # Best-fit: choosing the core that has minimum workload (utilization)

    # the allocation matrix
    n_rt_task = len(rt_taskset)
    x = np.zeros((n_rt_task, n_core))

    x[0][0] = 1  # first task is always core zero

    for tindx in range(1, n_rt_task):
        core_list = get_feasible_core_index(rt_taskset=rt_taskset,
                                rt_task_indx=tindx, core_assignment=x,
                                n_core=n_core)

        if core_list:

            # print core_list

            if strategy == PARAMS.RT_ALLOC_BF:

                core_indx = get_core_with_min_util(rt_taskset=rt_taskset,
                                                   n_rt_task=n_rt_task,
                                                   core_list=core_list,
                                                   core_assignment=x)
            elif strategy == PARAMS.RT_ALLOC_FF:
                core_indx = min(core_list)

            # print "core indx", core_indx

            x[tindx][core_indx] = 1  # assign task to that core

        else:
            print "RT Taskset Unshcedulable for core and RT Util:", "(", n_core, ",", rt_taskset[tindx].util, ")"
            return None

    # print x
    return x


def check_rt_schedulability(rt_taskset, core_assignment):

    n_rt_task = len(rt_taskset)
    for tindx in range(n_rt_task):
        # get the core where RT task is assigned (assuming it is get assignment)
        m = list(core_assignment[tindx, :]).index(1)
        intf = get_interference_core_m(rt_taskset=rt_taskset,
                                       rt_task_indx=tindx, core_indx=m, core_assignment=core_assignment)
        wcrt = rt_taskset[tindx].wcet + intf

        # print "Task", tindx, "Period:", rt_taskset[tindx].period, "WCET", rt_taskset[tindx].wcet, "WCRT:", wcrt
        if wcrt >= rt_taskset[tindx].deadline:
            return False

    return True


def do_get_wcrt_upper_bound(rt_taskset, task_indx, core_assignment):
    m = list(core_assignment[task_indx, :]).index(1)  # which core the task is assigned
    intf = get_interference_core_m(rt_taskset=rt_taskset,
                                   rt_task_indx=task_indx, core_indx=m, core_assignment=core_assignment)
    wcrt = rt_taskset[task_indx].wcet + intf
    return wcrt


def do_get_rt_wcrt_fixed_point(rt_taskset, task_indx, core_assignment):

    x = rt_taskset[task_indx].wcet
    m = list(core_assignment[task_indx, :]).index(1)  # which core the task is assigned
    max_ctr = PARAMS.FIXED_POINT_MAX_BOUND  # an upperbound counter
    ctr = 0

    while True:
        intf = [core_assignment[i][m] * math.ceil(x / rt_taskset[i].period) * rt_taskset[i].wcet for i in range(0, task_indx)]
        intf = sum(intf)
        # print "intf:", intf

        x_new = rt_taskset[task_indx].wcet + intf

        # print "x:", x, "xnew", x_new

        if x == x_new:
            return x

        if ctr >= max_ctr:
            return -1

        x = x_new
        ctr += 1


def set_wcrt_all_rt_task(rt_taskset, core_assignment):

    for tindx in range(len(rt_taskset)):
        wcrt = do_get_rt_wcrt_fixed_point(rt_taskset=rt_taskset,
                                           task_indx=tindx,
                                           core_assignment=core_assignment)
        if wcrt < 0:
            wcrt = do_get_wcrt_upper_bound(rt_taskset=rt_taskset,
                                           task_indx=tindx,
                                           core_assignment=core_assignment)
        rt_taskset[tindx].wcrt = wcrt
        # print "Task:", tindx, "WCRT", wcrt

    return wcrt


def get_z_combinations(n_rt_task, se_task_indx, n_core):
    hpset = list(range(n_rt_task+se_task_indx))
    hpseset = list(range(n_rt_task, n_rt_task+se_task_indx))
    # print hpset
    # print hpseset

    all_ci_list = []  # list of all carry-in index
    # iterate m-1 time (where m is the number of cores)
    for c in range(0, n_core):
        cmblist = list(itertools.combinations(hpseset, c))
        # print "cmpblist", cmblist
        all_ci_list.append(cmblist)

    all_ci_list = [item for sublist in all_ci_list for item in sublist]  # flatten the list
    # print "allci:", all_ci_list

    z_combination_list = []

    for ci_list in all_ci_list:
        # print "hpset:", hpset, "cilist:", list(ci_list)
        nc_list = list(set(hpset) - set(list(ci_list)))
        zcomb = CINCPartition(ci_idx_list=list(ci_list), nc_idx_list=nc_list)
        # print "CI:", zcomb.ci_idx_list, "NC:", zcomb.nc_idx_list
        z_combination_list.append(zcomb)

    return z_combination_list


def get_carry_in_workload(x, wcet, period):
    """ Returns carry-in workload """
    ciw = math.floor(x/period) * wcet + min(x % period, wcet)
    return ciw


def get_nc_intf(tcconfig, x, nc_intf_list, se_task_indx):
    """ x is the window size, returns the carry in interference """
    intf = 0

    for ti in nc_intf_list:

        if ti < tcconfig.n_rt_task:
            intf_task = tcconfig.rt_taskset[ti]  # this is RT task
        else:
            intf_task = tcconfig.se_taskset[ti % tcconfig.n_rt_task]  # se task, get proper index

        w = get_carry_in_workload(x=x, wcet=intf_task.wcet, period=intf_task.period)
        ii = min(max(w, 0), x - tcconfig.se_taskset[se_task_indx].wcet + 1)
        intf += ii
        # print "x:",x, "TI:", ti, "II:", ii, "intf:", intf

    return intf



def get_rt_nc_intf_all_global(tcconfig, x, nc_intf_list, rt_task_indx):
    """ x is the window size, returns the carry in interference """
    intf = 0

    for ti in nc_intf_list:

        intf_task = tcconfig.rt_taskset[ti]  # this is RT task

        w = get_carry_in_workload(x=x, wcet=intf_task.wcet, period=intf_task.period)
        ii = min(max(w, 0), x - tcconfig.rt_taskset[rt_task_indx].wcet + 1)
        intf += ii
        # print "x:",x, "TI:", ti, "II:", ii, "intf:", intf

    return intf


def get_xh_and_delh(wcet, period, wcrt):
    # return the xp value in the paper:
    # Improving the Response Time Analysis of Global Fixed-Priority Multiprocessor Scheduling
    xh = wcet - 1 + math.floor((wcrt-wcet)/(period-wcet)) * period - wcrt
    delh = math.floor((wcrt-wcet)/(period-wcet)) * wcet - 1
    return xh, delh


def get_ci_intf(tcconfig, x, ci_intf_list, se_task_indx):

    """ Returns carry-in interference (only SE tasks can have carry-in) """
    intf = 0

    for ti in ci_intf_list:

        indx = ti % tcconfig.n_rt_task
        intf_task = tcconfig.se_taskset[indx]  # se task, get proper index

        xh, delh = get_xh_and_delh(wcet=intf_task.wcet, period=intf_task.period,
                                   wcrt=intf_task.wcrt)

        w = get_carry_in_workload(x=max(x-xh, 0), wcet=intf_task.wcet, period=intf_task.period) + min(x, delh)
        ii = min(max(w, 0), x - tcconfig.se_taskset[se_task_indx].wcet + 1)
        intf += ii

    return intf


def get_ci_intf_all_global(tcconfig, x, ci_intf_list, se_task_indx):

    """ Returns carry-in interference (only SE tasks can have carry-in) """
    intf = 0

    for ti in ci_intf_list:

        if ti < tcconfig.n_rt_task:
            intf_task = tcconfig.rt_taskset[ti]  # this is RT task
        else:
            intf_task = tcconfig.se_taskset[ti % tcconfig.n_rt_task]  # se task, get proper index

        xh, delh = get_xh_and_delh(wcet=intf_task.wcet, period=intf_task.period,
                                   wcrt=intf_task.wcrt)

        w = get_carry_in_workload(x=max(x-xh, 0), wcet=intf_task.wcet, period=intf_task.period) + min(x, delh)
        ii = min(max(w, 0), x - tcconfig.se_taskset[se_task_indx].wcet + 1)
        intf += ii

    return intf


def get_rt_ci_intf_all_global(tcconfig, x, ci_intf_list, rt_task_indx):

    """ Returns carry-in interference (only SE tasks can have carry-in) """
    intf = 0

    for ti in ci_intf_list:

        intf_task = tcconfig.rt_taskset[ti]  # this is interfering RT task

        xh, delh = get_xh_and_delh(wcet=intf_task.wcet, period=intf_task.period,
                                   wcrt=intf_task.wcrt)

        w = get_carry_in_workload(x=max(x-xh, 0), wcet=intf_task.wcet, period=intf_task.period) + min(x, delh)
        ii = min(max(w, 0), x - tcconfig.rt_taskset[rt_task_indx].wcet + 1)
        intf += ii

    return intf


def get_total_intf_by_window_given_nc_ci(tcconfig, x, nc_intf_list, ci_intf_list, se_task_indx, _allglobal):
    """ x is the window size, returns total interference """
    ncintf = get_nc_intf(tcconfig=tcconfig, x=x, nc_intf_list=nc_intf_list, se_task_indx=se_task_indx)

    if not ci_intf_list:
        ciintf = 0
    else:
        # this is the scheme for all global scheduling as Rodolfo mentioned
        if _allglobal:
            ciintf = get_ci_intf_all_global(tcconfig=tcconfig, x=x, ci_intf_list=ci_intf_list, se_task_indx=se_task_indx)
        else:
            # this is the propsed scheme
            ciintf = get_ci_intf(tcconfig=tcconfig, x=x, ci_intf_list=ci_intf_list, se_task_indx=se_task_indx)

    # print "ncintf", ncintf
    # print "ciintf", ciintf
    total_intf = ciintf + ncintf

    return total_intf


def get_rt_total_intf_by_window_given_nc_ci_all_global(tcconfig, x, nc_intf_list, ci_intf_list, rt_task_indx):
    """ x is the window size, returns total interference """
    ncintf = get_rt_nc_intf_all_global(tcconfig=tcconfig, x=x, nc_intf_list=nc_intf_list, rt_task_indx=rt_task_indx)

    if not ci_intf_list:
        ciintf = 0
    else:
        # this is the scheme for all global scheduling as Rodolfo mentioned

        ciintf = get_rt_ci_intf_all_global(tcconfig=tcconfig, x=x, ci_intf_list=ci_intf_list, rt_task_indx=rt_task_indx)


    # print "ncintf", ncintf
    # print "ciintf", ciintf
    total_intf = ciintf + ncintf

    return total_intf


def get_wcrt_given_nc_ci(tcconfig, nc_intf_list, ci_intf_list, se_task_indx, _allglobal=False):
    """ Returns the WCRT using fixed point iteration """
    x = tcconfig.se_taskset[se_task_indx].wcet
    # x = math.ceil(x)

    # print "==== xinit: ====", x
    # rt_util = [rt_tc.wcet/rt_tc.period for rt_tc in tcconfig.rt_taskset]
    # print "RT Util(before)", tcconfig.rt_util, "RT Util after rouding", sum(rt_util)

    max_ctr = PARAMS.FIXED_POINT_MAX_BOUND  # an upperbound counter
    # ctr = 0

    while True:

        intf = get_total_intf_by_window_given_nc_ci(tcconfig=tcconfig, x=x,
                                                    nc_intf_list=nc_intf_list,
                                                    ci_intf_list=ci_intf_list,
                                                    se_task_indx=se_task_indx,
                                                    _allglobal=_allglobal)

        # print "intf:", intf

        x_new = math.floor(intf/tcconfig.n_core) + tcconfig.se_taskset[se_task_indx].wcet
        # x_new = math.floor(intf/tcconfig.n_core) + math.ceil(tcconfig.se_taskset[se_task_indx].wcet)

        # print "x:", x, "xnew", x_new

        if x == x_new:
            return x

        # unschedulable anyways
        if x_new > tcconfig.se_taskset[se_task_indx].period_max:
            # print "x new greater than period max"
            return -1

        # if ctr >= max_ctr:
        #     return -1

        x = x_new
        # ctr += 1


def get_rt_wcrt_given_nc_ci_all_global(tcconfig, nc_intf_list, ci_intf_list, rt_task_indx):
    """ Returns the WCRT using fixed point iteration """
    x = tcconfig.rt_taskset[rt_task_indx].wcet
    # x = math.ceil(x)

    # print "==== xinit: ====", x
    # rt_util = [rt_tc.wcet/rt_tc.period for rt_tc in tcconfig.rt_taskset]
    # print "RT Util(before)", tcconfig.rt_util, "RT Util after rouding", sum(rt_util)

    max_ctr = PARAMS.FIXED_POINT_MAX_BOUND  # an upperbound counter


    while True:

        intf = get_rt_total_intf_by_window_given_nc_ci_all_global(tcconfig=tcconfig, x=x,
                                                    nc_intf_list=nc_intf_list,
                                                    ci_intf_list=ci_intf_list,
                                                    rt_task_indx=rt_task_indx)

        # print "intf:", intf

        x_new = math.floor(intf/tcconfig.n_core) + tcconfig.rt_taskset[rt_task_indx].wcet
        # x_new = math.floor(intf/tcconfig.n_core) + math.ceil(tcconfig.se_taskset[se_task_indx].wcet)

        # print "x:", x, "xnew", x_new

        if x == x_new:
            return x

        # unschedulable anyways
        if x_new > tcconfig.rt_taskset[rt_task_indx].deadline:
            # print "x new greater than period max"
            return -1


        x = x_new


def do_calculate_se_task_wcrt(tcconfig, se_task_indx):
    z_combination_list = get_z_combinations(n_rt_task=tcconfig.n_rt_task, se_task_indx=se_task_indx,
                                            n_core=tcconfig.n_core)

    max_wcrt = -1  # a negative number
    # print "SE Task indx:", se_task_indx
    for zcl in z_combination_list:
        # print "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list
        # wcrt = get_wcrt_given_nc_ci(tcconfig=tcconfig,
        #                             nc_intf_list=zcl.nc_idx_list,
        #                             ci_intf_list=zcl.ci_idx_list,
        #                             se_task_indx=se_task_indx)

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                wcrt = get_wcrt_given_nc_ci(tcconfig=tcconfig,
                                            nc_intf_list=zcl.nc_idx_list,
                                            ci_intf_list=zcl.ci_idx_list,
                                            se_task_indx=se_task_indx,
                                            _allglobal=False)
            except Warning as e:
                print('Overflow in WCRT calculation:', e)
                continue

        if wcrt > 0 and wcrt > max_wcrt:
            # print "Se indx", se_task_indx, "wcrt:", wcrt, "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list
            max_wcrt = wcrt
        # else:
        #     print "this wcrt", wcrt, "current_max", max_wcrt, "Se indx", se_task_indx, "wcrt:", wcrt, "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list

    return max_wcrt


def do_calculate_se_task_wcrt_all_global(tcconfig, se_task_indx):
    z_combination_list = get_z_combinations_all_global(n_rt_task=tcconfig.n_rt_task, se_task_indx=se_task_indx,
                                            n_core=tcconfig.n_core)

    max_wcrt = -1  # a negative number
    # print "SE Task indx:", se_task_indx
    for zcl in z_combination_list:
        # print "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list
        # wcrt = get_wcrt_given_nc_ci(tcconfig=tcconfig,
        #                             nc_intf_list=zcl.nc_idx_list,
        #                             ci_intf_list=zcl.ci_idx_list,
        #                             se_task_indx=se_task_indx)

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                wcrt = get_wcrt_given_nc_ci(tcconfig=tcconfig,
                                            nc_intf_list=zcl.nc_idx_list,
                                            ci_intf_list=zcl.ci_idx_list,
                                            se_task_indx=se_task_indx,
                                            _allglobal=True)
            except Warning as e:
                print('Overflow in WCRT calculation:', e)
                continue

        if wcrt > 0 and wcrt > max_wcrt:
            # print "Se indx", se_task_indx, "wcrt:", wcrt, "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list
            max_wcrt = wcrt
        # else:
        #     print "this wcrt", wcrt, "current_max", max_wcrt, "Se indx", se_task_indx, "wcrt:", wcrt, "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list

    return max_wcrt


def check_se_schedulability(tcconfig, se_task_indx):

    # print "SE period list:", [setc.period for setc in tcconfig.se_taskset]
    # print "SE WCET list:", [setc.wcet for setc in tcconfig.se_taskset]
    # print "SE Wcrt list:", [setc.wcrt for setc in tcconfig.se_taskset]
    # print "SE Intf list:", [setc.wcrt-setc.wcet for setc in tcconfig.se_taskset]

    wcrt = do_calculate_se_task_wcrt(tcconfig=tcconfig, se_task_indx=se_task_indx)

    if wcrt > 0 and wcrt < tcconfig.se_taskset[se_task_indx].period_max:
        return True, wcrt
    return False, -1


def check_se_schedulability_all_global(tcconfig, se_task_indx):

    wcrt = do_calculate_se_task_wcrt_all_global(tcconfig=tcconfig, se_task_indx=se_task_indx)

    if wcrt > 0 and wcrt < tcconfig.se_taskset[se_task_indx].period_max:
        tcconfig.se_taskset[se_task_indx].wcrt = wcrt  # update wcrt
        return True
    return False


def get_period_by_bin_search(tcconfig, se_task_indx):

    # print "WCRT inside", tcconfig.se_taskset[se_task_indx].wcrt

    tmin = int(math.floor(tcconfig.se_taskset[se_task_indx].wcrt + 1))
    tmax = int(tcconfig.se_taskset[se_task_indx].period_max)
    if PARAMS.SHOW_DEBUG_MSG:
        print "Optimizing periods for SE Task:", se_task_indx,  " --> Tmin", tmin, "Tmax:", tmax, "..."

    feasible_period_list = []

    # linear search
    # for t in range(tmin, tmax+1):
    #     tcnfg_local = copy.deepcopy(tcconfig)
    #     tcnfg_local.se_taskset[se_task_indx].period = t
    #     feasible_period = True
    #     for lpindx in range(se_task_indx+1, tcconfig.n_se_task):
    #         # print "T:", t, "lp indx:", lpindx
    #         is_sched, lpwcrt = check_se_schedulability(tcconfig=tcnfg_local, se_task_indx=lpindx)
    #         if not is_sched:
    #             print "not feasible for period:", t
    #             feasible_period = False
    #             break
    #         else:
    #             print "for T:", t, "lp indx:", lpindx, "lp wcrt:", lpwcrt
    #             tcnfg_local.se_taskset[lpindx].wcrt = lpwcrt
    #
    #     if feasible_period:
    #         feasible_period_list.append(t)

    # binary search
    if tmin > tmax:
        return None  # WCRT > desired period, not feasible

    # this is the lowest prio task
    if se_task_indx == tcconfig.n_se_task-1:
        feasible_period_list.append(tmin)
    else:
        # find the minimum period using binary search considering schedulability of all LP SE tasks

        tl = tmin
        tr = tmax
        while tl <= tr:
            tm = math.floor((tl + tr) / 2)
            # print "Tm", tm
            tcnfg_local = copy.deepcopy(tcconfig)
            tcnfg_local.se_taskset[se_task_indx].period = tm
            feasible_period = True
            is_sched_tm = True
            for lpindx in range(se_task_indx + 1, tcconfig.n_se_task):
                # print "T:", t, "lp indx:", lpindx
                is_sched, lpwcrt = check_se_schedulability(tcconfig=tcnfg_local, se_task_indx=lpindx)

                if not is_sched:
                    # print "not feasible for period:", tm
                    feasible_period = False
                    # tl = tm + 1
                    is_sched_tm = False
                    break
                else:
                    # print "for Tm:", tm, "lp indx:", lpindx, "lp wcrt:", lpwcrt
                    tcnfg_local.se_taskset[lpindx].wcrt = lpwcrt
                    # tr = tm - 1

            if is_sched_tm:
                tr = tm - 1
                # print "tl:", tl, "tr:", tr
            else:
                tl = tm + 1
                # print "tl:", tl, "tr:", tr

            if feasible_period:
                feasible_period_list.append(tm)

            # gc.collect()  # free memory

    # print "feas p list", feasible_period_list
    if feasible_period_list:
        # return the minimum period
        tstar = min(feasible_period_list)
        return tstar
    else:
        # no feasible period found. Taskset is unschedulable
        return None


def get_se_periods_proposed_with_timeout(tcconfig):

    """ Try to get period within timeout """
    try:
        with hf.timeout_handler(int(PARAMS.EXP_TIMEOUT)):
            result = get_se_periods_proposed(tcconfig)
    except (RuntimeWarning, hf.TimeoutException):
        # if the solution is not found by timeout
        print "Proposed :: Unable to get periods. Timeout!!"
        return False

    return result


def get_se_periods_proposed(tcconfig):
    """ This is the main method that calculates the periods for SE tasks.
    If schedulable, update the period in tcconfig.se_taskset[j].period for each SE task j"""

    feasible_wcrt_list = [0] * tcconfig.n_se_task

    for se_task_indx in range(tcconfig.n_se_task):

        is_sched, wcrt = check_se_schedulability(tcconfig=tcconfig, se_task_indx=se_task_indx)
        # wcrt = do_calculate_se_task_wcrt(tcconfig=tcconfig, se_task_indx=se_task_indx)

        if not is_sched:
            print "--> PROP :: SE task", se_task_indx, "Unschedulable with Tmax:", \
                tcconfig.se_taskset[se_task_indx].period_max, "Return False <--"
            return False

        # print "SE task:", se_task_indx, "With Tmax:", tcconfig.se_taskset[se_task_indx].period_max, "WCRT:", wcrt
        tcconfig.se_taskset[se_task_indx].wcrt = wcrt  # update wcrt
        feasible_wcrt_list[se_task_indx] = wcrt  # saving wcrt if not optimization is successful

    # now optimize period
    is_optimize_successful = True

    if PARAMS.SHOW_DEBUG_MSG:
        print "Schedulable with Tmax. Now optimizing periods..."

    for se_task_indx in range(tcconfig.n_se_task):
        wcrt = do_calculate_se_task_wcrt(tcconfig=tcconfig, se_task_indx=se_task_indx)

        if wcrt >= 0:
            tcconfig.se_taskset[se_task_indx].wcrt = wcrt  # update wcrt
            tstar = get_period_by_bin_search(tcconfig=tcconfig, se_task_indx=se_task_indx)

            if tstar is not None:
                tcconfig.se_taskset[se_task_indx].period = tstar  # update period
                # print "SE task:", se_task_indx, "wcrt:", wcrt, "period:", tstar
            else:
                if PARAMS.SHOW_DEBUG_MSG:
                    print "Period optimization is not possible for SE task", \
                        se_task_indx, "Keeping period:", tcconfig.se_taskset[se_task_indx].period, "Tmax:", \
                        tcconfig.se_taskset[se_task_indx].period_max

        else:
            is_optimize_successful = False
            if PARAMS.SHOW_DEBUG_MSG:
                print "*** WCRT returns negative for SE task", se_task_indx, "Resetting to Tmax ***"
            break

    # reset to Tmax
    if not is_optimize_successful:
        for se_task_indx in range(tcconfig.n_se_task):
            tcconfig.se_taskset[se_task_indx].wcrt = feasible_wcrt_list[se_task_indx]
            tcconfig.se_taskset[se_task_indx].period = tcconfig.se_taskset[se_task_indx].period_max

    return True


def ff_tmax_get_total_intf_by_core_m_n_se_indx(tcconfig, se_task_indx, core_indx, se_alloc):
    """ Returns the total interference for Best-fit with Tmax case """

    se_period = tcconfig.se_taskset[se_task_indx].period_max

    rt_intf = get_all_rt_interference_core_m(rt_taskset=tcconfig.rt_taskset,
                                             core_indx=core_indx,
                                             core_assignment=tcconfig.rt_core_assignment,
                                             se_period=se_period)

    se_intf = get_se_interference_core_m(se_taskset=tcconfig.se_taskset,
                                         core_indx=core_indx,
                                         se_core_assignment=se_alloc,
                                         se_task_indx=se_task_indx, se_period=se_period)
    total_intf = rt_intf + se_intf

    # wcrt = tcconfig.se_taskset[se_task_indx].wcet + total_intf

    return total_intf


def ff_get_min_period_given_se_task_n_core_indx(tcconfig, se_task_indx, core_indx, se_alloc):

    se_period_min = int(math.floor(tcconfig.se_taskset[se_task_indx].wcet + 1))
    se_period_max = int(tcconfig.se_taskset[se_task_indx].period_max + 1)

    se_period_vec = list(range(se_period_min, se_period_max))

    feasible_period = []
    wcrt_list = []

    tmin = None

    for se_period in se_period_vec:

        rt_intf = get_all_rt_interference_core_m(rt_taskset=tcconfig.rt_taskset,
                                                 core_indx=core_indx,
                                                 core_assignment=tcconfig.rt_core_assignment,
                                                 se_period=se_period)

        se_intf = get_se_interference_core_m(se_taskset=tcconfig.se_taskset,
                                             core_indx=core_indx,
                                             se_core_assignment=se_alloc,
                                             se_task_indx=se_task_indx, se_period=se_period)
        total_intf = rt_intf + se_intf

        wcrt = tcconfig.se_taskset[se_task_indx].wcet + total_intf
        if wcrt <= se_period:
            # feasible_period.append(math.floor(tcconfig.se_taskset[se_task_indx].wcet + total_intf + 1))
            feasible_period.append(se_period)
            wcrt_list.append(wcrt)  # save it


    if feasible_period:
        idx = feasible_period.index(min(feasible_period))
        tmin = min(feasible_period)
        wcrt = wcrt_list[idx]

    # print "FF-> RT Intf:", rt_intf
    # print "FF-> Total Intf:", total_intf
    # print "FF -> Feas period: ", feasible_period

    # print "FF -> Core:", core_indx, "SE Task", se_task_indx, "Tmax:", tcconfig.se_taskset[se_task_indx].period_max,  "Tmin", tmin
    return tmin, wcrt


def ff_get_se_wcrt_by_period(tcconfig, se_task_indx, core_indx, se_alloc, se_period):
    """ Returns the WCRT of the SE tasks"""

    rt_intf = get_all_rt_interference_core_m(rt_taskset=tcconfig.rt_taskset,
                                             core_indx=core_indx,
                                             core_assignment=tcconfig.rt_core_assignment,
                                             se_period=se_period)

    se_intf = get_se_interference_core_m(se_taskset=tcconfig.se_taskset,
                                         core_indx=core_indx,
                                         se_core_assignment=se_alloc,
                                         se_task_indx=se_task_indx, se_period=se_period)

    total_intf = rt_intf + se_intf

    wcrt = tcconfig.se_taskset[se_task_indx].wcet + total_intf
    return wcrt


def get_se_periods_bestfit(tcconfig):
    """ This method calculates se task periods using partitioned best-fit approach """

    # se_task_indx = 0
    # core_indx = 0
    se_alloc = np.zeros((tcconfig.n_se_task, tcconfig.n_core))

    for se_task_indx in range(tcconfig.n_se_task):

        tmin_all_core = float('Inf')  # set a large number
        se_core_indx = None
        wcrtmin_all_core = None

        for ci in range(tcconfig.n_core):
            tmin, wcrtmin = ff_get_min_period_given_se_task_n_core_indx(tcconfig=tcconfig, se_task_indx=se_task_indx, core_indx=ci, se_alloc=se_alloc)

            if tmin is not None:
                if tmin < tmin_all_core:
                    tmin_all_core = tmin
                    se_core_indx = ci
                    wcrtmin_all_core = wcrtmin

        if tmin_all_core == float('Inf'):
            print "FF: unable to find core assignment for SE task", se_task_indx
            return False

        # wcrt = ff_get_se_wcrt_by_period(tcconfig=tcconfig,
        #                                 se_task_indx=se_task_indx,
        #                                 core_indx=se_core_indx, se_alloc=se_alloc, se_period=tmin_all_core)

        se_alloc[se_task_indx][se_core_indx] = 1  # allocate SE task
        tcconfig.se_taskset[se_task_indx].period = tmin_all_core  # update period
        tcconfig.se_taskset[se_task_indx].wcrt = wcrtmin_all_core  # update wcrt

    if PARAMS.SHOW_DEBUG_MSG:
        print "FF -> SE Alloc:", se_alloc
    # save assignment
    tcconfig.ff_se_core_assignment = copy.deepcopy(se_alloc)

    return True


def get_se_sched_bestfit_tmax(tcconfig):
    """ This method calculates se task periods using partitioned best-fit approach """

    # se_task_indx = 0
    # core_indx = 0
    se_alloc = np.zeros((tcconfig.n_se_task, tcconfig.n_core))

    for se_task_indx in range(tcconfig.n_se_task):

        # tmin_all_core = float('Inf')  # set a large number
        se_core_indx = None
        # wcrtmin_all_core = None

        intf_min_all_core = float('Inf')  # set a large number

        for ci in range(tcconfig.n_core):
            intf = ff_tmax_get_total_intf_by_core_m_n_se_indx(tcconfig=tcconfig, se_task_indx=se_task_indx, core_indx=ci, se_alloc=se_alloc)

            if intf is not None:
                if intf < intf_min_all_core:
                    intf_min_all_core = intf
                    se_core_indx = ci

        if intf_min_all_core == float('Inf'):
            print "FF_TMAX: unable to find core assignment for SE task", se_task_indx
            return False

        # check wcrt < tmax
        if tcconfig.se_taskset[se_task_indx].wcet + intf_min_all_core > tcconfig.se_taskset[se_task_indx].period_max:
            print "FF_TMAX: Unschedulable for SE task", se_task_indx
            return False

        se_alloc[se_task_indx][se_core_indx] = 1  # allocate SE task

    if PARAMS.SHOW_DEBUG_MSG:
        print "FF_TMAX -> SE Alloc:", se_alloc
    # save assignment
    tcconfig.ff_se_core_assignment = copy.deepcopy(se_alloc)

    return True


def get_z_combinations_all_global(n_rt_task, se_task_indx, n_core):
    hpset = list(range(n_rt_task+se_task_indx))
    # hpseset = list(range(n_rt_task, n_rt_task+se_task_indx))
    # print hpset
    # print hpseset

    all_ci_list = []  # list of all carry-in index
    # iterate m-1 time (where m is the number of cores)
    for c in range(0, n_core):
        cmblist = list(itertools.combinations(hpset, c))
        # print "cmpblist", cmblist
        all_ci_list.append(cmblist)

    all_ci_list = [item for sublist in all_ci_list for item in sublist]  # flatten the list
    # print "allci:", all_ci_list

    z_combination_list = []

    for ci_list in all_ci_list:
        # print "hpset:", hpset, "cilist:", list(ci_list)
        nc_list = list(set(hpset) - set(list(ci_list)))
        zcomb = CINCPartition(ci_idx_list=list(ci_list), nc_idx_list=nc_list)
        # print "CI:", zcomb.ci_idx_list, "NC:", zcomb.nc_idx_list
        z_combination_list.append(zcomb)

    return z_combination_list


def do_get_rt_wcrt_by_indx_all_global(tcconfig, rt_task_indx):

    z_combination_list = get_rt_z_combinations_all_global(rt_task_indx=rt_task_indx, n_core=tcconfig.n_core)

    max_wcrt = -1  # a negative number
    # print "RT Task indx:", RT_task_indx
    for zcl in z_combination_list:

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                wcrt = get_rt_wcrt_given_nc_ci_all_global(tcconfig=tcconfig,
                                            nc_intf_list=zcl.nc_idx_list,
                                            ci_intf_list=zcl.ci_idx_list,
                                            rt_task_indx=rt_task_indx)
            except Warning as e:
                print('Overflow in WCRT calculation:', e)
                continue

        if wcrt > 0 and wcrt > max_wcrt:
            # print "RT indx", rt_task_indx, "wcrt:", wcrt, "nc intf list", zcl.nc_idx_list, "ci intf list", zcl.ci_idx_list
            max_wcrt = wcrt

    return max_wcrt


def reset_rt_taskset(tcconfig):
    """ Delete RT core assignment and  set WCRT to none """
    tcconfig.rt_core_assignment = None

    for rt_tc in tcconfig.rt_taskset:
        rt_tc.wcrt = None


def check_rt_sched_n_set_wcrt_all_global(tcconfig):

    for rt_task_indx in range(tcconfig.n_rt_task):
        wcrt = do_get_rt_wcrt_by_indx_all_global(tcconfig=tcconfig, rt_task_indx=rt_task_indx)

        if wcrt <= tcconfig.rt_taskset[rt_task_indx].deadline:
            tcconfig.rt_taskset[rt_task_indx].wcrt = wcrt
        else:
            return False

    return True


def get_rt_z_combinations_all_global(rt_task_indx, n_core):

    # return z combinations for RT tasks

    hpset = list(range(rt_task_indx))

    #
    # print hpset
    # print hpseset

    all_ci_list = []  # list of all carry-in index
    # iterate m-1 time (where m is the number of cores)
    for c in range(0, n_core):
        cmblist = list(itertools.combinations(hpset, c))
        # print "cmpblist", cmblist
        all_ci_list.append(cmblist)

    all_ci_list = [item for sublist in all_ci_list for item in sublist]  # flatten the list
    # print "allci:", all_ci_list

    z_combination_list = []

    for ci_list in all_ci_list:
        # print "hpset:", hpset, "cilist:", list(ci_list)
        nc_list = list(set(hpset) - set(list(ci_list)))
        zcomb = CINCPartition(ci_idx_list=list(ci_list), nc_idx_list=nc_list)
        # print "CI:", zcomb.ci_idx_list, "NC:", zcomb.nc_idx_list
        z_combination_list.append(zcomb)

    return z_combination_list


def do_get_se_sched_all_global(tcconfig):

    for se_task_indx in range(tcconfig.n_se_task):

        is_sched = check_se_schedulability_all_global(tcconfig=tcconfig, se_task_indx=se_task_indx)

        if not is_sched:
            print "--> ALL_GLOBAL :: SE task", se_task_indx, "Unschedulable with Tmax:", \
                tcconfig.se_taskset[se_task_indx].period_max, "Return False <--"
            return False

    return True


def prepare_rt_taskset_all_global(tcconfig):
    """ Set response time of RT Tasks (when RT tasks can migrate).
        Return False if failed """

    reset_rt_taskset(tcconfig)

    is_rt_sched = check_rt_sched_n_set_wcrt_all_global(tcconfig)

    if is_rt_sched:
        # print ("RT Taskset is schedulable with ALL GLOBAL")
        return True
    else:
        print ("RT Taskset is not schedulable if migration allowed. Continue...")
        return False


def get_se_sched_all_global(tcconfig):
    is_rt_global_sched = prepare_rt_taskset_all_global(tcconfig)

    if is_rt_global_sched:
        # now check if the taskset is schedulable for SE tasks

        is_se_sched_allglobal = do_get_se_sched_all_global(tcconfig)
        return is_se_sched_allglobal

    # RT taskset with global is not schedulable. return False
    return False
