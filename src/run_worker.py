
import os
import sys
from time import sleep
from threading import Thread
print sys.argv[1]
def threadFunc():
    os.system('python worker_zmap.py')
for i in range(int(sys.argv[1])):
    t = Thread(target=threadFunc, args=())
    t.start()
    print i
while True:
    sleep(30)