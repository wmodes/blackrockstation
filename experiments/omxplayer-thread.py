
import subprocess
import os
import signal
import threading
from time import sleep

player = "/home/pi/blackrockstation/omxplaylist/omxplaylist.py"
opt = ["--loop", "--random"]
playlist = "/home/pi/blackrockstation/experiments/audio/playlist/"
cmd = [player] + opt + [playlist]

process = None

def runomx():
    #subprocess.Popen([player, playlist])
    process = subprocess.Popen(cmd, preexec_fn=os.setsid)

def killomx():
    # subprocess.Popen(["killall", "omxplayer.bin"])
    # Send the signal to all the process groups
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

thread_obj = threading.Thread(target=runomx)
thread_obj.start()

sleep(20)
killomx()
