import os
from time import sleep
while True:
    print '------Dispatch Info--------'
    os.system('python dispatcher_zmap.py')
    print '-'
    print '------Task Info--------'
    os.system('python collect_progress.py')
    for i in range(3):
        print '-'
    sleep(1)