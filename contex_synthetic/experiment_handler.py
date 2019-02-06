# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

from __future__ import division
from collections import defaultdict
import copy
import taskset_generator as tgen
import sched_functions as schf
import helper_functions as hf
import output_classes as oc
from config import *


def calculate_period_for_se_task_by_id(taskset, se_task_indx):
    pass


def get_period_cont_ex(taskset):
    pass


def prepare_rt_taskset(tcconfig):
    """ Set the core_assignment and response time of RT Tasks.
        Return False if failed """

    core_assignment = schf.get_rt_core_assignment(rt_taskset=tcconfig.rt_taskset, n_core=tcconfig.n_core)

    if core_assignment is not None:
        # run schedulability test for safety
        is_sched = schf.check_rt_schedulability(rt_taskset=tcconfig.rt_taskset, core_assignment=core_assignment)
        if is_sched:
            # print "RT Tasks schedulable!"
            # update the wcrt variable in RT taskset
            schf.set_wcrt_all_rt_task(rt_taskset=tcconfig.rt_taskset, core_assignment=core_assignment)
            tcconfig.rt_core_assignment = copy.deepcopy(core_assignment)
            return True
        else:
            print ("RT Taskset is not schedulable. Continue...")
            return False

    else:
        print ("Unable to find core assignment for RT Tasks. Continue...")
        return False


# this is dummy function for testing a single taskset
def dummy_run_period_selection_exp():
    print "hello"

    # core = 2;
    # util = 1 + PARAMS.SE_UTIL_PERCENTAGE
    # ntc = 50;

    n_core = 4
    n_rt_task = 5
    n_se_task = 6
    # total_system_util = 1.0 * n_core / (1.0 - PARAMS.SE_UTIL_PERCENTAGE)
    total_system_util = 3.0

    tcconfig = tgen.generate_taskset(n_core, n_rt_task, n_se_task, total_system_util)
    # tcconfig = all_taskset[core][util][ntc]

    # all_taskset = hf.load_object_from_file(PARAMS.TASKET_FILENAME)
    # util_list = tgen.get_util_list_by_core(core=2)
    # print "indx", list(util_list).index(0.05)
    # tcconfig = all_taskset[2][0][196]

    prt = prepare_rt_taskset(tcconfig)

    if prt:

        # util_list = tgen.get_util_list_by_core(core=n_core)
        #
        # for total_system_util in util_list:
        #     tcconfig = tgen.generate_taskset(n_core, n_rt_task, n_se_task, total_system_util)
        #     print "total rt util", tcconfig.rt_util
        #     print "total se util", tcconfig.se_util
        #     print "total util", tcconfig.total_util

        print "=== RT TASKSET SCHEDULABLE ==="
        print "total rt util", tcconfig.rt_util
        print "total se util", tcconfig.se_util
        print "total util", tcconfig.total_util

        print tcconfig.rt_core_assignment

        for rt_tsk in tcconfig.rt_taskset:
            print "RT Task id", rt_tsk.tid, "Period", rt_tsk.period, "WCET", rt_tsk.wcet, "WCRT:", rt_tsk.wcrt

        # for se_tsk in tcconfig.se_taskset:
        #     print se_tsk.util

        tcconfig_proposed = copy.deepcopy(tcconfig)
        tcconfig_ff = copy.deepcopy(tcconfig)

        print "======"
        # proposed scheme
        is_se_sched_prop = schf.get_se_periods_proposed(tcconfig=tcconfig_proposed)

        if is_se_sched_prop:
            print "\n PROP: Taskset is schedulable. Printing periods and WCRT.."
            for se_tsk in tcconfig_proposed.se_taskset:
                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

            print "Testing with Euc dist:"

            tvec_prop = [se_tsk.period for se_tsk in tcconfig_proposed.se_taskset]
            tmaxvec_prop = [se_tsk.period_max for se_tsk in tcconfig_proposed.se_taskset]

            ecdist_prop = hf.get_normalized_euc_dist(tvec_prop, tmaxvec_prop)
            print "ECDIST_PROP:", ecdist_prop

        # now test with best-fit scheme

        is_se_sched_ff = schf.get_se_periods_bestfit(tcconfig=tcconfig_ff)

        if is_se_sched_ff:
            print "\n FF: Taskset is schedulable. Printing periods and WCRT.."
            for se_tsk in tcconfig_ff.se_taskset:
                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

            print "Testing with Euc dist:"

            tvec_ff = [se_tsk.period for se_tsk in tcconfig_ff.se_taskset]
            tmaxvec_ff = [se_tsk.period_max for se_tsk in tcconfig_ff.se_taskset]
            ecdist_ff = hf.get_normalized_euc_dist(tvec_ff, tmaxvec_ff)
            print "ECDIST_FF:", ecdist_ff



    else:
        print "TODO: handle when RT tasks are not schedulable."


