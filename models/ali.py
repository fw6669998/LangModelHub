import random
from http import HTTPStatus
import dashscope
from lib.LangModel import LangModel
import config

dashscope.api_key = config.aliApiKey

name = "通义千问"


class models:
    qwen_turbo = LangModel('qwen-turbo', dashscope.Generation.Models.qwen_turbo, 0.008)
    qwen_plus = LangModel('qwen-plus', dashscope.Generation.Models.qwen_plus, 0.02)
    # llama2_7b_chat_v2 = LangModel('llama2-7b-chat-v2', 'llama2-7b-chat-v2', None)
    qwen_14b_chat = LangModel('qwen-14b-chat', 'qwen-14b-chat', 0.008, True)
    qwen_7b_chat = LangModel('qwen-7b-chat', 'qwen-7b-chat', 0.006, True)
    baichuan2_7b_chat_v1 = LangModel('baichuan2-7b-chat-v1', 'baichuan2-7b-chat-v1', 0.006, True)
    # ziya_llama_13b_v1 = LangModel('ziya-llama-13b-v1', 'ziya-llama-13b-v1', 0.006, True)


def getAnswer(quest, model=models.qwen_turbo):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': quest}]
    response = dashscope.Generation.call(
        model.method,
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices.pop().message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return "请求接口失败," + response.message
