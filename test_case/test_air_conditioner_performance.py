# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::11:30
import logging
import os
import random
import sys
import pytest
import allure
from common.log import Logger,LoggingInit
from interface.request_case import RequestCase
from config.judge_log import JudgeLog

@allure.feature("中弘协调器性能测试")
class TestAirConditionerPerformance():
    def setup_class(self):
        # 初始化参数,创建实例
        self.devId = "cc86ecfffe35d796"
        self.prodTypeId = "VZ00E32210300ZHWK"
        self.request_case = RequestCase(self.devId,self.prodTypeId)
        self.endpoint_list = ['1','2']
        # SecureCRT日志存放路径
        self.dir = r'D:\Work(勿删）\03 项目\log\192.168.18.1-192.168.18.1'
        self.logging_init = LoggingInit()
        # 日志最新存放路径
        self.log_path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\空调\autotest_air_conditioner\log\log_file\\'
        self.judge_log = JudgeLog(self.dir, self.log_path)
        self.count = 5 # 循环次数
        self.path = os.getcwd()
        sys.stdout = Logger(os.path.join(self.path, "..", "log", "test_log", "log.txt"), sys.stdout)
        sys.stderr = Logger(os.path.join(self.path, "..", "log", "test_log", "log_error.txt"), sys.stderr)

    def test_000_log(self):
        self.logging_init.logging_init(self.devId)

    @pytest.mark.parametrize("endpoint",['1','2'],ids=['ep1','ep2'])
    def test_001_powerstate_perssure(self,endpoint):
        logging.info("压力测试开关机：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count :
            i += 1
            powerstate_list = ['0','1']
            key = self.request_case.payload_onoff["data"][0]["k"]
            self.request_case.payload_onoff["expData"]["endpoint"] = endpoint
            for powerstate in powerstate_list :
                self.request_case.payload_onoff["data"][0]["v"] = powerstate
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case.set_onoff_state()
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

    @pytest.mark.parametrize("endpoint",['1','2'],ids=['ep1','ep2'])
    def test_002_model_perssure(self,endpoint):
        logging.info("压力测试设置不同model：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count :
            i += 1
            model_list = ['3', '4','7','8']
            key = self.request_case.payload_model["data"][0]["k"]
            self.request_case.payload_model["expData"]["endpoint"] = endpoint
            for model in model_list :
                self.request_case.payload_model["data"][0]["v"] = model
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case.set_model_state()
                result = self.judge_log.judge_result(sno,key,model,endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s",success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！",sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    @pytest.mark.parametrize("model",['3','4','7'],ids=['cool','heat','fan'])
    @pytest.mark.parametrize("endpoint", ['1', '2'], ids=['ep1', 'ep2'])
    def test_003_windspeed_perssure(self,endpoint,model):
        logging.info("测试不同model下，设置不同windspeed：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            windspeed_list = ['1', '2', '3']
            key = self.request_case.payload_windspeed["data"][0]["k"]
            self.request_case.payload_windspeed["expData"]["endpoint"] = endpoint
            for windspeed in windspeed_list:
                self.request_case.payload_windspeed["data"][0]["v"] = windspeed
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case.set_windspeed_state()
                result = self.judge_log.judge_result(sno, key, windspeed, endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)


    @pytest.mark.parametrize("model", ['3', '4'], ids=['cool', 'heat'])
    @pytest.mark.parametrize("endpoint", ['1', '2'], ids=['ep1', 'ep2'])
    def test_004_temp_perssure(self,endpoint,model):
        logging.info("测试不同model下，随机设置温度（19℃~30℃）：")
        i = 0
        success_count = 0
        fail_count = 0
        while i < self.count:
            i += 1
            j = 0
            while j < 3 :
                j += 1
                temp_list = random.randint(19,30)
                key = self.request_case.payload_temp["data"][0]["k"]
                self.request_case.payload_temp["expData"]["endpoint"] = endpoint
                # for temp in temp_list:
                self.request_case.payload_temp["data"][0]["v"] = str(temp_list)
                logging.info("*" * 22 + "开始设置" + key + "命令" + "*" * 22)
                sno = self.request_case.set_temp_state()
                result = self.judge_log.judge_result(sno, key, str(temp_list), endpoint)
                if result:
                    success_count += 1
                    logging.info("成功次数：%s", success_count)
                else:
                    fail_count += 1
                    logging.info("失败次数：%s", fail_count)
                    logging.info("断言失败，请检查结果！", sno)
        # 统计压力测试丢包率
        self.judge_log.statistics_loss_rate(success_count, fail_count)

