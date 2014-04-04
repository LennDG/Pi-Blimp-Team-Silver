import time
from subprocess import call

img_loc = "/run/shm/image.jpg"

call(["/home/pi/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/start_camd.sh " + img_loc], shell=True)

for i in range(0,10):
    call(["/home/pi/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/do_caputure.sh"], shell=True)
    time.sleep(0.5)
call(["/home/pi/rasperry-pi-userland/host_applications/linux/apps/raspicam/raspifastcamd_scripts/stop_camd.sh"], shell=True)
