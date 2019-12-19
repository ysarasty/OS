# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:41:47 2019

@author: DL5399
"""
from collections import namedtuple
from subprocess import check_output


disk_ntuple = namedtuple('partition',  'device mountpoint fstype')


def disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = check_output(['df -h |/usr/gnu/bin/awk \'{print $6 " "$5}\\'], -p)
    """f = open("/proc/filesystems", "r")
   """
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        ntuple = disk_ntuple(device, mountpoint, fstype)
        retlist.append(ntuple)
    return retlist


if __name__ == '__main__':
    for part in disk_partitions():
        print(part)
