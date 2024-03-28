import time
import subprocess, sys

timer = (float(input("Timer (minutes): "))*60)
print("Start")
time.sleep(timer)

opener = "open" if sys.platform == "darwin" else "xdg-open"
subprocess.call([opener, "timer.odt"])
