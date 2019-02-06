# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import copy


class ExportSchedOutput:

    """ A Class to format schedulability output result """

    def __init__(self, core_list, ntc_each_conf, rt_sched_dict, se_sched_prop_dict, se_sched_ff_dict, ecdist_prop_dict, ecdist_ff_dict):
        self.core_list = copy.deepcopy(core_list)
        self.ntc_each_conf = copy.deepcopy(ntc_each_conf)
        self.ecdist_prop_dict = copy.deepcopy(ecdist_prop_dict)
        self.ecdist_ff_dict = copy.deepcopy(ecdist_ff_dict)
        self.se_sched_prop_dict = copy.deepcopy(se_sched_prop_dict)
        self.se_sched_ff_dict = copy.deepcopy(se_sched_ff_dict)
        self.rt_sched_dict = copy.deepcopy(rt_sched_dict)


class ExportSchedOutputAllGlobalTmax:

    """ A Class to format schedulability output result for all_global and ff_tamx scheme """

    def __init__(self, core_list, ntc_each_conf, rt_sched_dict, se_sched_allglobal_dict, se_sched_fftmax_dict):
        self.core_list = copy.deepcopy(core_list)
        self.ntc_each_conf = copy.deepcopy(ntc_each_conf)
        self.se_sched_allglobal_dict = copy.deepcopy(se_sched_allglobal_dict)
        self.se_sched_fftmax_dict = copy.deepcopy(se_sched_fftmax_dict)
        self.rt_sched_dict = copy.deepcopy(rt_sched_dict)

