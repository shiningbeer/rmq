#!/usr/bin/env python
from util.sender import Sender
from util.logger import logger
from util.dao import Dao
import json
import ConfigParser
import sys
config=ConfigParser.ConfigParser()



try:
    config.read('config.ini')
    host=config.get('rmq','host')
    channel=config.get('rmq','zmap_task_channel')
    max_queue_length=int(config.get('rmq','zmap_max_queue_length'))
    send_batch_count=int(config.get('rmq','zmap_send_batch_count'))
    task_info=config.get('mongo','task_info_collection_name')
    zmap_task_db=config.get('mongo','zmap_task_db_name')
except Exception,e:
    print u'reading config.ini error!',repr(e)
    sys.exit(0)
try:
    dao=Dao(zmap_task_db)
except Exception,e:
    print u'cannot connect database!',repr(e)
    sys.exit(0)

try:
    send=Sender(host,channel)
except Exception,e:
    print u'cannot connect rmq server!',repr(e)
    sys.exit(0)
msg_count=send.get_msg_count()
if msg_count>max_queue_length:
    print u'queue length: %s > %s. waiting...' % (msg_count, max_queue_length)
    sys.exit(0)
print 'queue length: %d ' % msg_count
task=dao.find_one(task_info,{'allSent':False,'pause':False})
if task is None:
    print u'no task now!'
    sys.exit(0)
col_name=task['name']
task_id=task['_id']
if not dao.collection_exits(col_name):
    logger.critical('the task %s listed in the taskInfo table is missing its collection!' % col_name)
    dao.delete_many(task_info,{'name':col_name})
    logger.critical('the task %s is deleted in tasinInfo table!' % col_name)
    sys.exit(0)
for i in range(send_batch_count):
    doc=dao.find_one(col_name,{'sent':None})
    if doc is None:
        # means the ip of task is all sent
        dao.update_many(task_info,{'_id':task_id},{'allSent':True})
        sys.exit(0)
    doc['name']=col_name
    doc_id=doc['_id']
    doc['_id']=str(doc['_id'])
    msg=json.dumps(doc)
    try:
        send.send_msg(msg)
    except Exception,e:
        print repr(e)
        continue
    dao.update_one(col_name,{'_id':doc_id},{'sent':True})
print 'task--%s : sent another %d' % (col_name,send_batch_count)
send.close()