def run_sched_exp(all_taskset):
    """ This is the script that run period selection methods and obtain schedulability and Euclidian distance """

    ecdist_prop_dict = defaultdict(lambda: defaultdict(dict))
    ecdist_ff_dict = defaultdict(lambda: defaultdict(dict))
    se_sched_prop_dict = defaultdict(lambda: defaultdict(dict))
    se_sched_ff_dict = defaultdict(lambda: defaultdict(dict))
    rt_sched_dict = defaultdict(lambda: defaultdict(dict))

    for core in PARAMS.CORE_LIST:
        util_list = tgen.get_util_list_by_core(core)

        for uindx, util in enumerate(util_list):

            se_sched_prop_count = 0
            se_sched_ff_count = 0
            rt_sched_count = 0

            ecdist_list_prop = []
            ecdist_list_ff = []

            for ntc in range(0, PARAMS.N_TASKSET_EACH_CONF):
                print "Analyzing Core:", core, "System Utilization:", util, "NTC Task index", ntc

                tcconfig = all_taskset[core][util][ntc]
                prt = prepare_rt_taskset(tcconfig)

                if prt:

                    if PARAMS.SHOW_DEBUG_MSG:
                        print "=== RT TASKSET SCHEDULABLE ==="
                        print "Total RT util", tcconfig.rt_util, "Total SE util", tcconfig.se_util, "Total util", tcconfig.total_util
                        print "RT Core Assignement:", tcconfig.rt_core_assignment
                        for rt_tsk in tcconfig.rt_taskset:
                            print "RT Task id", rt_tsk.tid, "Period", rt_tsk.period, "WCET", rt_tsk.wcet, "WCRT:", rt_tsk.wcrt


                    rt_sched_count += 1
                    tcconfig_proposed = copy.deepcopy(tcconfig)
                    tcconfig_ff = copy.deepcopy(tcconfig)

                    # proposed scheme
                    is_se_sched_prop = schf.get_se_periods_proposed(tcconfig=tcconfig_proposed)

                    if is_se_sched_prop:
                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n PROP: Taskset is schedulable. Printing periods and WCRT.."
                            for se_tsk in tcconfig_proposed.se_taskset:
                                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

                        tvec_prop = [se_tsk.period for se_tsk in tcconfig_proposed.se_taskset]
                        tmaxvec_prop = [se_tsk.period_max for se_tsk in tcconfig_proposed.se_taskset]

                        ecdist_prop = hf.get_normalized_euc_dist(tvec_prop, tmaxvec_prop)

                        se_sched_prop_count += 1  # increase sched count
                        ecdist_list_prop.append(ecdist_prop)  # save distance


                    # now test with best-fit scheme

                    is_se_sched_ff = schf.get_se_periods_bestfit(tcconfig=tcconfig_ff)

                    if is_se_sched_ff:

                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n FF: Taskset is schedulable. Printing periods and WCRT.."
                            for se_tsk in tcconfig_ff.se_taskset:
                                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

                        tvec_ff = [se_tsk.period for se_tsk in tcconfig_ff.se_taskset]
                        tmaxvec_ff = [se_tsk.period_max for se_tsk in tcconfig_ff.se_taskset]
                        ecdist_ff = hf.get_normalized_euc_dist(tvec_ff, tmaxvec_ff)

                        se_sched_ff_count += 1  # increase sched count
                        ecdist_list_ff.append(ecdist_ff)  # save distance

                else:
                    print "RT tasks are not schedulable. Continue.."

            # save sched counts
            se_sched_prop_dict[core][uindx] = se_sched_prop_count
            se_sched_ff_dict[core][uindx] = se_sched_ff_count
            rt_sched_dict[core][uindx] = rt_sched_count

            # save distance for all util
            ecdist_prop_dict[core][uindx] = ecdist_list_prop
            ecdist_ff_dict[core][uindx] = ecdist_list_ff

    # save the dictionary as class object
    output = oc.ExportSchedOutput(core_list=PARAMS.CORE_LIST,
                                  ntc_each_conf=PARAMS.N_TASKSET_EACH_CONF,
                                  rt_sched_dict=rt_sched_dict,
                                  se_sched_prop_dict=se_sched_prop_dict,
                                  se_sched_ff_dict=se_sched_ff_dict,
                                  ecdist_prop_dict=ecdist_prop_dict,
                                  ecdist_ff_dict=ecdist_ff_dict)
    # saving results to pickle file
    print "--> Schedulability Experiment :: Saving result to file..."
    hf.write_object_to_file(output, PARAMS.EXP_RES_FILENAME_SCHED)


