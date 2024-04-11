from lib.LangModel import LangModel
from openai import OpenAI
import config

# 设置openai的API密钥
API_KEY = config.openaiApiKey


class models:
    gpt_35_turbo = LangModel('gpt-3.5-turbo', '', 0.01)
    gpt_4_turbo = LangModel('gpt-4-1106-preview', '', 0.2)
    gpt_4 = LangModel('gpt-4', '', 0.4)


def getAnswer(quest, model=models.gpt_35_turbo):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=model.name,
        messages=[
            {"role": "user", "content": quest},
        ]
    )
    return response.choices[0].message.content


def getAnswerByFtModel(quest):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        # model='ft:gpt-3.5-turbo-1106:ms::8PiV2LXt',
        # model='ft:gpt-3.5-turbo-1106:ms::8TL9h27e',
        model='ft:gpt-3.5-turbo-1106:ms::8fOWgVgA',
        messages=[
            {"role": "system", "content": "你是一个指令编辑员"},
            {"role": "user", "content": quest},
        ]
    )
    return response.choices[0].message.content
