import sys, os, math
import time
from datetime import datetime

import models.baidu as baidu
import models.ali as ali
import models.spark as spark
import models.openai as openai

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask import Flask, request
import json

app = Flask(__name__, static_folder='static')


@app.route("/")
def index():
    return "<script>window.location = '/static/index.html';</script>"


@app.route('/data')
def data():
    return ""
    # return kdata


# models = {"百度": baidu.models, "阿里": ali.models, "讯飞": spark.models, "openai": openai.models}
factoryObjs = {"百度": baidu, "阿里": ali, "讯飞": spark, "openai": openai}


@app.get('/getModels')
def getModels():
    res = []
    for factoryName in factoryObjs.keys():  # 遍历厂家
        for item in vars(factoryObjs[factoryName].models):  # 遍历模型
            if item.startswith("__"):
                continue
            item2 = getattr(factoryObjs[factoryName].models, item)
            resItem = {}
            resItem["model"] = factoryName + '.' + item
            for key in vars(item2):  # 遍历模型属性
                if key.startswith("__"):
                    continue
                resItem[key] = getattr(item2, key)
            res.append(resItem)
    return json.dumps(res)


@app.post('/getAnswer')
def getAnswer():
    # startTime = math.floor(time.time() * 1000)
    quest = request.form.get('quest')
    model = request.form.get('model')
    # exceptVal = request.form.get('except')
    # exceptVal = tool.getVal(exceptVal)
    # exceptVal = 100
    # model= "baidu.ERNIE_Bot_4" 用.分割
    model1 = model.split('.')
    factoryName = model1[0]
    modelName = model1[1]
    factoryObj = factoryObjs[factoryName]
    modelObj = getattr(factoryObj.models, modelName)

    answer = ""
    try:
        answer = factoryObj.getAnswer(quest, modelObj)
    except Exception as e:
        answer = "请求接口失败"
    # endTime = math.floor(time.time() * 1000)

    # real = tool.getVal(answer)
    # real = 100
    # error = None

    # if exceptVal is not None and real is not None:
    #     error = math.fabs(exceptVal - real)
    # createTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # data = {"quest": quest, "model": model, "factory": factory, "answer": answer, "time": endTime - startTime,
    #         "except": exceptVal, "actual": real, "error": error, 'create_time': createTime}
    # # 清理data中的None字段
    # data = {k: v for k, v in data.items() if v is not None}
    return answer


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
