import json


# 获取配置
def get_config():
    with open('config.json', 'r') as configFile:
        json_obj = json.load(configFile)
        return Config(json_obj)


# 配置类
class Config:
    def __init__(self, json_obj):
        self.mail_host = json_obj['mail_host']
        self.mail_port = json_obj['mail_port']
        self.mail_user = json_obj['mail_user']
        self.mail_password = json_obj['mail_password']
        self.sender = json_obj['sender']
        self.receivers = json_obj['receivers']


if __name__ == '__main__':
    config = get_config()
    print(vars(config))
