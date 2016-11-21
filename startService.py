# -*- coding: utf-8 -*-
# @Time    : 16/8/2 下午5:27
# @Author  : liulei
# @Brief   : 
# @File    : startService.py
# @Software: PyCharm Community Edition
import json
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver
import tornado.netutil
import tornado.gen
import sys
from src import AdsExtract
from src import redis_ads

class NewsAdsExtract(tornado.web.RequestHandler):
    def post(self):
        ads_raw_data_file = './result/ads_raw_data.txt'
        data = ''
        with open(ads_raw_data_file, 'r') as f:
            data = f.read()
        d = json.loads(data.encode('utf-8'))
        AdsExtract.extract_ads(d)

class GetModifiedWechatNames(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(list(AdsExtract.modify_dict)))

class GetCheckedNames(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps(AdsExtract.get_checked_name()))

class GetAdsOfOneWechat(tornado.web.RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        self.write(json.dumps(AdsExtract.get_ads_of_one_wechat(name)))

class ModifyNewsAdsResults(tornado.web.RequestHandler):
    def post(self):
        modify_type = self.get_body_argument('modify_type').encode('utf-8')
        modify_data = self.get_body_argument('modify_data').encode('utf-8')
        AdsExtract.modify_ads_results(modify_type, modify_data)

class SaveAdsModify(tornado.web.RequestHandler):
    def get(self):
        AdsExtract.save_ads_modify()
        #清空保存了修改微信号的set
        AdsExtract.modify_dict.clear()

class NewsAdsExtractOnnid(tornado.web.RequestHandler):
    def post(self):
        pname = self.get_body_argument('pname')
        content_list = json.loads(self.get_body_argument('contents'))
        response = AdsExtract.get_ads_paras(pname, content_list)
        self.write(json.dumps(response))

class NewsAdsAddNid(tornado.web.RequestHandler):
    def post(self):
        nid = self.get_body_argument('nid')
        redis_ads.produce_nid(nid)

class test(tornado.web.RequestHandler):
    url = 'http://120.55.88.11:9000/ml/test2'
    import requests
    response = requests.get(url)
    print response.content

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ml/NewsAdsExtract", NewsAdsExtract),
            (r"/ml/NewsAdsExtractOnnid", NewsAdsExtractOnnid),
            (r"/ml/GetAdsOfOneWechat", GetAdsOfOneWechat),
            (r"/ml/GetCheckedNames", GetCheckedNames),
            (r"/ml/ModifyNewsAdsResults", ModifyNewsAdsResults),
            (r"/ml/SaveAdsModify", SaveAdsModify),
            (r"/ml/GetModifiedWechatNames", GetModifiedWechatNames),
            (r"/ml/NewsAdsAddNid", NewsAdsAddNid),
            (r"/ml/test", test),
        ]
        settings = {}
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    port = sys.argv[1]
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    #检测队列
    redis_ads.consume_process()
    tornado.ioloop.IOLoop.instance().start()

