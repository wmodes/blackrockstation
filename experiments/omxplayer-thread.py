
import subprocess
import threaded
from time import sleep

def runomx():
    subprocess.Popen(["/usr/bin/omxplayer", "wlac-grizzard-60-u.mp3"])

def killomx():
    subprocess.Popen(["killall", "omxplayer.bin"])

thread_obj = threading.Thread(target=runomx)
thread_obj.start()

sleep(20)
killomx()
