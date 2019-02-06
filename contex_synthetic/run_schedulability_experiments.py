# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"


import helper_functions as hf
import taskset_generator as tgen
import experiment_handler as eh
from config import *


def run_exp_without_base_util_gen():
    if PARAMS.GENERATE_NEW_TC:
        # generate taskset and write to file as pickle object
        print "Generating Taskset and Saving to Pickle file..."
        all_taskset = tgen.generate_all_tasksets()
        hf.write_object_to_file(all_taskset, PARAMS.TASKET_FILENAME)
    else:
        print "Loading Taskset from Pickle file..."
        all_taskset = hf.load_object_from_file(PARAMS.TASKET_FILENAME)

    eh.run_sched_exp(all_taskset)


if __name__ == "__main__":

    if PARAMS.GENERATE_NEW_TC:
        # generate taskset and write to file as pickle object
        print "Generating Taskset and Saving to Pickle file..."
        all_taskset = tgen.generate_all_tasksets_base_util()
        hf.write_object_to_file(all_taskset, PARAMS.TASKET_FILENAME)
    else:
        print "Loading Taskset from Pickle file..."
        all_taskset = hf.load_object_from_file(PARAMS.TASKET_FILENAME)

    eh.run_sched_exp_with_base_util_tc(all_taskset)

    print "Script finished"
