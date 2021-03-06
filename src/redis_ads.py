# -*- coding: utf-8 -*-
# @Time    : 16/11/21 下午4:34
# @Author  : liulei
# @Brief   : 
# @File    : redis.py
# @Software: PyCharm Community Edition

import multiprocessing as mp
from redis import Redis
redis_inst = Redis(host='localhost', port=6379)
nid_queue = 'nid_queue'
def produce_nid(nid):
    global redis_inst
    redis_inst.lpush(nid_queue, nid)
    print 'produce nid: ' + nid

def consume_nid():
    global redis_inst
    import requests
    while True:
        nid = redis_inst.brpop(nid_queue)
        print '------------------------------------------consume id :' + nid[1]
        #url = 'http://120.55.88.11:9000/ml/RemoveAdsOnnidCore'
        url = 'http://120.55.88.11:9000/ml/test2'
        data = {}
        data['nid'] = nid[1]
        #response = requests.post(url, data=data)
        response = requests.get(url)
        print response.content

def consume_process():
    proc = mp.Process(target=consume_nid)
    proc.start()


