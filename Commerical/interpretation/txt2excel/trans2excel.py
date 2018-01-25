#! /usr/bin/env python3

import os, sys, re
import xlrd
import xlwt
from txt2excel import readtxt


class trans2excel():
    def __init__(self, path, output='./tmp', sep='\t', type='xls'):
        self.path = path
        self.out = output
        self.sep = sep
        self.type = type

    def isfile(self, mydir):
        for lists in os.listdir(mydir):
            path = os.path.join(mydir, lists)

            if os.path.isdir(path):
                self.isfile(path)
            else:
                self.files.append(path)

    def getfiles(self):
        self.files = []
        if os.path.isdir(self.path):
            self.isfile(self.path)
        else:
            self.files.append(self.path)
        return self.files

    def extractlines(self, file):
        self.getfiles()
        rt = readtxt.readtxt(file, self.sep)
        lines = rt.readfile()
        return lines

    def generateExcel(self):
        self.getfiles()
        self.files.sort()
        fmt = '@'
        style = xlwt.XFStyle()
        style.num_format_str = fmt
        if not os.path.exists('{}.{}'.format(self.out, self.type)):
            workbook = xlwt.Workbook(encoding='ascii')
            for efile in self.files:
                filename = os.path.basename(efile)
                filename = filename.replace('.txt', '')
                worksheet = workbook.add_sheet(filename)
                mylines = self.extractlines(efile)
                row = 0
                for line in mylines:

                    line = line.strip()
                    cells = line.split(self.sep)
                    for col in range(0, len(cells)):
                        worksheet.write(row, col, cells[col],style)
                    row += 1

            workbook.save('{}.{}'.format(self.out, self.type))
        else:
            print('({}.{}) is existed, please check the File!!\n'
                  .format(self.out, self.type))


if __name__ == '__main__':
    test = trans2excel('/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial/others_batches/test/test_239/result/out/Leu_interpretation',
                       '/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/V2_panel/test12_RERUN_20160120/chenyuelong/tmp/excel')
    files = test.getfiles()
    test.generateExcel()
    for i in files:
        print('file:{}'.format(i))
