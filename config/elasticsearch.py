#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav l@pker.in
@version: 2017/7/13 13:59
"""
DATA_ES_HOST = 'http://192.168.50.241:9200/'

ES_HOST = 'http://192.168.50.241:9200/'

ES_IP = '192.168.50.241'

ES_PORT = 9200

VOIP_TYPE_NAME = 'b12_call'

INDEX_BODY = '''
{
  "index.number_of_replicas" : "0",
  "index.number_of_shards" : "4",
  "index.refresh_interval" : "1s"
}
'''

ES_VOIP_TYPE_MAPPING = '''
{
        "%s": {
            "include_in_all": false,
            "properties": {
                "b12_ip": {
                    "type": "keyword"
                },
                "call_id": {
                    "type": "keyword"
                }
            }
        }
}
'''