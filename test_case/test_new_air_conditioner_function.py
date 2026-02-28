#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_new_air_conditioner_function.py
# @Author: yangyaxin
# @Date  : 2024/6/7
# @Desc  :

import logging
import os
import sys
from interface.request_case_3_01 import RequestCase01
from common.log import Logger,LoggingInit
from config.new_judge_log import JudgeLog
import pytest
import allure

@allure.feature("中弘协调器功能测试")
class TestAirConditioner():
    '''
    空调基本功能测试
    '''
    def setup_class(self):
        # 初始化参数，创建实例
        self.devId = "84ba20fffe8031eb_1"
        self.prodTypeId = "VZ00E32210300ZHWK-3-01"
        self.request_case = RequestCase01(self.devId,self.prodTypeId)
        self.endpoint_list = ["84ba20fffe8031eb_1"]
        # SecureCRT日志存放路径
        self.dir = r'D:\Work(勿删）\03 项目\log\10.1.2.1-10.1.2.1 (max3)'
        self.logging_init = LoggingInit()
        # 日志最新存放路径
        self.log_path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\空调\autotest_air_conditioner\log\log_file\\'
        self.judge_log = JudgeLog(self.dir,self.log_path)
        self.path = os.getcwd()
        # self.new_path = os.path.join(self.path, "..", "log", "log_file")
        # sys.stdout = Logger(r'D:\Work(勿删）\04 _自动化项目\auto_testplat\z_touch\log\test_log\ztouch_log.txt', sys.stdout)
        sys.stdout = Logger(os.path.join(self.path, "..", "log", "test_log", "log.txt"), sys.stdout)
        sys.stderr = Logger(os.path.join(self.path, "..", "log", "test_log", "log_error.txt"), sys.stderr)


    def test_000_log(self):
        self.logging_init.logging_init(self.devId)

    @pytest.mark.parametrize("powerstate",['0','1'],ids=['off','on'])
    # @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1","cc86ecfffe35d796_2"], ids=[ 'ep1','ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=[ 'ep1'])
    def test_001_air_conditioner_onoff(self,powerstate,endpoint):
        logging.info("测试中弘设置开关机：")
        # powerstate_list = ['0','1']
        key = self.request_case.payload_onoff["data"][0]["k"]
        # for endpoint in self.endpoint_list :
        print("endpoint:",endpoint)
        self.request_case.payload_onoff["devId"] = endpoint
        print("self.request_case.payload_onoff:",self.request_case.payload_onoff)
        # for state in powerstate_list :
        self.request_case.payload_onoff["data"][0]["v"] = powerstate
        logging.info("*" * 22 + " 开始设置" + key + "命令 "+"*" * 22)
        sno = self.request_case.set_onoff_state()        # 判断resp、notify
        print("sno:", sno)
        result = self.judge_log.judge_result(sno,key,powerstate,endpoint)
        pytest.assume(result)

    @pytest.mark.parametrize("model",["8","4","7","3"],ids=["cool","heat","fan","arefaction"])
    # @pytest.mark.parametrize("endpoint", ["cc86ecfffe35d796_1", "cc86ecfffe35d796_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_002_air_conditioner_model(self,model,endpoint):
        logging.info("测试中弘设置模式：")
        key = self.request_case.payload_model["data"][0]["k"]
        # for endpoint in self.endpoint_list :
        print("endpoint:", endpoint)
        self.request_case.payload_model["devId"]  = endpoint
        self.request_case.payload_model["data"][0]["v"] = model
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_model_state()
        print("sno:", sno)
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, model,endpoint)
        pytest.assume(result)

    @pytest.mark.parametrize("windspeed",["1","2","3"],ids=["low","middle","high"])
    # @pytest.mark.parametrize("endpoint", ["cc86ecfffe35d796_1", "cc86ecfffe35d796_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_003_air_condiioner_windspeed(self,windspeed,endpoint):
        logging.info("测试中弘设置风速：")
        key = self.request_case.payload_windspeed["data"][0]["k"]
        # for endpoint in self.endpoint_list:
        self.request_case.payload_windspeed["devId"]  = endpoint
        self.request_case.payload_windspeed["data"][0]["v"] = windspeed
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_windspeed_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, windspeed,endpoint)
        pytest.assume(result)

    @pytest.mark.parametrize("temp", ["19", "26", "30"], ids=["low", "middle", "high"])
    # @pytest.mark.parametrize("endpoint", ["cc86ecfffe35d796_1", "cc86ecfffe35d796_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_004_air_conditioner_temp(self,temp,endpoint):
        logging.info("测试中弘设置温度：")
        key = self.request_case.payload_temp["data"][0]["k"]
        # for endpoint in self.endpoint_list:
        self.request_case.payload_temp["devId"] = endpoint
        self.request_case.payload_temp["data"][0]["v"] = temp
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_temp_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, temp,endpoint)
        pytest.assume(result)

    # 在cool、heat模式下遍历设置温度
    @pytest.mark.parametrize("temp", ["19", "26", "30"], ids=["low", "middle", "high"])
    @pytest.mark.parametrize("model", ["3", "4"], ids=["cool", "heat"])
    # @pytest.mark.parametrize("endpoint", ["cc86ecfffe35d796_1", "cc86ecfffe35d796_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_005_air_conditioner_temp(self, temp, model,endpoint):
        logging.info("不同模式下测试中弘设置温度：")
        # 先设置model(cool，heat)
        key = self.request_case.payload_model["data"][0]["k"]
        # for endpoint in self.endpoint_list :
        self.request_case.payload_model["devId"] = endpoint
        self.request_case.payload_model["data"][0]["v"] = model
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_model_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, model,endpoint)
        if pytest.assume(result) :
            logging.info("#" * 22 + "设置" + key + "命令成功" + "#" * 22)
        else :
            logging.info("#" * 22 + "设置" + key + "命令失败" + "#" * 22)
        # 开始设置温度
        key = self.request_case.payload_temp["data"][0]["k"]
        # for endpoint in self.endpoint_list:
        self.request_case.payload_temp["devId"] = endpoint
        self.request_case.payload_temp["data"][0]["v"] = temp
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_temp_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, temp, endpoint)
        pytest.assume(result)

    # 在cool、heat、fun模式下遍历设置windspeed
    @pytest.mark.parametrize("windspeed",["1","2","3"],ids=["low","middle","high"])
    @pytest.mark.parametrize("model", ["3", "4","7"], ids=["cool", "heat", "fan"])
    # @pytest.mark.parametrize("endpoint", ["cc86ecfffe35d796_1", "cc86ecfffe35d796_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_006_air_condiioner_windspeed(self,windspeed,model,endpoint):
        logging.info("不同模式下测试中弘设置风速：")
        # 先设置model(cool，heat)
        key = self.request_case.payload_model["data"][0]["k"]
        # for endpoint in self.endpoint_list :
        self.request_case.payload_model["devId"] = endpoint
        self.request_case.payload_model["data"][0]["v"] = model
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_model_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, model, endpoint)
        if pytest.assume(result) :
            logging.info("#" * 22 + "设置" + key + "命令成功" + "#" * 22)
        else :
            logging.info("#" * 22 + "设置" + key + "命令失败" + "#" * 22)
        # 开始设置windspeed
        key = self.request_case.payload_windspeed["data"][0]["k"]
        # for endpoint in self.endpoint_list:
        self.request_case.payload_windspeed["devId"] = endpoint
        self.request_case.payload_windspeed["data"][0]["v"] = windspeed
        logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
        sno = self.request_case.set_windspeed_state()
        # 判断resp、notify
        result = self.judge_log.judge_result(sno, key, windspeed,endpoint)
        pytest.assume(result)
