from util.dao import Dao
import sys
db_name='scanTask'
dao=Dao(db_name)
try:
    index=sys.argv.index('-n')
    name=sys.argv[index+1]
    index=sys.argv.index('-p')
    port=str(sys.argv[index+1])
    index=sys.argv.index('-t')
    target=sys.argv[index+1]
except Exception,e:
    print u'sys args wrong!'
    sys.exit(0)
try:
    f=open(target,'r')
except Exception,e:
    print u'cannot open the target file!'

for line in f:
    print line
f.close()
