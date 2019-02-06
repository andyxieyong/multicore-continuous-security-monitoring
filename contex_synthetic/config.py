# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"


class MetaConst(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError


class Const(object):
    __metaclass__ = MetaConst

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError


class PARAMS(Const):

    """ This class stores all the configuration parameters """

    # Parameters mostly follow the following paper:
    # Global and Partitioned Multiprocessor Fixed Priority Scheduling with Deferred Pre-emption

    # CORE_LIST = [2, 4, 8]
    CORE_LIST = [4]
    N_TASKSET_EACH_CONF = 250  # number of taskset in each configuration

    SE_UTIL_PERCENTAGE = 0.3  # percentage of utilization for security tasks (at least X% of RT Tasks)

    UTIL_RANGE_MIN = 0.025  # use 0.025m to 0.975m where m is the number of cores in CORE_LIST
    # UTIL_RANGE_MAX = 1  # actually 0.975 (as in paper) since np.arange doesn't count endpoint

    UTIL_RANGE_MAX = 1.0 / (1.0 - SE_UTIL_PERCENTAGE)  # consider max util as for RT tasks max util 1
    # UTIL_RANGE_STEP = 0.025
    UTIL_RANGE_STEP = 0.1  # increase step size to reduce number of points in experiments

    N_RT_TASK_MIN = 3  # n * number of cores
    N_RT_TASK_MAX = 10

    N_SE_TASK_MIN = 2  # n * number of cores
    N_SE_TASK_MAX = 5

    RT_PERIOD_MIN = 10
    RT_PERIOD_MAX = 1000

    # Max period bound for SE Tasks
    SE_PERIOD_MAX_LO = 1500
    SE_PERIOD_MAX_HI = 3000

    N_BASE_UTIL_GRP = 10  # number of base utilization group (as Man-ki)

    # RT task allocation strategy
    RT_ALLOC_BF = 'RT_BF'
    RT_ALLOC_FF = 'RT_FF'

    RT_ALLOC_STRATEGY = RT_ALLOC_FF

    GENERATE_NEW_TC = False  # indicate whether we will generate new taskset or load from file

    FIXED_POINT_MAX_BOUND = 10000  # while loop bound for fixed point search

    EXP_TIMEOUT = 300  # in seconds (total per taskset)


    # TASKET_FILENAME = 'all_taskset_4core_grp_log_100.pickle.gzip'
    TASKET_FILENAME = 'all_taskset_4core_grp_log_250.pickle.gzip'
    # TASKET_FILENAME = 'all_taskset_2core_grp_log_100.pickle.gzip'
    # TASKET_FILENAME = 'all_taskset_2core_grp_log_250.pickle.gzip'
    # TASKET_FILENAME = 'all_taskset_5.pickle.gzip'
    #EXP_RES_FILENAME_SCHED = 'sched_exp_result_250.pickle.gzip'
    # EXP_RES_FILENAME_SCHED = 'sched_exp_result_4core_log_grp_100.pickle.gzip'
    # EXP_RES_FILENAME_SCHED = 'sched_exp_result_2core_log_grp_100.pickle.gzip'

    # EXP_RES_FILENAME_SCHED_ALLGLOBAL_FFTMAX = 'sched_exp_result_agff_2core_log_grp_250.pickle.gzip'
    EXP_RES_FILENAME_SCHED_ALLGLOBAL_FFTMAX = 'sched_exp_result_agff_4core_log_grp_250.pickle.gzip'

    SHOW_DEBUG_MSG = False
