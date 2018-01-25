#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 13:49
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : Beida_outer.py
# @Software: PyCharm

import os, sys
import argparse
import subprocess
form interpretation import BeidaRenmin_class as BeidaRenmin
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
parser = argparse.ArgumentParser()
parser.add_argument('--classf','-c',help='Gene Mutation Class File', action='store',dest='classf')
parser.add_argument('--genecom','-g',help='combination genes of hospital',action='store',dest='com',required=True)
parser.add_argument('--leuout','-i',help='sample in leu result',action='store',dest='input',required=True)
args=parser.parse_args()

def getnerate(inputfile,outputroad):
    dealClass=BeidaRenmin(args.classf,args.com,inputfile,outputroad)
    dealClass.enddeal()
    return True

def findfile(road):
    inlist=[]
    outlist=[]
    dirs=os.listdir(road)
    if 'Leu_interpretation' in dirs:
        txtdir=os.path.join(road,'Leu_interpretation')
        txtfile=os.listdir(txtdir)
        for file in txtfile:
            if '附件' in file:continue
            name=file.split('-')[0]
            if name in dirs:
                inputfile=os.path.join(txtfile,file)
                outroad=os.path.join(road,name)
                inlist.append(inputfile)
                outlist.append(outroad)
    else:
        raise Exception('fatal error not have leuresult!')

def main():
    infiles,outsamples=findfile(args.input)
    for i,o in zip(infiles,outsamples):
        if getnerate(i,o):
            print(i)
        else:
            print('Error')


if __name__ == '__main__':
    main()
