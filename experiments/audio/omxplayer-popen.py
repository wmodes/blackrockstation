
import subprocess
import os
import signal
import threading
from time import sleep


player = './omxplaylist.py'
opt = ["--loop", "--random", "--autoplay", "--debug"]
playlist = "data"
cmd = [player] + opt + [playlist]

def runomx():
    #subprocess.Popen([player, playlist])
    process = subprocess.Popen(cmd, preexec_fn=os.setsid)
    return process

def killomx(process):
    # subprocess.Popen(["killall", "omxplayer.bin"])
    # Send the signal to all the process groups
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

# thread_obj = threading.Thread(target=runomx)
# thread_obj.start()

print("Starting omxplaylist.py as subprocess.Popen")
process = runomx()
print("Process started, control returns to calling program")
sleep(10)
print("Preparing to kill omxplaylist.py subprocess")
sleep(10)
print("Killing omxplaylist.py subprocess")
killomx(process)
print("Process killed")
