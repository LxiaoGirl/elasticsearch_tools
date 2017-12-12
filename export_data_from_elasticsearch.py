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
import functools
import os
import csv
import random
import string
import re
import warnings
warnings.filterwarnings("ignore")


# 从es导出数据 存储在中间层
def export_data_from_elasticsearch(http, index='*',json_body='', size_data=100, from_data=0, limit=10000000):
    elastic_search_connect = Elasticsearch(http, retry_on_timeout=True, max_retries=3, timeout=3600000)
    try:
        body = json.loads(json_body)
    except Exception as error:
        Logger.error(u"查询请求body出错%s" % error)
        body = {}
    if limit < size_data:
        size_data = limit
    Logger.info(u'查询body为 %s' % json.dumps(body))
    total_number = elastic_search_connect.count(index=index, body=body)
    Logger.info(u"数据总量为 %d" % int(total_number['count']))
    if not body.has_key('size'):
        body['size'] = size_data
    if not body.has_key('from'):
        body['from'] = from_data
    else:
        body['from'] = 0
    data_number = 0
    while True:
        response = elastic_search_connect.search(index=index,body=body)
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


# 读取body请求包
def read_request_body():
    try:
        return open('body.data', 'r').read()
    except Exception as error:
        Logger.error(u"请求文件读取，body请求为空，错误%s。" % error)
        return ''


# 获取文件名
def get_filename(index):
    # 文件名替换 windows下不允许字符
    filename = functools.reduce(lambda r, x: r.replace(x, ''), ['|', '\\', '/', ':', '?', '*', '<', '>', '"'], index)
    if not filename:
        filename = 'data_list'
    return filename


# 修改输出文件名
def rename_to_outfile(source_filename, target_filename):
    random_string = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    try:
        if os.path.exists(target_filename):
            os.rename(target_filename, "%s.%s.bak" % (random_string, target_filename))
    except Exception as error:
        Logger.error(u"文件名修改错误 %s" % error)
        return False
    return True


# 控制导出流程
def start_export_process(args):
    args.body = read_request_body()
    export_filename = get_filename(args.index)
    line_number = 0
    csv_writer = None
    first_line = True
    with open(export_filename, 'wb') as json_file:
        if args.out == 'csv':
            csv_writer = csv.writer(json_file)
        for source_data in export_data_from_elasticsearch(args.http, args.index, args.body, args.size, args.skip, args.limit):
            if source_data:
                line_number += 1
                if args.out == 'json':
                    json_file.write(json.dumps(source_data)+'\n')
                elif args.out == 'csv':
                    if first_line:
                        first_line = False
                        csv_writer.writerow(tuple(source_data.keys()))

                    try:
                        csv_writer.writerow(tuple(source_data.values()))
                    except Exception as error:
                        Logger.error(u"CSV文件写入出错%s" % error)
                print u"当前导出数据量%s\r" % line_number,
        Logger.info(u"导出数据量%d" % (line_number))
    out_filename = 'data_list'
    if args.out == 'csv':
        out_filename = "%s.csv" % export_filename
    elif args.out == 'json':
        out_filename = "%s.json" % export_filename
    if rename_to_outfile(export_filename, out_filename):
        os.rename(export_filename, out_filename)
        Logger.info(u"文件生成成功 %s" % out_filename)


if __name__ == '__main__':
    Logger.info(u"开始数据导出")
    command_line = parse_args()
    start_export_process(command_line)

