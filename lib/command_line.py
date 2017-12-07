#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: xiaoL-pkav l@pker.in
@version: 2017/12/6
"""
import argparse


def parse_args():
    args_parse = argparse.ArgumentParser(description="L's Rural Elasticsearch Tools")
    args_parse.add_argument('http', help='ElasticSearch Http Server Address! E.g Http://192.168.1.250:9200')
    args_parse.add_argument('-i', '--index', default='*', help='ElasticSearch Index! E.g shop_20171101 or shop _2017*')
    args_parse.add_argument('-t', '--type', default='', help='ElasticSearch Type! E.g shop')
    args_parse.add_argument('-s', '--size', default=1000, help='Data Size E.g 2000', type=int)
    args_parse.add_argument('-f', '--skip', default=0, help='Data From E.g 4000', type=int)
    args_parse.add_argument('-l', '--limit', default=10000000000, help='Data Limit E.g 4000', type=int)
    args_parse.add_argument('-o', '--out', default='json', choices=['json', 'csv'], help='File Type E.g json | csv')
    args = args_parse.parse_args()
    return args

if __name__ == '__main__':
    parse_args()
