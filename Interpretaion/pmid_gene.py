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
import xlwt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

def readfile(infile,outfile):
    sheet1=xlrd.open_workbook(infile)
    book=xlwt.Workbook(encoding = 'ascii')
    OUT=book.add_sheet(outfile)
    file1=sheet1.sheet_by_index(0)
    nrows=file1.nrows
    ncols=file1.ncols
    for row in nrows:
        if row==1:
            OUT.write(sheet1.row_values(row))
        else:
            geneinfo=(sheet1.cell(row,5).value).split('。')



def pmid(listinfo):
    for info in range(0,len(listinfo)-1):
        if re.search(r'^[\d+]'):
            id=re.search(r'(^[\d+])').group(1)
            re.replace()

def main():
    pass


if __name__ == '__main__':
    main()
