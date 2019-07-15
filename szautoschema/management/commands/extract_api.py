import logging
import os
from django.core.management.base import BaseCommand
import json

# 将drf_yasg生成的json文件转换下格式，列出接口和注释，顺便统计下注释完成率
class Command(BaseCommand):
    help = 'Write the Swagger schema to disk in JSON or YAML format.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-j', '--json', dest='json_file',
            type=str,
            help='请指定json文件.，如： -j api.json'
        )

    def handle(self, json_file,
               *args, **kwargs):
        # disable logs of WARNING and below
        logging.disable(logging.WARNING)

        print("loading json file: %s" % json_file)

        with open(json_file,"r") as fr:
            s = fr.read()

        res=json.loads(s)

        apis = res["paths"]

        uriList = res["paths"].keys()

        apiDocs = []
        apiDocSummaryNum = 0
        normalSummaryNum = 0
        for uri in uriList:
            api = apis[uri]
            methods = api.keys()
            for method in methods:
                if method == "parameters":
                    continue
                apiDoc = {}
                apiDoc['uri'] = uri
                apiDoc['method'] = method
                summary = api[method]["summary"]
                apiDoc['summary'] = summary
                apiDocs.append(apiDoc)

                if len(summary) > 1:
                    normalSummaryNum += 1
                    if "@api" in summary:
                        apiDocSummaryNum += 1

        apiNum = len(apiDocs)

        rep = {"apis":apiDocs}
        print(rep)

        # 写json
        with open("api_result.json","w") as f:
            result = json.dump(rep, f)
            print("已写入api_result.json")
            print("共有api接口%d个, 注释完成率%.0f%%, apiDoc注释完成率%.0f%%" % (apiNum, normalSummaryNum/apiNum*100, apiDocSummaryNum/apiNum*100 ))