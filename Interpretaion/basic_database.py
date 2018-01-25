#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 10:43
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : basic_database.py
# @Software: PyCharm

import os, sys
import re
import xlwt
import xlrd
import xlutils.copy import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
class database():
    def __init__(self,inputfile,genedata,mutationdata,outfile):
        self.infile=inputfile
        self.genedata=genedata
        self.mutationdata=mutationdata
        self.out=outfile
        self.data={}
        self.gene={}

    def readgene(self):
        genefile=xlrd.open_workbook(self.genedata)
        information=genefile.sheet_by_index(0)
        for row in range(1,information.nrows):
            keys=information.cell(row,0)
            values=[information.cell(row,10).value,information.cell(row,14).value,information.cell(row,15).value]
            if not keys in self.data:
                self.data[keys]=values
            else:
                print(keys+'is an error geneid')
    def readmuta(self):
        mutaionfile=xlrd.open_workbook(self.mutationdata)
        information=mutaionfile.sheet_by_index(0)
        for row in range(1,information.nrows):
            keys=information.cell(row,1).value
            value=information.cell(row,5).value
            if not keys in self.gene:
                self.gene[keys]=value
            else:
                print(keys +'is an error gene')
    def readsample(self):
        workbook=xlrd.open_workbook(self.infile)
        worksheet=workbook.sheet_by_index(0)
        title=worksheet.


def main():
    pass


if __name__ == '__main__':
    main()
