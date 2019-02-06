# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import copy

class RT_Task:
    def __init__(self, wcet, period, util, deadline, tid):
        self.wcet = wcet
        self.period = period
        self.util = util
        self.deadline = deadline
        self.wcrt = None  # will be updated later
        self.tid = tid
        self.name = "RT_Task" + str(tid)


class SE_Task:
    def __init__(self, wcet, period, period_max, util, deadline, tid):
        self.wcet = wcet
        self.period = period  # actual period (obtained later by our method)
        self.period_max = period_max
        self.util = util
        self.deadline = deadline
        self.wcrt = period  # will be updated later with actual response time
        self.tid = tid
        self.name = "SE_Task" + str(tid)


class TaskSetConfig:
    def __init__(self, n_core, total_util, rt_util, se_util, n_rt_task, n_se_task, rt_taskset, se_taskset):
        self.n_core = n_core
        self.total_util = total_util
        self.rt_util = rt_util
        self.se_util = se_util
        self.n_rt_task = n_rt_task
        self.n_se_task = n_se_task
        self.rt_taskset = copy.deepcopy(rt_taskset)
        self.se_taskset = copy.deepcopy(se_taskset)
        self.rt_core_assignment = None  # will be updated later
        self.ff_se_core_assignment = None  # will be updated later
