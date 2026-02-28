# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::12:32
from common.sendmethod import RequestConnector
from common.ssh_connect import SshConnect
import json
import uuid
import logging

class RemoteAccess:
    '''
    启动远程连接权限
    '''
    def __init__(self,mac,port=10007):
        self.mac = mac
        self.port = port
        self.value = f"[common]\nserver_addr = 192.144.233.51\nserver_port = 10000\n\n\n[{self.mac}]\ntype = tcp\nlocal_ip = 127.0.0.1\nlocal_port= 22\nauthentication_timeout = 0\nremote_port = {self.port}"
        self.payload = {
            "msgType": "DEVICE_CONTROL",
            "devId": "2418C69B1FC7",
            "prodTypeId": "ZH-C0101",
            "time": "2019-09-19 18:27:10",
            "sno": "123",
            "attribute": "debug",
            "command": "start",
            "data": [
                {
                    "k": "content",
                    # "v": "[common]\nserver_addr = 192.144.233.51\nserver_port = 10000\n\n\n[ssh10007]\ntype = tcp\nlocal_ip = 127.0.0.1\nlocal_port= 22\nauthentication_timeout = 0\nremote_port = 10007"
                    "v":  self.value
                }, {
                    "k": "timeout",
                    "v": "7200"
                }
            ],
        }
        self.request_connect = RequestConnector()

    def retry_request(self,command):
        # 重试请求，直到请求发送成功退出循环
        self.payload["command"] = command
        self.payload["sno"] = str(uuid.uuid1())
        sno = self.payload
        print("sno", sno)
        print("*"*88)
        flag = 0
        count = 0
        while count < 5 :
            rep = self.request_connect.post_request(self.payload)
            print("rep:",rep)
            if rep:
                logging.info(rep.text)
                if rep.status_code == 200:
                    msg = json.loads(rep.text)
                    print("msg", msg)
                    if 200 == msg["code"]:
                        break
                        # flag += 1
                    else :
                        count += 1

                else :
                    count += 1
            else :
                count += 1
        return count

    def start_remote_access(self,command="start"):
        # 启动远程权限
        count = self.retry_request(command)
        return count
    def stop_remote_access(self,command="stop"):
        # 关闭远程权限
        count =  self.retry_request(command)
        return count