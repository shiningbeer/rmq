#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
import json
from time import sleep
send=Sender('localhost','result_queue')

def getScanFunc(plugin):

    try:
        exec("from plugins import " + plugin + " as scanning_plugin")
    except Exception, e:
        print str(e)
        return None
    return scanning_plugin.scan

def xxx(body):
    task=json.loads(body)
    logger.info(" Received %r" % task['_id'])
    port=task['port']
    ip=task['ip']
    plugin=task['plugin']
    scan=getScanFunc(plugin)

    result=scan(ip,port)
    tr={'_id':task["_id"],'result':result}
    trstr=json.dumps(tr)
    send.send_msg(trstr)

receive=Receiver('localhost','task_queue',xxx)
receive.start_listen()