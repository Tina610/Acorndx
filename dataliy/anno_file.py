#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 10:05
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : anno_file.py
# @Software: PyCharm

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

def readfile(file,outroad,config):

    with open(file,'r') as F:
        for line in F:
            line=line.strip('\n')
            makefile(line,config,outroad)

def makefile(line,CONFIG,road):
    sample=os.path.basename(line)
    sample=sample.replace('vcf','')
    indir='{0}/result/{1}'.format(road,sample)
    os.system('mkdir -p '+indir)
    out='{0}/makefile.sh'.format(road+'/result')
    with open(out,'a+') as O:
        O.write('make -f /annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Work/GATK/ANNO_VCF/makefile/makefile_5_SNP indir={indir} gender=F CONFIG={con} vcf={vcf} realn=N SNP_INDEL_MT;'
                'make -f /annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Work/GATK/ANNO_VCF/makefile/makefile_6_ANNO indir={indir} CONFIG={con} style=MT ANNO_NEW;'
                'make -f /annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Work/GATK/ANNO_VCF/makefile/makefile_8_OR outdir={road} CONFIG={con} OR;\n'
                .format(indir=indir,con=CONFIG,vcf=line,road=road))



if __name__ == '__main__':
    #readfile(sys.argv[1],sys.argv[2],sys.argv[3])
    readfile('/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Out_result/Yuel_ANNO/B1283/list','/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Out_result/Yuel_ANNO/B1283'
             ,'/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/liting/Work/GATK/ANNO_VCF/config_leukemia_V3')
