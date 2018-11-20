#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
import json
import os
from time import sleep
send=Sender('localhost','zmap_result_queue')

def deal_with_msg(body):
    try:
        task=json.loads(body)    
        id=task['_id']
    except Exception, e:
        logger.error(repr(e))
        tr={'error':repr(e)}
        trstr=json.dumps(tr)
        send.send_msg(trstr)
        return
    logger.info("Received %r" % task['_id'])
    try:
        port=task['port']
        ip=task['ip']
        os.system('zmap -p '+port+' -B 5M '+ip+' -o ./'+id)
    except Exception,e:
        logger.error(repr(e))
        tr={'_id':id,'error':repr(e)}
        trstr=json.dumps(tr)
        send.send_msg(trstr)
        return

    result=[]
    for line in open('./'+id, 'r'):
        line = line.strip()
        result.append(line)
    tr={'_id':task["_id"],'result':result}
    trstr=json.dumps(tr)
    send.send_msg(trstr)

receive=Receiver('localhost','zmap_queue',deal_with_msg)
receive.start_listen()