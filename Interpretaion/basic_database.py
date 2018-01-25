#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 10:43
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : basic_database.py
# @Software: PyCharm

import os, sys
import re
import xlrd
os.chdir('C:\\Users\\acorndx_liting\\Desktop\\遗传咨询需求\\第一版')
print(os.getcwd())
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
class database():
    def __init__(self,inputfile,genedata,mutationdata,outfile):
        self.infile=inputfile
        self.genedata=genedata
        self.mutationdata=mutationdata
        self.out=outfile
        self.data={}
        self.gene={}

    def readmuta(self):
        genefile=xlrd.open_workbook(self.mutationdata)
        information=genefile.sheet_by_index(0)
        for row in range(1,information.nrows):
            keys=information.cell(row,0).value
            values=[information.cell(row,14).value,information.cell(row,15).value,information.cell(row,10).value]
            if not keys in self.data:
                self.data[keys]=values
            else:
                print(keys+'is an error geneid')
    def readgene(self):
        mutaionfile=xlrd.open_workbook(self.genedata)
        information=mutaionfile.sheet_by_index(0)
        for row in range(1,information.nrows):
            keys=information.cell(row,1).value
            value=information.cell(row,5).value
            if not keys in self.gene:
                self.gene[keys]=value
            else:
                print(keys +'is an error gene')
    def readsample(self):
        name=os.path.basename(self.infile)
        if '5-N.txt' in name:
            os.system('mv '+self.infile+' '+self.out)
        else:
            OUT=open(self.out,'w')
            with open(self.infile,'r') as F:
                title=F.readline()
                titles='\t'.join(title.split('\t')[0:3])
                print(titles)
                OUT.write('{0}\t位点意义\t证据级别\t参考依据\t疾病\n'.format(titles))
                pattern = re.compile('NM_\d+\((\w+)\):*')
                for line in F:
                    lines=line.strip('\n').split('\t')
                    hgvs=lines[0]
                    hgvs=hgvs.replace(r'<i>','')
                    hgvs=hgvs.replace(r'</i>','')
                    id = lines[-1]
                    gene = pattern.search(hgvs).group(1)
                    if id in self.data:
                        info='\t'.join(self.data[id])
                        OUT.write('{0}\t{1}\t{2}\t{3}'.format(hgvs,lines[1],lines[2],info))
                    if gene in self.gene:
                        OUT.write('********基因概述*******:{0}\t{1}\n'.format(self.gene[gene],lines[3]))
        OUT.close()
    def run(self):
        self.readgene()
        self.readmuta()
        self.readsample()
if __name__ == '__main__':
    temp=database('test贴报告表.txt','基因库.xls','突变库.xls','outresult.txt')
    temp.run()

