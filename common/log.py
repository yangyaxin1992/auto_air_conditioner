# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::11:14
import os
import logging
import sys
import shutil
import time
import colorlog

class LoggingInit:

    def logging_init(self,devid):
        log_colors_config = {
            'DEBUG': 'white',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        # 创建logger，如果参数为空则返回root logger
        logger = logging.getLogger("")
        logger.setLevel(logging.INFO)  # 设置logger日志等级

        # 输出到控制台
        console_handler = logging.StreamHandler()
        # 输出到文件
        output_file = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + devid
        # modelpath = os.path.dirname(os.path.realpath(__file__))
        log_file = os.path.join(output_file + ".log")
        # fh = logging.FileHandler(log_file, encoding="utf-8")
        file_handler = logging.FileHandler(filename=log_file, mode='a', encoding='utf8')

        # # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        # logger.setLevel(logging.DEBUG)
        # console_handler.setLevel(logging.DEBUG)
        # file_handler.setLevel(logging.INFO)

        # # 设置输出日志格式
        # formatter = logging.Formatter(
        #     fmt="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        # )

        # 日志输出格式
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )
        # # 特定位置创建日志
        # if not os.path.exists("Logs"):
        #     os.makedirs("Logs")
        # logger = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.DEBUG, datefmt='%a, %d %b %Y %H:%M:%S', filename='Logs/testGene.log', filemode='w')
        # 为handler指定输出格式，注意大小写
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        # if not logger.handlers:
        #     logger.addHandler(console_handler)
        #     logger.addHandler(file_handler)

        # console_handler.close()
        # file_handler.close()

        return True



class Logger(object):
    '''保存日志'''
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a', encoding="utf-8")
        # with open(filename,'a') as obj:
        #     self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # 优化：刷新缓冲区，确保日志实时写入文件/控制台，不会缓存
        self.terminal.flush()
        self.log.flush()


class GetLog:
    '''查找目录下最新的文件,拷贝到指定目录下'''
    def __init__(self,new_path):
        # self.new_path = r'D:\Work(勿删）\04 _自动化项目\auto_testplat\空调\autotest_air_conditioner\log\log_file\\'
        self.new_path = new_path

    def find_new_file(self,dir):
        # 输入目录路径，输出最新文件完整路径
        file_lists = os.listdir(dir)
        print("file_lists:",file_lists)
        file_lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn) if not os.path.isdir(dir + "\\" + fn) else 0)
        log_name = file_lists[-1]
        print('最新的文件为： ' + log_name)
        old_path = os.path.join(dir, file_lists[-1])
        print('完整路径：', old_path)
        shutil.copyfile(old_path,self.new_path+log_name)
        return log_name

# 函数调用
# dir = r'D:\Work(勿删）\03 项目\log'
# get_log = GetLog()
# log_name = get_log.find_new_file(dir)

# sys.stdout = Logger('a.log', sys.stdout)
# sys.stderr = Logger('a.log_file', sys.stderr)  # redirect std err, if necessary

# now it works
# print('print something')
