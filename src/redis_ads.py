# -*- coding: utf-8 -*-
# @Time    : 16/11/21 下午4:34
# @Author  : liulei
# @Brief   : 
# @File    : redis.py
# @Software: PyCharm Community Edition

import time
from redis import Redis
redis = Redis(host='localhost', port=6379, db=2)
now = time.strftime("%Y/%m/%d %H:%M:%S")
redis.lpush('test_queue', now)

res = redis.rpop('test_queue')
print str(res)

