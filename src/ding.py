
import requests
from core.logger import log
from core.config import MESSAGE_DINGDING


"""推送到消息到 Message 钉钉群"""
def message_dingding_api(data):
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + MESSAGE_DINGDING
    d = {
        "text": {
            "content": 
                    data['title'] + '\n' + 
                    "内容: " + data['text'] + '\n' +
                    "时间: " + data['date'] + '\n'
        },
        "msgtype": "text",
        "at": {
            "isAtAll": True
        }
    }
    responce = requests.post(url, json = d)
    if responce.json()["errcode"] == 0:
        log.info(f"{data['title']} 推送成功!")
    else:
        log.error(f"{data['title']} 推送失败!")
