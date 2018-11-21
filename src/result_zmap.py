#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.receiver import Receiver
from util.dao import Dao
import json
import os
from bson import ObjectId
from time import sleep
import sys
import ConfigParser
config=ConfigParser.ConfigParser()
#read config
try:
    config.read('config.ini')
    host=config.get('rmq','host')
    channel=config.get('rmq','zmap_result_channel')
    zmap_task_db=config.get('mongo','zmap_task_db_name')
except Exception,e:
    print u'reading config.ini error!',repr(e)
    sys.exit(0)
#connect db
try:
    dao=Dao(zmap_task_db)
except Exception,e:
    print u'cannot connect database!',repr(e)
    sys.exit(0)


def deal_with_msg(body):
    try:
        task=json.loads(body)    
        id=task['_id']
        name=task['name']
        msg=task['msg']
    except Exception, e:
        logger.error('%s, original message: %s' %(repr(e),body))
        return
    if id is None or name is None:
        logger.error('failed messge, original message: %s' % body)
        return
    try:
        oid=ObjectId(id)
    except Exception,e:
        logger.error('%s, original message: %s' %(repr(e),body))
        return
    dao.update_one(name,{'_id':oid},msg)
try:
    receive=Receiver(host,channel,deal_with_msg)
    receive.start_listen()
except Exception,e:
    print u'cannot connect rmq server!',repr(e)
    sys.exit(0)
