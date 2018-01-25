#! /usr/bin/env python3
import os, sys, re


class annoFileDivid():
    def getlines(self):
        nls = []
        lines = open(self.resultFile, 'r').readlines()
        self.title = lines[0].strip()
        for i in range(1, len(lines)):
            line = lines[i].strip()
            cells = line.split('\t')
            if len(cells)>18 and (cells[0] == 'FLT3-ITD' or (cells[2] == '' and cells[18] != 'synonymous SNV' \
                    and (cells[15] == 'exonic' or cells[15] == 'splicing'))):
                nls.append(line)
            else:
                pass
        return nls


    def __init__(self, resultFile):
        self.resultFile = resultFile
        self.needlines = self.getlines()

    def returntitle(self):
        return self.title

    def resultprint(self):
        for i in self.needlines:
            print('Baochu:{}'.format(i))

    def returnlines(self):
        return self.needlines


if __name__ == '__main__':
    test = annoFileDivid('/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/'
                         'Commercial/HB_234_20170318105823/result/HB15GL00312-1-28/Variant/'
                         'SNP-INDEL_MT/FILTER/HB15GL00312-1-28-RESULT.xls')
    test.resultprint()
