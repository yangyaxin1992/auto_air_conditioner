# ！/usr/bin/env python
# -*- coding:utf8 -*-
# author:yangyaxin time::13:55
import pytest
import sys
import os


if __name__ == '__main__':
    # 定义测试集
    # args = ['-s', '-q', '--alluredir=', r'D:\Work(勿删）\04 _自动化项目\auto_testplat\lock\report\report']
    # self_args = sys.argv[1:]
    # pytest.main(args)
    cmd = 'allure generate %s -o %s' % (r'D:\Work(勿删）\04 _自动化项目\auto_testplat\lock\report\report',
                                        r'D:\Work(勿删）\04 _自动化项目\auto_testplat\lock\report\allure-report')

    try:
        # shell.invoke(cmd)
        result = os.popen(cmd)
    except Exception as e:
        print('执行用例失败，请检查环境配置')
        raise


