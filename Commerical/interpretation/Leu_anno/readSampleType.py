#! /usr/bin/env python3
import os, sys
import re
import xlrd


class readSampleType():
    def __init__(self, excelfile):
        self.file = excelfile

    def whichType(self, type):
        if re.search('AML', type):
            return 'AML'
        elif re.search(r'/', type):
            return 'MDS/MPN'
        elif re.search('MDS', type):
            return 'MDS'
        elif re.search('MPN', type):
            return 'MPN'
        elif re.search('ALL', type):
            return 'ALL'
        elif re.search('CML', type):
            return 'CML'
        elif re.search('CLL', type):
            return 'CLL'
        else:
            return 'allgene'

    def read(self):
        self.dict = {}
        data = xlrd.open_workbook(self.file)
        table = data.sheets()[0]
        for i in range(1, table.nrows):
            sample = table.cell(i, 4).value
            type = self.whichType(table.cell(i, 7).value)
            # print('Sample:{},Type:{}'.format(sample,type))
            self.dict[sample] = type

    def returndict(self):
        self.read()
        return self.dict

if __name__ == '__main__':
    test = readSampleType('/annoroad/data1/bioinfo/PROJECT/RD/Medical'
                     '/Leukemia/V2_panel/test12_RERUN_20160120/chenyuelong/tmp/leu.xlsx')
    mydict=test.returndict()
    for i in mydict:
        print('tets:{},gogogo{}'.format(i,mydict[i]))
