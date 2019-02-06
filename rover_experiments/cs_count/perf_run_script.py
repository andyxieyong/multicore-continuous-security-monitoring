
import os
import re
import time

def get_cs_data(infilename):
    with open(infilename, "r") as text_file:
        lines = text_file.readlines()
        lines = lines[5]

    cs = re.sub("\D", "", lines)

    return cs


def write_cs_to_file(cs, outfilename):
    with open(outfilename, 'a') as out_file:
        out_file.write(cs)
        out_file.write('\n')


def run_perf_and_wrtite_trace(timeout, scheme, trace_file_name, binary_name):


    # some cleanup
    os.system("sudo rm ../roverlog/*.jpg")
    os.system("sudo rm ../roverlog/imagelog.tar")
    os.system("sudo touch ../roverlog/sensorlog.txt")
    os.system("sudo touch ../roverlog/locationlog.txt")


    command = 'sudo perf stat -e context-switches -o ' + \
                perfout_file + ' timeout ' + timeout + '  ' + binary_name + ' ' +\
                scheme


    # print "Command:", command
    os.system(command)

    # this is to stop rover
    os.system("sudo python ../rt_tasks/ab2_nav_ob_avoid.py")

    cs = get_cs_data(perfout_file)

    # print "CS", cs

    print "Writing data to file..."
    write_cs_to_file(cs, trace_file_name)

    # remove temp file
    command = 'sudo rm -r ' + perfout_file
    # print command
    os.system(command)



if __name__ == '__main__':

    timeout = '45s'
    scheme_vanilla = '2'
    scheme_ff = '0'
    scheme_prop = '1'

    perfout_file = 'perfout.txt'

    trace_file_name_vanilla = 'cstraces/cs_vanilla.txt'
    trace_file_name_prop = 'cstraces/cs_prop.txt'
    trace_file_name_ff = 'cstraces/cs_ff.txt'

    binary_name= './cs_count_main'

    num_exp = 1
    sleep_time  = 3  # seconds

    # for i in range(num_exp):
    #     print "\n==== CS TRACING VANILLA, COUNT", i+1, " ===="
    #     run_perf_and_wrtite_trace(timeout, scheme_vanilla,
    #                                 trace_file_name_vanilla, binary_name)
    #
    #     # clean caches
    #     # os.system("sync; echo 1 > /proc/sys/vm/drop_caches")
    #     time.sleep(sleep_time)
    #
    #
    # time.sleep(5)
    # for i in range(num_exp):
    #     print "\n==== CS TRACING PROPOSED, COUNT", i+1, " ===="
    #     run_perf_and_wrtite_trace(timeout, scheme_prop,
    #                                 trace_file_name_prop, binary_name)
    #     time.sleep(sleep_time+2)


    time.sleep(5)
    for i in range(num_exp):
        print "\n==== CS TRACING FF, COUNT", i+1, " ===="
        run_perf_and_wrtite_trace(timeout, scheme_ff,
                                    trace_file_name_ff, binary_name)
        time.sleep(sleep_time+2)


    print "CS count script finished!"
