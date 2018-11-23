#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
import json
import os
from threading import Thread
from time import sleep
import sys
import ConfigParser
config=ConfigParser.ConfigParser()
try:
    run_count=int(sys.argv[1])
except Exception,e:
    print u'sys args wrong!',repr(e)
    sys.exit(0)
try:
    config.read('config.ini')
    host=config.get('rmq','host')
    user=config.get('rmq','user')
    password=config.get('rmq','password')
    receive_channel=config.get('rmq','zmap_task_channel')
    result_channel=config.get('rmq','zmap_result_channel')
except Exception,e:
    print u'reading config.ini error!',repr(e)
    sys.exit(0)

def send_result(name,id,msg):
    tr={'name':name,'_id':id,'msg':msg}
    trstr=json.dumps(tr)
    while True:
        try:
            send=Sender(host,user,password,result_channel)
            send.send_msg(trstr)
            send.close()
        except Exception,e:
            print u'cannot connect rmq server!',repr(e)
            sleep(3)
            continue
        break
def deal_with_msg(body):
    sleep(3)
    try:
        task=json.loads(body)    
        id=task['_id']
        ip=task['ip']
        port=str(task['port'])
        name=task['name']
    except Exception, e:
        logger.error(repr(e))
        msg={'error':repr(e),'originalMsg':body}
        send_result(None,None,msg)
        return
    print ("Received %r" % id)
    try:
        x=os.system('zmap -p '+port+' -B 5M '+ip+' -o ./'+id)
    except Exception,e:
        logger.error(repr(e))

        msg={'error':repr(e)}
        send_result(name,id,msg)
        return
    if x!=0:
        msg={'error':'run zmap failed!'}
        send_result(name,id,msg)
        return

    result=[]
    for line in open('./'+id, 'r'):
        line = line.strip()
        result.append(line)
    msg={'result':result}
    send_result(name,id,msg)

for i in range (run_count):
    receive=Receiver(host,user,password,receive_channel,deal_with_msg)
    t=Thread(target=receive.start_listen).start()