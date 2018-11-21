#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
import json
import ConfigParser
config=ConfigParser.ConfigParser()
config.read('config.ini')
host=config.get('rmq','host')
channel=config.get('rmq','plugin_task_channel')
send=Sender(host,channel)
task={'_id':12345,'type':'plugin','ip':'173.181.212.179','port':502,'plugin':'modbus'}
print task
for i in range(2):
    task['_id']=i
    msg=json.dumps(task)
    logger.info(" Sent %r" % msg)
    send.send_msg(msg)
send.close()