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

# connect to server until successful
while True:
    try:
        send=Sender(host,result_channel)
    except Exception,e:
        print u'cannot connect rmq server!',repr(e)
        sleep(3)
        continue
    break
def send_result(result):
    while True:
        try:
            send.send_msg(result)
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
        tr={'name':None,'_id':None,'msg':msg}
        trstr=json.dumps(tr)
        send_result(trstr)
        return
    logger.info("Received %r" % id)
    try:
        print os.system('dir')
    except Exception,e:
        logger.error(repr(e))
        msg={'error':repr(e)}
        tr={'name':name,'_id':id,'msg':msg}
        trstr=json.dumps(tr)
        send_result(trstr)
        return
    print 'lalalalllllllllllll'
    msg={'result':111}
    tr={'name':name,'_id':id,'msg':msg}
    trstr=json.dumps(tr)
    send_result(trstr)


    # result=[]
    # for line in open('./'+id, 'r'):
    #     line = line.strip()
    #     result.append(line)
    # tr={'_id':task["_id"],'result':result}
    # trstr=json.dumps(tr)
    # send.send_msg(trstr)

receive=Receiver(host,receive_channel,deal_with_msg)
receive.start_listen()