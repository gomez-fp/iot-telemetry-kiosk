#import RPi.GPIO as GPIO
import subprocess
import os
#import board
import time
#from ppp0_on import ppp0

#GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17,GPIO.OUT)
# 
# GPIO.output(17,False)
# time.sleep(1.7)
# GPIO.output(17,True)
##print("modulo GSM ensendido")
##print(subprocess.run(["sudo", "pon", "fona"]))
##time.sleep(13)
os.system("xset -dpms")
os.system("xset s noblanck")
os.system("xset  s off")

time.sleep(2)
n = 0
try:
    while n<9:
        print(subprocess.call(['python', 'integracion_4.py']))
        n = n + 1
#     while n < 1:
#         print(subprocess.call(['python', 'appWeb.py']))
#         time.sleep(3)

except:
    print("sed daño")
    time.sleep(1)
    print(subprocess.call(['sudo', 'reboot now']))
    