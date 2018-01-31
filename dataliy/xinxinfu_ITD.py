#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/31 10:45
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : xinxinfu_ITD.py
# @Software: PyCharm

import os, sys
import glob,re
'''
提取送检的ITD阴性样本，截止2017年4月25,252期；
'''
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
def getdirs(indir):
    filedir=[]
    dirs=glob.glob(indir+'/*/result/')
    for dir in dirs:
        batch=dir.split(r'/')[-3]
        if float(batch)>252 or float(batch)<241:continue
        try:
            content=glob.glob(dir+'/Variant/ITD/*ITD_RESULT.txt')[0]
            sample=os.path.basename(dir)
            eles=';'.join([sample,content,batch])
            filedir.append(eles)
        except Exception as e:
            print(line+str(e))
    return filedir
def dealContent(indir2,out):
    files=getdirs(indir2)
    OUT=open(out,'w')
    for file in files:
        info={}
        [sample,itd,batch]=file.split(';')
        filesize=os.path.getsize(itd)
        if filesize !=12:
            continue
        OUT.write(batch,sample,itd)
    OUT.closed

if __name__ == '__main__':
    dealContent(sys.argv[1],sys.argv[2])