def run_sched_exp_with_base_util_tc(all_taskset):
    """ This is the script that run period selection methods and obtain schedulability and Euclidian distance """

    ecdist_prop_dict = defaultdict(lambda: defaultdict(dict))
    ecdist_ff_dict = defaultdict(lambda: defaultdict(dict))
    se_sched_prop_dict = defaultdict(lambda: defaultdict(dict))
    se_sched_ff_dict = defaultdict(lambda: defaultdict(dict))
    rt_sched_dict = defaultdict(lambda: defaultdict(dict))

    for core in PARAMS.CORE_LIST:

        total_grp = PARAMS.N_BASE_UTIL_GRP

        for uindx in range(total_grp):

            se_sched_prop_count = 0
            se_sched_ff_count = 0
            rt_sched_count = 0

            ecdist_list_prop = []
            ecdist_list_ff = []

            for ntc in range(0, PARAMS.N_TASKSET_EACH_CONF):
                print "Analyzing Core:", core, "Utilization Group:", uindx, "NTC Task index", ntc

                tcconfig = all_taskset[core][uindx][ntc]
                prt = prepare_rt_taskset(tcconfig)

                if prt:

                    if PARAMS.SHOW_DEBUG_MSG:
                        print "=== RT TASKSET SCHEDULABLE ==="
                        print "Total RT util", tcconfig.rt_util, "Total SE util", tcconfig.se_util, "Total util", tcconfig.total_util
                        print "RT Core Assignement:", tcconfig.rt_core_assignment
                        for rt_tsk in tcconfig.rt_taskset:
                            print "RT Task id", rt_tsk.tid, "Period", rt_tsk.period, "WCET", rt_tsk.wcet, "WCRT:", rt_tsk.wcrt


                    rt_sched_count += 1
                    tcconfig_proposed = copy.deepcopy(tcconfig)
                    tcconfig_ff = copy.deepcopy(tcconfig)

                    # proposed scheme
                    is_se_sched_prop = schf.get_se_periods_proposed(tcconfig=tcconfig_proposed)

                    if is_se_sched_prop:
                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n PROP: Taskset is schedulable. Printing periods and WCRT.."
                            for se_tsk in tcconfig_proposed.se_taskset:
                                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

                        tvec_prop = [se_tsk.period for se_tsk in tcconfig_proposed.se_taskset]
                        tmaxvec_prop = [se_tsk.period_max for se_tsk in tcconfig_proposed.se_taskset]

                        ecdist_prop = hf.get_normalized_euc_dist(tvec_prop, tmaxvec_prop)

                        se_sched_prop_count += 1  # increase sched count
                        ecdist_list_prop.append(ecdist_prop)  # save distance


                    # now test with best-fit scheme

                    is_se_sched_ff = schf.get_se_periods_bestfit(tcconfig=tcconfig_ff)

                    if is_se_sched_ff:

                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n FF: Taskset is schedulable. Printing periods and WCRT.."
                            for se_tsk in tcconfig_ff.se_taskset:
                                print "Se task:", se_tsk.tid, "wcet:", se_tsk.wcet, "wcrt:", se_tsk.wcrt, "period:", se_tsk.period, "Tmax:", se_tsk.period_max

                        tvec_ff = [se_tsk.period for se_tsk in tcconfig_ff.se_taskset]
                        tmaxvec_ff = [se_tsk.period_max for se_tsk in tcconfig_ff.se_taskset]
                        ecdist_ff = hf.get_normalized_euc_dist(tvec_ff, tmaxvec_ff)

                        se_sched_ff_count += 1  # increase sched count
                        ecdist_list_ff.append(ecdist_ff)  # save distance

                else:
                    print "RT tasks are not schedulable. Continue.."

            # save sched counts
            se_sched_prop_dict[core][uindx] = se_sched_prop_count
            se_sched_ff_dict[core][uindx] = se_sched_ff_count
            rt_sched_dict[core][uindx] = rt_sched_count

            # save distance for all util
            ecdist_prop_dict[core][uindx] = ecdist_list_prop
            ecdist_ff_dict[core][uindx] = ecdist_list_ff

    # save the dictionary as class object
    output = oc.ExportSchedOutput(core_list=PARAMS.CORE_LIST,
                                  ntc_each_conf=PARAMS.N_TASKSET_EACH_CONF,
                                  rt_sched_dict=rt_sched_dict,
                                  se_sched_prop_dict=se_sched_prop_dict,
                                  se_sched_ff_dict=se_sched_ff_dict,
                                  ecdist_prop_dict=ecdist_prop_dict,
                                  ecdist_ff_dict=ecdist_ff_dict)
    # saving results to pickle file
    print "--> Schedulability Experiment :: Saving result to file..."
    hf.write_object_to_file(output, PARAMS.EXP_RES_FILENAME_SCHED)


