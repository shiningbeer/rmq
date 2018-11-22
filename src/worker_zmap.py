#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
import json
import os
from time import sleep
import sys
import ConfigParser
config=ConfigParser.ConfigParser()

try:
    config.read('config.ini')
    host=config.get('rmq','host')
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
            send=Sender(host,result_channel)
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
    msg={'result':111}
    send_result(name,id,msg)


    # result=[]
    # for line in open('./'+id, 'r'):
    #     line = line.strip()
    #     result.append(line)
    # tr={'_id':task["_id"],'result':result}
    # trstr=json.dumps(tr)
    # send.send_msg(trstr)

receive=Receiver(host,receive_channel,deal_with_msg)
receive.start_listen()