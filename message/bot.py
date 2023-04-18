# -*- coding: UTF-8 -*-
import os
import requests
import json

WEB_HOOK = os.environ.get('WEB_HOOK') if (os.environ.get('WEB_HOOK') != None) else "web_hook"

class QYWXMessage():
    data = ''

class MessageBot():
    
    def __init__(self, logd=False):
        self.log = logd
        pass
    
    def _log(self, content):
        if self.log:
            print(f'MessageBot: {content}')
    
    def _send_message(self, message: str) -> bool:
        self._log(message)
        pass
    
class QYWXMessageBot(MessageBot):
    
    webhook_url = 'your_webhook_url'
    
    def __init__(self, hook: str, log=False):
        super().__init__(logd=log)
        self._log(f'Init bot with hook: {hook}')
        self.webhook_url = hook
        
    def send_message(self, message: QYWXMessage) -> bool:
        print(message)
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        self._log(f'MessageBot:<REQT>{json.dumps(message.data)}')
        response = requests.post(self.webhook_url, headers=headers, data=json.dumps(message.data))
        self._log(f'MessageBot:<RESP>{response}')
        return super()._send_message(message)



class QYWXMessageText(QYWXMessage):
    
    def __init__(self, content: str, log=False):
        self.data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
        }
        
class QYWXMessageMD(QYWXMessage):
    
    def __init__(self, content: str, log=False):
        self.data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            },
        }
        
class QYWXMessageIMG(QYWXMessage):
    
    def __init__(self, base64: str, md5: str, log=False):
        self.data = {
            "msgtype": "image",
            "image": {
                "base64": base64,
                "md5": md5
            },
        }

if __name__ == '__main__':
    hook = WEB_HOOK
    message = 'Test message ..'
    bot = QYWXMessageBot(hook)
    bot.send_message(message)