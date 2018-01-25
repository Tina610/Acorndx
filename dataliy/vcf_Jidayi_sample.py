#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/12 9:55
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : vcf_Jidayi_sample.py
# @Software: PyCharm

import os, sys
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

def findsample(road,file):
    file=glob.glob('{road}/*/*/result/{file}*'.format(road=road,file=file))

def readfile(file,road):
    with open(file,'r') as F:
        for line in F:
            lines=line.strip('\n').split('\t')
            fileroad=findsample(road,lines[0])
            os.system('{fileroad}/Variant/SNP-INDEL_*/ANNO/*-*-Filter.vcf.hg19_multianno.txt|grep {gene}|grep {loc}'
                      .format(fileroad=fileroad,gene=lines[1],loc=lines[2]))



def filefre(road,file)
    pattern = re.compile('[\d]/1:([\d]+),([\d]+):')
    with open(file,'r') as F:
        for line in F:
            lines=line.strip('\n').split('\t')
            fileroad=findsample(road,lines[0])
            sitegene=os.popen('less -S {fileroad}/Variant/SNP-INDEL_*/ANNO/*-Filter.vcf.hg19_multianno.txt|grep {gene}|grep "{loc}"'
                       .format(fileroad=fileroad,gene=lines[1],loc=lines[2]))
            long=sitegene.read().split('\t')
            fre=long[-1]
            if pattern.search(fre):
                ref, alt = pattern.search(fre).groups()
                all=int(ref)+int(alt)
                end=100*float(alt)/all
                print(lines,end)

             #print(long)



if __name__ == '__main__':
    readfile(file,road)
