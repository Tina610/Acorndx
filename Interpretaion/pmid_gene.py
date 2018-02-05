#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/4 19:28
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : pmid_gene.py
# @Software: PyCharm

import os, sys
import re
import xlrd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
‘’‘
此程序主要是利用基因库和突变库改写文献引用格式，匹配而已
’‘’
def readfilemutation(infile,outfile):
    file=xlrd.open_workbook(infile)
    OUT=open(outfile,'w')
    sheet1=file.sheet_by_index(0)
    nrows=sheet1.nrows
    for row in range(nrows):
        if row==0:
            txt='\t'.join(sheet1.row_values(row))
            OUT.write(txt+'\n')
        else:
            geneinfo=(sheet1.cell(row,10).value).split('。')
            result=pmidmutation(geneinfo)
            value1=sheet1.row(row)[0:10]
            value1=exvalue(value1)
            value2=result
            value3=sheet1.row(row)[11:16]
            value3=exvalue(value3)
            OUT.write('{0}\t{1}\t{2}\n'.format(value1,value2,value3))
def readfilegene(infile,outfile):
    file=xlrd.open_workbook(infile)
    OUT=open(outfile,'w')
    sheet1=file.sheet_by_index(0)
    nrows=sheet1.nrows
    for row in range(nrows):
        if row==0:
            txt='\t'.join(sheet1.row_values(row))
            OUT.write(txt+'\n')
        else:
            geneinfo=(sheet1.cell(row,5).value).split('。')
            result=pmidgene(geneinfo)
            value1=sheet1.row(row)[0:5]
            value1=exvalue(value1)
            value2=result
            OUT.write('{0}\t{1}\n'.format(value1,value2))

def exvalue(value):
    tmp=[]
    for i in value:
        j=i.value
        tmp.append(j)
    temp='\t'.join(tmp)
    return temp

def pmidgene(listinfo):
    information=[]
    for info in range(0,len(listinfo)-1):
        if re.findall(r'\[\d+\]',listinfo[info]):
            ids=re.findall(r'\[(\d+)\]',listinfo[info])
            tmp=[]
            for id in ids:
                id=id.replace('[','')
                id=id.replace(']','')
                pmidsing = 'pmid' + id
                tmp.append(pmidsing)
            tmp=','.join(tmp)
            pmidsub='\cite{left}pmid{tmp}{right}'.format(left='{',right='}',tmp=tmp)
            info = re.sub(id, pmidsub, listinfo[info])
            information.append(info)
        elif re.search(r'\[\d+.*?\]',listinfo[info]):
            id=re.search(r'\[(\d.*)\]',listinfo[info]).group(1)
            print(id)
            ids=id.split(',')
            tmp=[]
            for pm in ids:
                pmidsing='pmid'+pm
                tmp.append(pmidsing)
            tmp=','.join(tmp)
            pmidsub='\cite{left}pmid{tmp}{right}'.format(left='{',right='}',tmp=tmp)
            info=re.sub(id,pmidsub,listinfo[info])
            information.append(info)
        else:
            information.append(listinfo[info])
    #print(information)
    information='。'.join(information)
    return information
def pmidmutation(listinfo):
    information=[]
    for info in range(0,len(listinfo)-1):
        if re.search(r'\[\d+\]',listinfo[info]):
            ids=re.search(r'\[(\d+)\]',listinfo[info]).group(1)
            pmidsub='\cite{left}pmid{tmp}{right}'.format(left='{',right='}',tmp=ids)
            info = re.sub(ids, pmidsub, listinfo[info])
            information.append(info)
        else:
            information.append(listinfo[info])
    #print(information)
    information='。'.join(information)
    return information



if __name__ == '__main__':
    #readfile(sys.argv[1],sys.argv[2])
    readfilegene('C:\\Users\\acorndx_liting\\Desktop\\遗传咨询需求\\数据库\\基因库.xls','C:\\Users\\acorndx_liting\\Desktop\\遗传咨询需求\\数据库\\gene.xls')