def do_run_sched_exp_all_global_fftmax(tcconfig):
    # n_core = 4
    # n_rt_task = 5
    # n_se_task = 10
    # # total_system_util = 1.0 * n_core / (1.0 - PARAMS.SE_UTIL_PERCENTAGE)
    # total_system_util = 3.2
    #
    # tcconfig = tgen.generate_taskset(n_core, n_rt_task, n_se_task, total_system_util)
    #
    # prt = prepare_rt_taskset(tcconfig)

    tcconfig_allglobal = copy.deepcopy(tcconfig)
    tcconfig_fftmax = copy.deepcopy(tcconfig)

    # check if the all global scheme is schedulable
    # is_se_sched_allglobal = schf.get_se_sched_all_global(tcconfig=tcconfig_allglobal)
    # print "SE_ALL_Global:", is_se_sched_allglobal
    is_se_sched_allglobal = False  # for now we will not run all global scheme

    # check if the FF_Tmax scheme is schedulable
    is_se_sched_fftmax = schf.get_se_sched_bestfit_tmax(tcconfig=tcconfig_fftmax)
    # print "SE_FF_Tmax:", is_se_sched_fftmax

    return is_se_sched_allglobal, is_se_sched_fftmax


def run_sched_exp_all_global_fftmax(all_taskset):
    """ This is the script that run schedulability experiments for All_global and Best-fit_Tmax approach """

    se_sched_allglobal_dict = defaultdict(lambda: defaultdict(dict))
    se_sched_fftmax_dict = defaultdict(lambda: defaultdict(dict))
    rt_sched_dict = defaultdict(lambda: defaultdict(dict))

    for core in PARAMS.CORE_LIST:

        total_grp = PARAMS.N_BASE_UTIL_GRP

        for uindx in range(total_grp):

            se_sched_allglobal_count = 0
            se_sched_fftmax_count = 0
            rt_sched_count = 0

            for ntc in range(0, PARAMS.N_TASKSET_EACH_CONF):
                print "Analyzing Core:", core, "Utilization Group:", uindx, "NTC Task index", ntc

                tcconfig = all_taskset[core][uindx][ntc]
                prt = prepare_rt_taskset(tcconfig)

                if prt:

                    if PARAMS.SHOW_DEBUG_MSG:
                        print "=== RT TASKSET SCHEDULABLE ==="
                        print "Total RT util", tcconfig.rt_util, "Total SE util", tcconfig.se_util, "Total util", tcconfig.total_util
                        print "RT Core Assignement:", tcconfig.rt_core_assignment
                        for rt_tsk in tcconfig.rt_taskset:
                            print "RT Task id", rt_tsk.tid, "Period", rt_tsk.period, "WCET", rt_tsk.wcet, "WCRT:", rt_tsk.wcrt

                    rt_sched_count += 1

                    # run experiments

                    is_se_sched_allglobal, is_se_sched_fftmax = do_run_sched_exp_all_global_fftmax(tcconfig)

                    if is_se_sched_allglobal:
                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n ALL_GLOBAL: Taskset is schedulable"

                        se_sched_allglobal_count += 1  # increase sched count

                    if is_se_sched_fftmax:
                        if PARAMS.SHOW_DEBUG_MSG:
                            print "\n ALL_GLOBAL: Taskset is schedulable"

                        se_sched_fftmax_count += 1  # increase sched count

                else:
                    print "RT tasks are not schedulable. Continue.."

            # save sched counts
            se_sched_allglobal_dict[core][uindx] = se_sched_allglobal_count
            se_sched_fftmax_dict[core][uindx] = se_sched_fftmax_count
            rt_sched_dict[core][uindx] = rt_sched_count

    # save the dictionary as class object
    output = oc.ExportSchedOutputAllGlobalTmax(core_list=PARAMS.CORE_LIST,
                                  ntc_each_conf=PARAMS.N_TASKSET_EACH_CONF,
                                  rt_sched_dict=rt_sched_dict,
                                  se_sched_allglobal_dict=se_sched_allglobal_dict,
                                  se_sched_fftmax_dict=se_sched_fftmax_dict)
    # saving results to pickle file
    print "--> Schedulability Experiment :: Saving result to file..."
    hf.write_object_to_file(output, PARAMS.EXP_RES_FILENAME_SCHED_ALLGLOBAL_FFTMAX)
