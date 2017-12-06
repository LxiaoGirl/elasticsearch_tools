#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav l@pker.in
@version: 2017/11/20
"""

import sys
reload(sys)
# chinese
sys.setdefaultencoding('gb2312')
# other
# sys.setdefaultencoding('utf-8')
from lib.command_line import parse_args
from common.logger import Logger
from elasticsearch import Elasticsearch
import json
import os
import csv
import warnings
warnings.filterwarnings("ignore")

DATA_ES_HOST = 'http://192.168.50.253:9200/'


# 从es导出数据 存储在中间层
def export_data_from_elasticsearch(http, index='*',json_body='', size_data=100, from_data=0, limit=10000000):
    try:
        body = json.loads(json_body)
    except Exception as error:
        body = {}
    if limit < size_data:
        size_data = limit
    Logger.info(u'查询body为 %s' % json.dumps(body))
    if not body.has_key('size'):
        body['size'] = size_data
    if not body.has_key('from'):
        body['from'] = from_data
    else:
        body['from'] = 0
    data_number = 0
    elastic_search_connect = Elasticsearch(DATA_ES_HOST, retry_on_timeout=True, max_retries=3, timeout=3600000)
    while True:
        response = elastic_search_connect.search(index='voip_20171205',body=body)
        if len(response['hits']['hits']) > 0:
            data = response['hits']['hits']
            for _source in data:
                yield _source['_source']
                data_number += 1
                if data_number == limit:
                    break
            else:
                body['from'] += size_data
                continue
            break
        else:
            break
    yield None


# 控制导出流程
def start_export_process(args):
    export_filename = 'source_data'
    line_number = 0
    csv_writer = None
    with open(export_filename, 'wb') as json_file:
        if args.out == 'csv':
            csv_writer = csv.writer(json_file)
        for source_data in export_data_from_elasticsearch(args.http, args.index, args.body, args.size, args.skip, args.limit):
            if source_data:
                line_number += 1
                if args.out == 'json':
                    json_file.write(json.dumps(source_data)+'\n')
                elif args.out == 'csv':
                    csv_writer.writerow(tuple(source_data.values()))
        Logger.info(u"导出数据量%d" % (line_number))
    if args.out == 'csv':
        os.rename(export_filename, "%s.csv" % export_filename)
    elif args.out == 'json':
        os.rename(export_filename, "%s.json" % export_filename)


if __name__ == '__main__':
    command_line = parse_args()
    start_export_process(command_line)
