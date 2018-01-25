#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/01/10 10:21
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : file_ITD_content.py
# @Software: PyCharm

import os, sys
import glob,re
'''
根据file list的路径，计算ITD阳性样本
'''
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
def getdirs(indir):
    filedir=[]
    with open(indir,'r') as F:
        for line in F:
            try:
                content=glob.glob(line+'/Variant/ITD/*ITD_RESULT.txt')[0]
                sample=os.path.basename(line)
                eles=';'.join([sample,content])
                filedir.append(eles)
            except Exception as e:
                print(line+str(e))
    return filedir
def dealContent(indir2,out):
    files=getdirs(indir2)
    OUT=open(out,'w')
    for file in files:
        info={}
        [sample,itd]=file.split(';')
        filesize=os.path.getsize(itd)
        if filesize ==12:
            continue
        with open(itd,'r') as F:
            for line in F:
                line=line.strip('\n').split('\t')
                keys='\t'.join([line[0],line[1]])
                info[keys]=line[-1]
            (keys,value)=max(info.items(),key=lambda x:x[1])
            value='%.2f%%'%(float(value)*100)
            OUT.write('{sample}\tFLT3_ITD\t{tent}\n'.format(sample=sample,tent=value))
    OUT.closed

if __name__ == '__main__':
    dealContent(sys.argv[1],sys.argv[2])
