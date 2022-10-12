#!/usr/bin/env python

import sys, os, signal
from writer import Writer

from libinput import LibInput


if len(sys.argv) <= 2:
    print(f"[USAGE] %s </path/to/keyboard/device> [</path/to/log/file>]", sys.argv[0]);
    sys.exit(1)

log_path = sys.argv[2]
if log_path == "":
    log_path = "./log.log"
f = open(log_path, "a+", buffering = 1)

def end(signum, frame):
    f.close()
    sys.exit(0)

signal.signal(signal.SIGINT, end)

dev_path = sys.argv[1]
li = LibInput()
device = li.path_add_device(dev_path)
time_delta = 60

w = Writer(li, f)
w.run(time_delta)

f.close()
