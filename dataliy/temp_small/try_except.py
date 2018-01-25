#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 14:19
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : try_except.py
# @Software: PyCharm

import os

# os.getcwd()

try:
    file = open('Test.txt')
    test = open('/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/test.txt', 'w')
    for line in file:
        try:
            (info, site) = line.split(':', 1)
            print('prognosis:', end='')
            print(info, end='')
            print('site infomation:', end='')
            print(site, end='')
            print(site, file=test)
        except ValueError:
            pass
            # except Exception as err:   ###for all error type
            # print('pass'+str(err))
        # file.close()
        # test.close()
except IOError as err:
    print('The data file is missing!' + str(err))
finally:
    if 'test' in locals():
        test.close()
        file.close()
        test.close()

'''
try:
    with open('Test.txt') as data:
        print("it's ",data.readline())
        # print("it's ",file=data)
except IOError as err:
    print('File error:'+str(err))
meters=[1,2,3]
sec=[m*60 for m in meters]
print(sec)
'''