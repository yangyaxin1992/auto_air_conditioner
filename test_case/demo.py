# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::11:16
import os.path
import random

import time

import pytest
# module_log = ['zdaemon','zgui','zigbee','zpanel','zvoice','zwifi']
# a = 'find /userdata/zihome/log/'
# for file in module_log :
#     # b = f'find /userdata/zihome/log/{file}'
#     c = f'find /userdata/zihome/log/'
#     d = os.path.join(c,file)
#     print('新的路径：',d)


# @pytest.mark.parametrize('data',['1','2'])
# @pytest.mark.parametrize('mux',['a','b'])
# def test_add(data,mux):
#     a = data + '1'
#     b = mux * 2
#     print(a)
#     print()
#     print(b)


# def test_data():
#     i = 0
#     while i < 100 :
#         i += 1
#         temp = random.randint(19, 30)
#         print("temp:", temp)
#         print("temp的类型：", type(str(temp)))

sn = "2024-08-21 10:57:51.245"
sn = sn.split('.')
print(sn[0])
s_t = time.strptime(sn[0],"%Y-%m-%d %H:%M:%S")
callbackTime = int(time.mktime(s_t))
print("时间：",callbackTime)
sno_1 = str(callbackTime)[:-3]
print("时间戳：",sno_1)
