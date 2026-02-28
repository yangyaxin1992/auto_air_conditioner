# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::11:10

import json
import requests

class RequestConnector:
    '''接口请求'''
    def __init__(self):
        self.url_qlink = 'https://qlink.zihome.com/link-handle-gateway/v1/operate/device/control'
        self.url_gw = 'https://gw.zihome.com/link-handle-gateway/v1/operate/device/control'
        self.control_headers = {'GATEWAY-VALIDATE': 'kLSIUlsSLILEKXasAAALIELKFJCKSILidksKALSIDKCKAKSIDKOA',
                          'content-type': 'application/json'}

    def post_request_qlink(self,payload):
        rep = requests.post(url=self.url_qlink,data=json.dumps(payload),headers=self.control_headers, timeout=(10, 10))
        return rep

    def post_request_gw(self,payload):
        rep = requests.post(url=self.url_gw,data=json.dumps(payload),headers=self.control_headers, timeout=(10, 10))
        return rep

if __name__ == '__main__':
    request_connect = RequestConnector()


