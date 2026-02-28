#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_new_air_conditioner_performance.py
# @Author: yangyaxin
# @Date  : 2024/6/17
# @Desc  :

import logging
import os
import random
import sys
import pytest
import allure
from common.log import Logger,LoggingInit
from interface.request_case_3_01 import RequestCase01
from interface.request_case_3_10 import RequestCase10
from interface.request_case_3_11 import RequestCase11
from config.new_judge_log  import JudgeLog

@allure.feature("中弘协调器性能测试")
class TestAirConditionerPerformance():
    def setup_class(self):
        # 初始化参数,创建实例
        self.devId_01 = "84ba20fffe8031eb_1"
        self.prodTypeId_01 = "VZ00E32210300ZHWK-3-01"
        self.devId_10 = "84ba20fffe8031eb_2"
        self.prodTypeId_10 = "VZ00E32210300ZHWK-3-10"
        self.devId_11 = "84ba20fffe8031eb_3"
        self.prodTypeId_11 = "VZ00E32210300ZHWK-3-11"
        self.request_case_01 = RequestCase01(self.devId_01,self.prodTypeId_01)
        self.request_case_10 = RequestCase10(self.devId_10,self.prodTypeId_10)
        self.request_case_11 = RequestCase11(self.devId_11,self.prodTypeId_11)
        self.endpoint_list = ["c49894fffecb1bd1_1"]
        # SecureCRT日志存放路径
        self.dir = r'D:\Work(勿删）\03 项目\log\10.1.3.1-10.1.3.1'
        self.logging_init = LoggingInit()
        # 日志最新存放路径
        self.log_path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\空调\autotest_air_conditioner\log\log_file\\'
        self.judge_log = JudgeLog(self.dir, self.log_path)
        self.count = 3 # 循环次数
        self.path = os.getcwd()
        sys.stdout = Logger(os.path.join(self.path, "..", "log", "test_log", "log.txt"), sys.stdout)
        sys.stderr = Logger(os.path.join(self.path, "..", "log", "test_log", "log_error.txt"), sys.stderr)

    def test_000_log(self):
        self.logging_init.logging_init(self.devId_01)

    # @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_1","84ba20fffe8031eb_2"],ids=['ep1','ep2'])
    @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_1"],ids=['ep1'])
    def test_001_conditioner_powerstate_perssure(self,endpoint):
        logging.info("压力测试空调开关机：")
        i = 0
        success_count = 0
        fail_count = 0
        print("endpoint:", endpoint)
        while i < self.count :
            i += 1
            powerstate_list = ['0','1']
            key = self.request_case_01.payload_onoff["data"][0]["k"]
            self.request_case_01.payload_onoff["devId"] = endpoint
            for powerstate in powerstate_list :
                self.request_case_01.payload_onoff["data"][0]["v"] = powerstate
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_01.set_onoff_state()
                print("sno:", sno)
                result = self.judge_log.judge_result(sno,key,powerstate,endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s",success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！",sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)

    # @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_1","84ba20fffe8031eb_2"],ids=['ep1','ep2'])
    @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_1"],ids=['ep1'])
    def test_002_conditioner_model_perssure(self,endpoint):
        logging.info("压力测试设置空调不同model：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count :
            i += 1
            model_list = ['1', '2','4','8','1']
            key = self.request_case_01.payload_model["data"][0]["k"]
            self.request_case_01.payload_model["devId"] = endpoint
            for model in model_list :
                self.request_case_01.payload_model["data"][0]["v"] = model
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_01.set_model_state()
                result = self.judge_log.judge_result(sno,key,model,endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s",success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果,%s",sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    # @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1","84ba20fffe8031eb_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_003_conditioner_windspeed_perssure(self,endpoint):
        logging.info("压力测试设置空调不同windspeed：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            windspeed_list = ['1', '2', '3']
            key = self.request_case_01.payload_windspeed["data"][0]["k"]
            self.request_case_01.payload_windspeed["devId"] = endpoint
            for windspeed in windspeed_list:
                self.request_case_01.payload_windspeed["data"][0]["v"] = windspeed
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_01.set_windspeed_state()
                result = self.judge_log.judge_result(sno, key, windspeed, endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果，%s", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    # @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1","84ba20fffe8031eb_2"], ids=['ep1', 'ep2'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_1"], ids=['ep1'])
    def test_004_conditioner_temp_perssure(self,endpoint):
        logging.info("压力测试随机设置空调温度（19℃~30℃）：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            j = 0
            while j < 3 :
                j += 1
                temp_list = random.randint(19,30)
                key = self.request_case_01.payload_temp["data"][0]["k"]
                self.request_case_01.payload_temp["devId"] = endpoint
                # for temp in temp_list:
                self.request_case_01.payload_temp["data"][0]["v"] = str(temp_list)
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_01.set_temp_state()
                result = self.judge_log.judge_result(sno, key, str(temp_list), endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果, %s", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)

    @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_2"],ids=['ep2'])
    # @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_2"],ids=['ep2','ep3','ep4'])
    def test_005_ventilator_powerstate_perssure(self,endpoint):
        logging.info("压力测试新风开关机：")
        i = 0
        success_count = 0
        fail_count = 0
        print("endpoint:", endpoint)
        while i < self.count :
            i += 1
            ventilator_powerstate_list = ['0','1']
            key = self.request_case_10.payload_onoff["data"][0]["k"]
            self.request_case_10.payload_onoff["devId"] = endpoint
            for powerstate in ventilator_powerstate_list :
                self.request_case_10.payload_onoff["data"][0]["v"] = powerstate
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_10.set_onoff_state()
                print("sno:", sno)
                result = self.judge_log.judge_result(sno,key,powerstate,endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s",success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！",sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)

    @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_2"],ids=['ep2'])
    def test_006_ventilator_model_perssure(self, endpoint):
        logging.info("压力测试设置新风不同model：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            ventilator_model_list = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','A','B','C','D','E','F','15','4']
            key = self.request_case_10.payload_model["data"][0]["k"]
            self.request_case_10.payload_model["devId"] = endpoint
            for model in ventilator_model_list:
                self.request_case_10.payload_model["data"][0]["v"] = model
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_10.set_model_state()
                result = self.judge_log.judge_result(sno, key, model, endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果,%s", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)

    @pytest.mark.parametrize("endpoint",["84ba20fffe8031eb_2"],ids=['ep2'])
    def test_007_ventilator_windspeed_perssure(self, endpoint):
        logging.info("压力测试设置新风不同windspeed：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            windspeed_list = ['1', '2', '3', '4', '5','1']
            key = self.request_case_10.payload_windspeed["data"][0]["k"]
            self.request_case_10.payload_windspeed["devId"] = endpoint
            for windspeed in windspeed_list:
                self.request_case_10.payload_windspeed["data"][0]["v"] = windspeed
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_10.set_windspeed_state()
                result = self.judge_log.judge_result(sno, key, windspeed, endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果，%s", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    # @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_6", "84ba20fffe8031eb_7", "84ba20fffe8031eb_8"],ids=['ep6', 'ep7', 'ep8'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_3"],ids=['ep3'])
    def test_008_floorheater_powerstate_perssure(self, endpoint):
        logging.info("压力测试地暖开关机：")
        i = 0
        success_count = 0
        fail_count = 0
        print("endpoint:", endpoint)
        while i < self.count:
            i += 1
            ventilator_powerstate_list = ['0', '1']
            key = self.request_case_11.payload_onoff["data"][0]["k"]
            self.request_case_11.payload_onoff["devId"] = endpoint
            for powerstate in ventilator_powerstate_list:
                self.request_case_11.payload_onoff["data"][0]["v"] = powerstate
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_11.set_onoff_state()
                print("sno:", sno)
                result = self.judge_log.judge_result(sno, key, powerstate, endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    # @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_6", "84ba20fffe8031eb_7", "84ba20fffe8031eb_8"],ids=['ep6', 'ep7', 'ep8'])
    @pytest.mark.parametrize("endpoint", ["84ba20fffe8031eb_3"],ids=['ep3'])
    def test_009_floorheater_temp_perssure(self, endpoint):
        logging.info("压力测试随机设置地暖温度（5℃~90℃）：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            j = 0
            while j < 3:
                j += 1
                temp_list = random.randint(5, 33)
                key = self.request_case_11.payload_temp["data"][0]["k"]
                self.request_case_11.payload_temp["devId"] = endpoint
                # for temp in temp_list:
                self.request_case_11.payload_temp["data"][0]["v"] = str(temp_list)
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case_11.set_temp_state()
                result = self.judge_log.judge_result(sno, key, str(temp_list), endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果, %s", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)