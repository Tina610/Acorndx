#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 20:12
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : WESfilter_target.py
# @Software: PyCharm

import sys
####从全外数据过滤芯片结果

def filter(targetbed,inputvcf,outvcf):
    ttars=readtarget(targetbed)
    VCF=open(outvcf,'w')
    with open(inputvcf,'r') as V:
        for cell in V:
            if cell.startswith('#'):
                VCF.write(F)
            else:
                lines=cell.strip('\n').split('\t')
                key='\t'.join(lines[0:2])
                if key in ttars:
                    VCF.write(cell)
    VCF.close()

def readtarget(target):
    dicttar={}
    with open(target,'r') as F:
        for line in F:
            lines=line.strip('\n').split('\t')
            chr=lines[0].replace('chr','')
            for i in range(int(lines[1],int(lines[2])+1)):
                key=chr+'\t'+str(i)
                if not key in dicttar:
                    dicttar[key]=1
                else:
                    print('this site '+str(i)+'is error')
    return dicttar

if __name__ == '__main__':
    filter(sys.argv[1],sys.argv[2],sys.argv[3])
