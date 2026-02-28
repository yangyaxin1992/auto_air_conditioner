#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : request_case_3_01.py
# @Author: yangyaxin
# @Date  : 2024/6/7
# @Desc  :


import json
import logging
import uuid
import requests
from common.sendmethod import RequestConnector

class RequestCase01():
    '''
    空调支持接口请求设置的用例
    '''
    def __init__(self,devId,prodTypeId):
        # 初始化接口请求的参数
        self.devId = devId
        self.prodTypeId = prodTypeId
        # 空调开关状态接口参数
        self.payload_onoff = {
           "msgType": "DEVICE_CONTROL",
           "devId": "cc86ecfffe35d796_1",
           "prodTypeId":   "VZ00E32210300ZHWK-3-01",
           "time": "2018-05-14 10:10:10",
           "sno": "789",
            "attribute":"conditioner_powerstate",
            "command":"set_powerstate",
            "data":[{
                "k":"powerstate",
                "v":"0"
            }]
        }
        # 空调模式接口参数
        self.payload_model = {
           "msgType": "DEVICE_CONTROL",
           "devId": "cc86ecfffe35d796_1",
           "prodTypeId":   "VZ00E32210300ZHWK-3-01",
           "time": "2018-05-14 10:10:10",
           "sno": "789",
            "attribute":"conditioner_model",
            "command":"set_model",
            "data": [{
                    "k":    "model",
                    "v":    "3"
            }]
        }
        # 空调风速接口参数
        self.payload_windspeed = {
           "msgType": "DEVICE_CONTROL",
           "devId": "cc86ecfffe35d796_1",
           "prodTypeId":   "VZ00E32210300ZHWK-3-01",
           "time": "2018-05-14 10:10:10",
           "sno": "789",
            "attribute":"conditioner_windspeed",
            "command":"set_windspeed",
            "data":[{
                "k":"windspeed",
                "v":"3"
            }]
        }
        # 空调温度接口参数
        self.payload_temp = {
           "msgType": "DEVICE_CONTROL",
           "devId": "cc86ecfffe35d796_1",
           "prodTypeId":   "VZ00E32210300ZHWK-3-01",
           "time": "2018-05-14 10:10:10",
           "sno": "789",
            "attribute":"conditioner_temperature",
            "command":"set_temperature",
            "data":[{
                "k":"temperature",
                "v":"35"
            }]
        }

        # 创建接口请求实例
        self.request_connect = RequestConnector()

    def set_onoff_state(self):
        # 初始化设备的vi的，prodtypeid
        # self.payload_onoff["devId"] = self.devId
        self.payload_onoff["prodTypeId"] = self.prodTypeId
        self.payload_onoff["sno"] = str(uuid.uuid1())
        sno = self.payload_onoff['sno']
        logging.info("sno: %s", sno)
        #发送接口请求
        flag = 0
        while flag == 0 :
            try :
                resp = self.request_connect.post_request_qlink(self.payload_onoff)
                if resp:
                    logging.info(resp.text)
                    if resp.status_code == 200:
                        msg = json.loads(resp.text)
                        logging.info("msg: %s", msg)
                        if 200 == msg["code"]:
                            flag += 1
                            break
                            # return sno
                        else:
                            flag += 0
                    else:
                        flag += 0
                else:
                    flag += 0
            except requests.exceptions.RequestException:
                flag = 0
        return sno

    def set_model_state(self):
        # 初始化设备的vi的，prodtypeid
        # self.payload_model["devId"] = self.devId
        self.payload_model["prodTypeId"] = self.prodTypeId
        self.payload_model["sno"] = str(uuid.uuid1())
        sno = self.payload_model['sno']
        logging.info("sno: %s", sno)
        #发送接口请求
        flag = 0
        while flag == 0 :
            # 捕获请求超时异常
            try :
                resp = self.request_connect.post_request_qlink(self.payload_model)
                if resp:
                    logging.info(resp.text)
                    if resp.status_code == 200:
                        msg = json.loads(resp.text)
                        logging.info("msg :%s", msg)
                        if 200 == msg["code"]:
                            flag += 1
                            break
                            # return sno
                        else :
                            flag += 0
                    else:
                        flag += 0
                else:
                    flag += 0
            except requests.exceptions.RequestException:
                flag = 0
        return sno

    def set_windspeed_state(self):
        # 初始化设备的vi的，prodtypeid
        # self.payload_windspeed["devId"] = self.devId
        self.payload_windspeed["prodTypeId"] = self.prodTypeId
        self.payload_windspeed["sno"] = str(uuid.uuid1())
        sno = self.payload_windspeed['sno']
        logging.info("sno: %s", sno)
        #发送接口请求
        flag = 0
        while flag == 0 :
            try :
                resp = self.request_connect.post_request_qlink(self.payload_windspeed)
                if resp:
                    logging.info(resp.text)
                    if resp.status_code == 200:
                        msg = json.loads(resp.text)
                        logging.info("msg:%s", msg)
                        if 200 == msg["code"]:
                            flag += 1
                            break
                        else:
                            flag += 0
                    else:
                        flag += 0
                else:
                    flag += 0
            except requests.exceptions.RequestException:
                flag = 0
        return sno

    def set_temp_state(self):
        # 初始化设备的vi的，prodtypeid
        # self.payload_temp["devId"] = self.devId
        self.payload_temp["prodTypeId"] = self.prodTypeId
        self.payload_temp["sno"] = str(uuid.uuid1())
        sno = self.payload_temp['sno']
        logging.info("sno: %s", sno)
        #发送接口请求
        flag = 0
        while flag == 0 :
            try :
                resp = self.request_connect.post_request_qlink(self.payload_temp)
                if resp:
                    logging.info(resp.text)
                    if resp.status_code == 200:
                        msg = json.loads(resp.text)
                        logging.info("msg:%s", msg)
                        if 200 == msg["code"]:
                            flag += 1
                            break
                        else:
                            flag += 0
                    else :
                        flag += 0
                else :
                    flag += 0
            except requests.exceptions.RequestException:
                flag = 0
        return sno