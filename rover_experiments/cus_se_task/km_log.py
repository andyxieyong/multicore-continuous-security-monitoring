import os
import re
import subprocess
from collections import Counter

# reads sensor values and log to /roverlog/sensorlog.txt

def compare(s, t):
    return Counter(s) == Counter(t)

def get_violations(current, prof):

    is_same = compare(current, prof)

    if is_same:
        print "Total violations found:  0"
    else:
        common_entry = set(current) - (set(current) - set(prof))
        violatons = len(current) - len(common_entry)
        print  "Total violations found: ", violatons

if __name__ == '__main__':

    km_profile = [  'enable_arm_cc',
                    'nfnetlink_queue',
                    'nfnetlink_log',
                    'nfnetlink',
                    'cmac',
                    'bnep',
                    'hci_uart',
                    'btbcm',
                    'bluetooth',
                    'brcmfmac',
                    'brcmutil',
                    'snd_bcm2835',
                    'snd_pcm',
                    'cfg80211',
                    'snd_timer',
                    'rfkill',
                    'snd',
                    'bcm2835_gpiomem',
                    'uio_pdrv_genirq',
                    'uio',
                    'fixed',
                    'ip_tables',
                    'x_tables',
                    'ipv6']

    command = "lsmod"
    # print command

    current_mod_list = []

    proc = subprocess.Popen([command],stdout=subprocess.PIPE)
    line = proc.stdout.readline()  # skip first line
    while True:
        line = proc.stdout.readline()
        if line != '':
            #the real code does filtering here
            modname = line.rstrip().split()
            modname = modname[0]  # first entry is the module name
            # print "test:", modname
            current_mod_list.append(modname)

        else:
            break


    get_violations(current=current_mod_list, prof=km_profile)

    # print is_same
    # print km_profile
