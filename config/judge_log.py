# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::10:40
import logging
import os
import re
import json
import allure
from common.log import GetLog
import time

# 判断正则表达式的数据为空时，.sno时间戳可能错1，需要更新sno，重新匹配
def g_sno(sno_1):
    # 按照一定时间戳规则匹配对应resp与notify
    si = int(sno_1[-1])
    print(si, type(si))
    if si < 9:
        sr = str(si + 1)
        # sr = int(sno_1[-1]) + 1
        sno_2 = sno_1[:-1] + sr
        print(sno_2)
        return sno_2
    return g_sno(sno_1[:-1]) + '0'


class JudgeLog():
    '''
    判断发送请求响应结果
    '''

    # log正则匹配的数据转换成json格式
    def __init__(self,dir,path):
        # SecureCRT日志存放路径
        self.dir = dir
        self.path = path
        # # SecureCRT日志存放路径
        # self.dir = r'D:\Work(勿删）\03 项目\log'
        # # 日志最新存放路径
        # self.path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\空调\autotest_air_conditioner\log\log_file\\'


    def log_change_json(self,r):
        # 正则的数据，经过一定规则处理后，数据转换成json格式
        chars = '\n\t'
        for c in chars:
            # 将列表里的元素，去掉\n\t
            r[-1] = r[-1].replace(c, '')
        # print(r[-1])
        code_data = json.loads(r[-1])
        print("转换后的数据：",code_data)
        return code_data

    # sno正则匹配时，遇到时间戳差1时，需要通过一定的计算获取sno

    # 获取开关、模式、风速、温度响应resp
    def get_set_resp(self, key, log_name, sno):
        logging.info(self.path + log_name)
        try:
            with open(self.path + log_name, encoding='utf-8') as obj:
                # with open(r"D:\Work(勿删）\04 _自动化项目\auto_testplat\light\log\log_file\ZGateway_Main_202112231524_019070_001.log",encoding='utf-8') as obj:
                log = obj.read()
                # print("打印log",log)
                # sno = 'bdd39bc9-87fc-11ec-9a30-dc1ba18ce37f'
                # sno = 'dd604b5a-6dfd-11ec-a491-002432a04e89'
                symbol = '.*\n'
                regex_onoff = r'LOG_DEBUG ({.*\n.*"msgType"' + '.*' + '"DEVICE_CONTROL_RESP"' + symbol * 4 + '.*"sno"' + '.*' + sno + '"' + symbol * 2 + '.*"command"' + '.*' + '"set_powerstate_resp"' + symbol * 14 + '})'
                regex_model = r'LOG_DEBUG ({.*\n.*"msgType"' + '.*' + '"DEVICE_CONTROL_RESP"' + symbol * 4 + '.*"sno"' + '.*' + sno + '"' + symbol * 2 + '.*"command"' + '.*' + '"set_model_resp"' + symbol * 14 + '})'
                regex_windspeed = r'LOG_DEBUG ({.*\n.*"msgType"' + '.*' + '"DEVICE_CONTROL_RESP"' + symbol * 4 + '.*"sno"' + '.*' + sno + '"' + symbol * 2 + '.*"command"' + '.*' + '"set_windspeed_resp"' + symbol * 14 + '})'
                regex_temp = r'LOG_DEBUG ({.*\n.*"msgType"' + '.*' + '"DEVICE_CONTROL_RESP"' + symbol * 4 + '.*"sno"' + '.*' + sno + '"' + symbol * 2 + '.*"command"' + '.*' + '"set_temperature_resp"' + symbol * 14 + '})'
                if key == 'powerstate':
                    r = re.findall(regex_onoff, log)
                elif key == 'model':
                    r = re.findall(regex_model, log)
                elif key == 'windspeed':
                    r = re.findall(regex_windspeed, log)
                elif key == 'temperature':
                    r = re.findall(regex_temp, log)
                # r =  re.findall(r'LOG_DEBUG ({\n.*"msgType".*\n.*\n.*\n.*\n.*"sno":	"'+sno+'"'+symbol*13+'})',log)
            logging.info("r:%s",r)
            # print(len(r))
            if len(r) == 1:
                code_data = self.log_change_json(r)
                logging.info("resp的数据解析： %s",code_data)
                return code_data
            elif len(r) > 1:
                code_data = self.log_change_json(r[-2:])
                logging.info("resp的数据解析： %s",code_data)
                return code_data
            else:
                logging.info("没有获取到指定的数据，测试失败")
                return False
        except FileNotFoundError as f:
            logging.info("文件不存在，请检查文件路径")

    # 判断resp
    def judge_set_resp(self, key, log_name, sno,endpoint):
        code_data = self.get_set_resp(key, log_name, sno)
        if code_data == False:
            return False
        else:
            if code_data['data'][0]['k'] == 'code':
                if code_data['data'][0]['v'] == '0':
                    if code_data['expData']['endpoint'] == endpoint:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    # 判断开关、亮度状态改变通知notify
    def judge_device_notify(self, key, log_name, sno, state,endpoint):
        code_data = self.get_set_resp(key, log_name, sno)
        if code_data == False:
            return False
        else:
            sn = code_data['data'][2]['v']
            sno_1 = sn[:-3]
            # print(type(sno_1))

            logging.info("sno_1:%s", sno_1)
            try:
                with open(self.path + log_name, encoding='utf-8') as obj:
                    # with open(r'D:\Work(勿删）\04 _自动化项目\auto_testplat\light\log\log_file\ZGateway_Main_202112231349_019070_000.log',encoding='utf-8') as obj:
                    log = obj.read()
                    # print(str(log))
                    # sno = 'f02415f7-63b7-11ec-b6a9-dc1ba18ce37c'
                    symbol = '.*\n'
                    regex_onoff_change = r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_powerstate_change"' + symbol * 9 + '})'
                    regex_model_change = r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_model_change"' + symbol * 9 + '})'
                    regex_windspeed_change = r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_windspeed_change"' + symbol * 9 + '})'
                    regex_temp_change = r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_temperature_change"' + symbol * 9 + '})'
                    if key == 'powerstate':
                        r = re.findall(regex_onoff_change, log)
                    elif key == 'model':
                        r = re.findall(regex_model_change, log)
                    elif key == 'windspeed':
                        r = re.findall(regex_windspeed_change, log)
                    elif key == 'temperature':
                        r = re.findall(regex_temp_change, log)
                    # print(r)
                    logging.info("查询出的NOTIFY数据: %s", r)
                # 判断正则表达式的数据为空时，sno时间戳可能错1，需要更新sno，重新匹配
                if len(r) == 0:
                    i = 0
                    while i < 5:
                        # 循环找5S内的sno时间戳
                        i += 1
                        sno_1 = g_sno(sno_1)
                        # print("sno_2", sno_2)
                        logging.info("sno_1:%s",sno_1)
                        if key == 'powerstate':
                            r = re.findall(
                                r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_powerstate_change"' + symbol * 9 + '})',
                                log)
                        elif key == 'model':
                            r = re.findall(
                                r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_model_change"' + symbol * 9 + '})',
                                log)
                        elif key == 'windspeed':
                            r = re.findall(
                                r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_windspeed_change"' + symbol * 9 + '})',
                                log)
                        elif key == 'temperature':
                            r = re.findall(
                                r'LOG_DEBUG ({\n.*"msgType"' + '.*' + '"DEVICE_NOTIFY"' + symbol * 4 + '.*"sno"' + '.*' + sno_1 + '.*"' + symbol * 2 + '.*"command"' + '.*' + '"on_temperature_change"' + symbol * 9 + '})',
                                log)
                        # r = re.findall(
                        #     r'LOG_DEBUG ({\n.*"msgType":      "DEVICE_NOTIFY' + symbol * 4 + '.*"sno":  "' + sno_1 + '"' + symbol * 8 + '})',
                        #     log)
                        # print(r)
                        logging.info("更新sno后查询出的NOTIFY数据: %s", r)
                        if len(r) != 0:
                            break
                logging.info("r:%s",r)
                logging.info("notify上报记录有：%d",len(r))
                if len(r) == 1:
                    device_data = self.log_change_json(r)
                    logging.info("notify的数据解析： %s",device_data)
                elif len(r) > 1:
                    logging.info("#"*22+"上报notify记录大于1条，请分析："+"#"*22)
                    device_data = self.log_change_json(r[-2:])
                    logging.info(device_data)
                else:
                    logging.info("没有获取到指定的数据，测试失败")
                    return False
                # print(device_data['data'][0]['v'], v)

                if device_data['data'][0]['k'] == key:
                    if device_data['data'][0]['v'] == state:
                        if device_data['expData']['endpoint'] == endpoint:
                            # print("*" * 22 + key+" notify结果判断pass" + "*" * 22)
                            return True
                        else:
                            # print("*" * 22 + key+" notify结果判断fail" + "*" * 22)
                            return False
                    else :
                        # print("*" * 22 + key+" notify结果判断fail" + "*" * 22)
                        return False
                else :
                    # print("*" * 22 + key+" notify结果判断fail" + "*" * 22)
                    return False

            except:
                logging.info("文件不存在，请检查文件路径")

    def judge_result(self,sno,key,state,endpoint):
        # 判断日志结果
        # 获取最新log
        time.sleep(30)
        # print()
        logging.info("#"*22+"设置"+key+"命令成功"+"#"*22)
        get_log = GetLog(self.path)
        log_name = get_log.find_new_file(self.dir)
        logging.info(log_name)
        # judge_log = JudgeLog()
        # 判断响应码
        # print()
        logging.info("*" * 22 + "开始判断"+ key + "的resp结果" + "*" * 22)
        result = self.judge_set_resp(key,log_name,sno,endpoint)
        # pytest.assume(result)
        # 判断状态改变通知
        if result :
            # print()
            logging.info("#"*22+key +"的resp结果判断：pass"+"#"*22)
            # if key == 'powerstate' or key == 'model' or key == 'windspeed':
            # print('onoff or level')
            # print()
            logging.info("*" * 22 + "开始判断"+ key + "的notify结果" + "*" * 22)
            device_notify = self.judge_device_notify(key,log_name,sno,state,endpoint)
            # pytest.assume(device_notify)
            # return pytest.assume(device_notify)
            if device_notify :
                # print()
                logging.info("#" * 22 + key + "的notify结果判断：pass" + "#" * 22)
                return True
            else :
                # print()
                logging.info("#" * 22 + key + "的notify结果判断：fail" + "#" * 22)
                return False

            # elif key == 'temperature':
            #     # print("temp")
            #     temp_notify = self.judge_temp_notify(key,log_name,sno,state)
            #     # pytest.assume(temp_notify)
            #     # return pytest.assume(temp_notify)
            #     return temp_notify
            # else:
            #     return False
        else:
            # print()
            logging.info("#" * 22 + key +  "的resp结果判断：fail" + "#" * 22)
            return False

    def statistics_loss_rate(self,success_count,fail_count):
        # 统计丢包率
        logging.info("#"*22+"测试结束："+"#"*22)
        loss = float(fail_count / (success_count + fail_count))
        loss_rate = "%.2f%%" % (loss * 100)
        logging.info("执行成功次数：%s", success_count)
        logging.info("执行失败次数：%s", fail_count)
        logging.info("丢包率：%s", loss_rate)
        allure.attach(f"执行成功次数：{success_count}", "成功次数", allure.attachment_type.TEXT)
        allure.attach(f"执行失败次数：{fail_count}", "失败次数", allure.attachment_type.TEXT)
        allure.attach(f"控制成功率：{loss_rate}", "成功率", allure.attachment_type.TEXT)

if __name__ == '__main__':
    pass


