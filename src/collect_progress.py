
from util.dao import Dao
import json
import ConfigParser
import sys
config=ConfigParser.ConfigParser()


try:
    config.read('config.ini')
    host=config.get('rmq','host')
    channel=config.get('rmq','zmap_task_channel')
    task_info=config.get('mongo','task_info_collection_name')
    zmap_task_db=config.get('mongo','zmap_task_db_name')
except Exception,e:
    print u'reading config.ini error!',repr(e)
try:
    dao=Dao(zmap_task_db)
except Exception,e:
    print u'cannot connect database!',repr(e)
    sys.exit(0)
# collect progress
uncompleted_tasks=dao.find_many(task_info,{'complete':False})
if uncompleted_tasks.count()==0:
    print 'task all complete!'
for utask in uncompleted_tasks:
    finished_count=dao.find_count(utask['name'],{'$or':[{'error':{'$exists':True}},{'result':{'$exists':True}}]})
    sent_count=dao.find_count(utask['name'],{'sent':True})
    if finished_count==utask['count']:
        #complete
        dao.update_one(task_info,{'_id':utask['_id']},{'complete':True})
    dao.update_one(task_info,{'_id':utask['_id']},{'progress':finished_count})
    print 'task--%s : sent (%d/%d)   complete (%d/%d)' % (utask['name'],sent_count,utask['count'], finished_count,utask['count'])