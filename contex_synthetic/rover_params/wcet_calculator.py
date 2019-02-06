# __author__ = "Monowar Hasan"
# __email__ = "mhasan11@illinois.edu"

import pandas as pd
import math


# NOTE: returns WCET values rounded and unit is ms
def get_max_wcet_by_filename(filename, wcet_pad):
    """ Returns the data form text file """
    data = pd.read_csv(filename, header=None)
    data = max(data[0].values.tolist())

    data = data * 1e-6  # change to millisecond

    data = data * wcet_pad  # add safety margin

    data = math.ceil(data)  # round to ceil

    return data


if __name__ == "__main__":

    wcet_pad = 1.5

    camera = get_max_wcet_by_filename('wcet_traces/camera.txt', wcet_pad)
    coretemp = get_max_wcet_by_filename('wcet_traces/coretemp.txt', wcet_pad)
    cus_kmlog = get_max_wcet_by_filename('wcet_traces/cus_kmlog.txt', wcet_pad)
    location = get_max_wcet_by_filename('wcet_traces/location.txt', wcet_pad)
    navigation = get_max_wcet_by_filename('wcet_traces/navigation_iter.txt', wcet_pad)
    sensor = get_max_wcet_by_filename('wcet_traces/sensor.txt', wcet_pad)
    tw_ownbin = get_max_wcet_by_filename('wcet_traces/tw_ownbin.txt', wcet_pad)
    tw_roverlogscan = get_max_wcet_by_filename('wcet_traces/tw_roverlogscan.txt', wcet_pad)
    tw_rovlog_cus_kmlog = get_max_wcet_by_filename('wcet_traces/tw_rovlog_cus_kmlog.txt', wcet_pad)

    print "Task Name\t\t WCET (ms)"
    print "-------------------------"

    print "navigation\t\t", navigation
    print "camera\t\t\t", camera
    print "sensor\t\t\t", sensor
    print "coretemp\t\t", coretemp
    print "location\t\t", location
    print "========================="
    print "tw_onwbin\t\t", tw_ownbin
    print "tw_roverlogscan\t", tw_roverlogscan
    print "cus_kmlog\t\t", cus_kmlog
    print "tw_rovlog_cus_kmlog\t\t", tw_rovlog_cus_kmlog


    print "\n\nWCET Script Finished!"