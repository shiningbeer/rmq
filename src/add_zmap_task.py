from util.dao import Dao
from util.functions import is_cidr,is_ipv4
import sys

# see anything wrong?
try:
    db_name='zmapTask'
    dao=Dao(db_name)
except Exception,e:
    print u'cannot connect database!',repr(e)
    sys.exit(0)
try:
    index=sys.argv.index('-n')
    name=sys.argv[index+1]
    index=sys.argv.index('-p')
    port=int(sys.argv[index+1])
    index=sys.argv.index('-t')
    target=sys.argv[index+1]
except Exception,e:
    print u'sys args wrong!',repr(e)
    sys.exit(0)
if dao.collection_exits(name):
    print u'task name exists, please change to another name!',repr(e)
    sys.exit(0)
try:
    f=open(target,'r')
except Exception,e:
    print u'cannot open the target file!',repr(e)
    sys.exit(0)
line_number=0
for line in f:
    line_number+=1
    if not is_cidr(line):
        print (u'tartget file contains none-cidr format at line : %s' % line_number)
        sys.exit(0)
# everything is ok
f.seek(0)
line_number=0
for line in f:
    line_number+=1
    doc={'ip':line.strip(),'port':port}
    x=dao.insert_one(name,doc)
new_task={'name':name,'port':port,'complete':False,'pause':False,'allSent':False,'count':line_number,'progress':0}
dao.insert_one('taskInfo',new_task)
print u'add task successful!'
f.close()
