#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 14:17
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : cBioPortal_gene.py
# @Software: PyCharm

import os, sys
import pandas as pd
import re
import glob
from scipy.stats import ttest_ind
from scipy.stats import levene
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
os.chdir('C:\\Users\\acorndx_liting\\Desktop\\变红Gene\\mRNA')


def gettxts(out):
    O=open(out,'a+')
    txts=glob.glob('C:\\Users\\acorndx_liting\\Desktop\\变红Gene\\mRNA\\'+'*txt')
    for txt in txts:
        print(txt)
        name=os.path.basename(txt)
        gene=name.split('_')[0]
        p=readcsv(txt)
        O.write(gene+'\n'+p)
    O.close()

def readcsv(file):
    data=pd.read_table(file,sep='\t',header=0)
    NONE_VIN = (data['Alteration'].isnull())
    #df_null = data[NONE_VIN]
    data = data[~NONE_VIN]
    #gene3=data[data['Alteration']=='NPM1: MUT;DNMT3A: MUT;FLT3: MUT;']['ADAMTS10, mRNA expression (RNA Seq V2 RSEM) (log)']
    gene3=data[data.Alteration.apply(listlen3)].iloc[:,1]
    gene2=data[data.Alteration.apply(listlen2)].iloc[:,1]
    gene1=data[data.Alteration.apply(listlen1)].iloc[:,1]
    t1,p1=ttest_ind(gene3,gene1)
    t2,p2=ttest_ind(gene3, gene2)##ind用于独立样本的t检验；ttest_rel配对样本t检验
    #print(levene(gene3,gene1))###检验方差是否齐性
    pvalue='DNMT3A;FLT3;NPM1 VS one gene pvalue is\t{0}\nDNMT3A;FLT3;NPM1 VS two gene pvalue is\t{1}\n'.format(p1,p2)
    return pvalue

def listlen3(sublist):
    genelist = re.split(';', sublist)
    if len(genelist) == 4:
        return True
    else:
        return False

def listlen2(sublist):
    genelist=sublist.split(';')
    if len(genelist)==3:
        return True
    else:
        return False
def listlen1(sublist):
    genelist=sublist.split(';')
    if len(genelist)==2:
        return True
    else:
        return False

if __name__ == '__main__':
    gettxts('C:\\Users\\acorndx_liting\\Desktop\\变红Gene\\result_gene.txt')
