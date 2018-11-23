from util.dao import Dao
import ConfigParser
import sys
config=ConfigParser.ConfigParser()
# read config
try:
    config.read('config.ini')
    task_info=config.get('mongo','task_info_collection_name')
    zmap_task_db=config.get('mongo','zmap_task_db_name')
    plugin_task_db=config.get('mongo','plugin_task_db_name')
except Exception,e:
    print u'reading config.ini error!',repr(e)
    sys.exit(0)
# connect database
try:
    dao_zmap=Dao(zmap_task_db)
    dao_plugin=Dao(plugin_task_db)
except Exception,e:
    print u'cannot connect database!',repr(e)
    sys.exit(0)

zmap_tasks=dao_zmap.find_many(task_info,{})
plugin_tasks=dao_plugin.find_many(task_info,{})
print u'------zmap tasks-----'
print 'name      ','port   ','progress   ','pause   '
for task in zmap_tasks:
    print task['name'],'     ',task['port'],'     ','%d/%d'%(task['progress'],task['count']),'     ',task['pause']
print u'------plugin tasks-----'

for task in plugin_tasks:
    print task
