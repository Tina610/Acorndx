#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/29 16:51
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : Assay_aritical.py
# @Software: PyCharm
‘’‘
此程序主要利用文献数据库改成bib的形式
’‘’
import os, sys
import re
import xlrd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))


def main(file,out):
    assay=readassay(file,out)
    assay.readfile()

class readassay():
    def __init__(self,infile,outfile):
        self.infile=infile
        self.outfile=outfile
        self.assy=[]

    def encode(self,decoenco):
        if isinstance(decoenco,str):
            return decoenco
        else:
            decoenco = decoenco.decode('gb2312').encode('utf-8')
            return decoenco
        # decoenco=decoenco.decode("unicode_escape").encode("utf8")
        # return decoenco
    def readfile(self):
        outtxt=open (self.outfile,'w',encoding='UTF-8')
        sheet=xlrd.open_workbook(self.infile)
        xlsx=sheet.sheet_by_index(0)
        nrows=xlsx.nrows
        for row in range(1,nrows):
            id=str(xlsx.cell(row,0).value)
            if re.match('^\d+',id):
                pmid='pmid'+id
            else:
                pmid=id
            author=xlsx.cell(row,1).value
            title=xlsx.cell(row,2).value
            page=xlsx.cell(row,7).value
            journal=xlsx.cell(row,4).value
            year=xlsx.cell(row,5).value
            volume=xlsx.cell(row,6).value
            # print(id,page,journal,year,volume)
            information='''\@article={left}{pmid},
            author={left}{author}{right},
            journal={left}{journal}{right},
            pages={left}{page}{right},
            pmid={left}{id}{right},
            title={left}{title}{right},
            volume={left}{volume}{right},
            year={left}{year}{right},
            {right}\n'''.format(left='{',right='}',pmid=pmid,author=author,journal=journal,page=page,id=id,title=title,volume=volume,year=year)
            #print(information)
            outtxt.write(information)

if __name__ == '__main__':
    #main(sys.argv[1],sys.argv[2])
    main('C:\\Users\\acorndx_liting\\Desktop\\遗传咨询需求\\数据库\\Bibliography-20160708.xlsx','C:\\Users\\acorndx_liting\\Desktop\\遗传咨询需求\\数据库\\assay_bib.txt')