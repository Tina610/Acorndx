#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 16:32
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : BeidaRenmin_class.py
# @Software: PyCharm

import os, sys
import xlrd
import xlwt
import re
import itertools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))


def main():
    dealtest=BeiDainterpre(classfication=sys.argv[1],combination=sys.argv[2],inputfile=sys.argv[3],outroad=sys.argv[4])
    #dealtest.genedict()
    dealtest.enddeal()

class BeiDainterpre():
    def __init__(self,classfication,combination,inputfile,outroad):
        self.classify=classfication
        self.combination=combination
        self.input=inputfile
        self.road=outroad
        self.gene = {'BL1': 0, 'ASXL1': 0, 'BCOR': 0, 'BRAF': 0, 'CALR': 0, 'CBL': 0, 'CEBPA': 0, 'CSF3R': 0,
                     'DDX41': 0, 'DKC1': 0, 'DNMT3A': 0, 'ETNK1': 0, 'ETV6': 0, 'EZH2': 0, 'FLT3': 0, 'GATA1': 0,
                     'GATA2': 0, 'IDH1': 0, 'IDH2': 0, 'JAK2': 0, 'KIT': 0, 'KRAS': 0, 'MLL': 0, 'MPL': 0, 'NF1': 0,
                     'NPM1': 0, 'NRAS': 0, 'PHF6': 0, 'PIGA': 0, 'PTPN11': 0, 'RUNX1': 0, 'SETBP1': 0, 'SF3B1': 0,
                     'SH2B3': 0, 'SRSF2': 0, 'STAG2': 0, 'STAT3': 0, 'TERC': 0, 'TERT': 0, 'TET2': 0, 'TP53': 0,
                     'U2AF1': 0, 'WT1': 0, 'ZRSR2': 0}

        self.result={}
    def deal_class(self):
        dict_classify={}
        sheets=xlrd.open_workbook(self.classify)
        worksheet=sheets.sheet_by_index(0)
        rows=worksheet.nrows
        for row in range(1,rows):
            if not worksheet.row(row)[9] in dict_classify and worksheet.cell(row,10).value!='':
                dict_classify[worksheet.cell(row,9).value]=worksheet.cell(row,10).value
            else:
                pass
        return dict_classify

    def gene_list(self):
        genecombin=[]
        self.summary={}
        classify=self.deal_class()
        pattern=re.compile('NM_\d+\((\w+)\):*')
        if self.postive_nagetive():
            with open(self.input,'r') as F1:
                title=F1.readline()
                for line in F1:
                    lines=line.strip('\n').split('\t')
                    hgvs=lines[0]
                    hgvs=hgvs.replace(r'<i>','')
                    hgvs=hgvs.replace(r'</i>','')
                    id=lines[-1]
                    if hgvs=='FLT3-ITD':
                        genecombin.append(hgvs)
                        self.gene['FLT3'] = []
                        self.gene['FLT3'].append([lines[2],lines[0]])
                    else:
                        try:
                            gene=pattern.search(hgvs).group(1)
                            if not id in classify:continue
                            if gene in self.gene:
                                genecombin.append(gene)
                                if isinstance(self.gene[gene],list):
                                    self.gene[gene].append([lines[2],hgvs])
                                else:
                                    self.gene[gene]=[]
                                    self.gene[gene].append([lines[2],hgvs])
                        except:
                            pass
                    if id in classify:
                        if not hgvs in self.summary:
                            self.summary[hgvs]=[]
                            self.summary[hgvs].append(classify[id])
                        else:
                            self.summary[hgvs].append(classify[id])

                    else:
                        pass
        return genecombin
    def file_combin(self):
        genecombin={}
        sheets=xlrd.open_workbook(self.combination)
        worksheet=sheets.sheet_by_index(0)
        nrows=worksheet.nrows
        for row in range(1,nrows):
            if not worksheet.cell(row,0).value in genecombin:
                genecombin[worksheet.cell(row,0).value]=worksheet.cell(row,1).value
            else:
                print('have an gene combination error')
        return genecombin
    def deal_combin(self):
        self.genecombin={}
        combintemp=[]
        combindict=self.file_combin()
        combingene=self.gene_list()
        for i in range(2, 6):
            for j in itertools.permutations(combingene, i):
                com_gene='&'.join(j)
                if com_gene in combindict:
                    combintemp.append(com_gene)
                else:
                    pass
        maxlist=self.extract_comgene(combintemp)
        for genemax in maxlist:
            if not genemax in self.genecombin:
                self.genecombin[genemax]=combindict[genemax]
            else:
                print(genemax)

    def extract_comgene(self,listcom):
        endcom=[]
        temp=4
        for comgene in listcom:
            lenmax=len(comgene)
            if 'RUNX1' in comgene:
                endcom.append(comgene)
            else:
                if lenmax>temp:
                    temp=lenmax
        endcom.append(comgene)
        return endcom


    def genedict(self):
        temp=self.gene_list()
        for gene in self.gene:
            print(gene,self.gene[gene])
    def enddeal(self):
        self.deal_combin()
        temp = os.path.basename(self.input)
        sample=temp.split('-')[0]
        excelname=sample+'_hospital'+'.xls'
        workbook=xlwt.Workbook(encoding = 'ascii')
        worksheet=workbook.add_sheet(sample)
        n=1
        worksheet.write(0,0,'基因',self.set_style(bold=True))
        worksheet.write(0,1,'频率',self.set_style(bold=True))
        worksheet.write(0,2,'突变',self.set_style(bold=True))
        for gene in sorted(self.gene):
            if isinstance(self.gene[gene],list):
                for value in self.gene[gene]:
                    worksheet.write(n,0,gene,self.set_style())
                    worksheet.write(n,1,value[0],self.set_style())
                    worksheet.write(n,2,value[1],self.set_style())
                    n+=1
            else:
                worksheet.write(n,0,gene,self.set_style())
                worksheet.write(n,1,self.gene[gene],self.set_style())
                n+=1

        worksheet.write(n+1,0,'突变',self.set_style(bold=True))
        worksheet.write(n+1,1,'临床意义',self.set_style(bold=True))
        n=n+2
        if self.summary:
            for hgvs in self.summary:
                for cell in self.summary[hgvs]:
                    worksheet.write(n,0,hgvs,self.set_style())
                    worksheet.write(n,1,cell,self.set_style())
                    n+=1
        else:
            worksheet.write(n,0,'在检测内容范围内，本次未检测到与血液肿瘤相关的单核苷酸变异(SNV)和小片段插入/缺失(InDel)。请结合临床其他检测结果，综合医生建议，进行相关诊疗',self.set_style())
            n+=1
        worksheet.write(n+1,0,'多基因分析',self.set_style(bold=True))
        n=n+2
        if self.genecombin:
            for combin in self.genecombin:
             worksheet.write(n,0,combin,self.set_style())
             worksheet.write(n,1,self.genecombin[combin],self.set_style())
        else:
            pass
        workbook.save(self.road+'/'+excelname)

    def set_style(self,name='Times New Roman', height=200, bold=False):
        style = xlwt.XFStyle() 
        font = xlwt.Font()  
        font.name = name  
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    def postive_nagetive(self):
        sample=os.path.basename(self.input)
        posnage=True
        letter=sample.split('-')[-1]
        if 'N' in letter:
            posnage=False
        return posnage





if __name__ == '__main__':
    main()

