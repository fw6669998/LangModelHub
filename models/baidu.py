import requests
import json

import config
from lib.LangModel import LangModel

API_KEY = config.baiduApiKey
SECRET_KEY = config.baiduApiSecret


class models:
    ERNIE_Bot_4 = LangModel('ERNIE-Bot-4', 'completions_pro', 0.12)
    ERNIE_Bot = LangModel('ERNIE-Bot', 'completions', 0.012)
    ERNIE_Bot_turbo = LangModel('ERNIE-Bot-turbo', 'eb-instant', 0.008)
    ChatGLM2_6B_32K = LangModel('ChatGLM2_6B_32K', 'chatglm2_6b_32k', 0.008)
    Qianfan_Chinese_Llama_2_7B = LangModel('Qianfan-Chinese-Llama-2-7B', 'qianfan_chinese_llama_2_7b', 0.008)


def getAnswer(quest, model=models.ERNIE_Bot_turbo):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/" + model.method + "?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": quest
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    obj = response.json()
    if "result" not in obj:
        return "请求接口失败: " + str(obj)
    else:
        return obj["result"]


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
