# elasticsearch_tools
工作中elasticsearch使用到的工具集合。

usage: export_data_from_elasticsearch.py [-h] [-i INDEX] [-t TYPE] [-s SIZE]
                                         [-f SKIP] [-l LIMIT] [-o {json,csv}]
                                         http

L's Rural Elasticsearch Tools

positional arguments:
  http                  ElasticSearch Http Server Address! E.g
                        Http://192.168.1.250:9200

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        ElasticSearch Index! E.g shop_20171101 or shop _2017*
  -t TYPE, --type TYPE  ElasticSearch Type! E.g shop
  -s SIZE, --size SIZE  Data Size E.g 2000
  -f SKIP, --skip SKIP  Data From E.g 4000
  -l LIMIT, --limit LIMIT
                        Data Limit E.g 4000
  -o {json,csv}, --out {json,csv}
                        File Type E.g json | csv
					
# python export_data_from_elasticsearch.py http://192.168.50.253:9200/ -i test_201712* -o csv -s 5000