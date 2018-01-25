#! /usr/bin/env python3

import os,sys
import subprocess
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--classification', '-c', help='Gene Mutation Class File', action='store',
                    dest='classf', default='/annoroad/data1/bioinfo/PROJECT/RD/Medical'
                                           '/Leukemia/V2_panel/test12_RERUN_20160120/chenyuelong'
                                           '/tmp/classfication.xlsx')
parser.add_argument('--samplelist', '-sl', help='SimpleSheet file with sample Class', action='store',
                    dest='samplel', default='/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia'
                                            '/V2_panel/test12_RERUN_20160120/chenyuelong/'
                                            'tmp/leu.xlsx')
parser.add_argument('--resultdir', '-rd', help='Result dir', action='store',
                    dest='resultdir', default='')
parser.add_argument('--output', '-o', help='output', action='store',
                    dest='out', default='/annoroad/data1/bioinfo/PROJECT/'
                                        'RD/Medical/Leukemia/V2_panel/test12_RERUN_20160120'
                                        '/chenyuelong/tmp/leu')
args = parser.parse_args()

python3='/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/chenyl/bin/python3'

def subpro(subargs):
    p = subprocess.Popen(subargs,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p

def generateArgs(python,bin,classfile,sampleClass,resultfile,out,tmpout,sample):
    myArgs = '{} {}/LeuMakeResult.py -c {} --samplelist {} --resultfile {} -o {} -ob {} -s {}'.\
        format(python,bin,classfile,sampleClass,resultfile,out,tmpout,sample)
    return myArgs

def generateRes(resultdir):
    dirs = glob.glob('{}/result/*/Variant/SNP-INDEL_MT/FILTER/*RESULT.xls'.format(resultdir))
    pathname = os.path.basename(resultdir)
    returnlist = []
    for eachdir in dirs:
        tmplist =[]
        tmpsample = os.path.basename(eachdir).split('-')[0]
        tmpdir = os.path.dirname(eachdir)
        tmplist.append(tmpsample)
        tmplist.append(eachdir)
        tmplist.append(tmpdir)
        returnlist.append(tmplist)
    return pathname,returnlist


def main():
    tmp ='/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemi' \
         'a/V2_panel/test12_RERUN_20160120/chenyuelong/tmp/leu'
    tmp1 = '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/' \
           'Leukemia/data/Commercial/HB_235_20170323113425'
    bin =sys.path[0]
    batch,batlist = generateRes(args.resultdir)
    piplist = []
    for eachbl in batlist:

        tmpargs = generateArgs(python3,bin,args.classf,args.samplel,
                               eachbl[1],args.out,eachbl[2],eachbl[0])
        p = subpro(tmpargs)
        piplist.append(p)

    return piplist


pmoinitor = main()
while pmoinitor.__len__()>0:
    print(len(pmoinitor))
    err,out=pmoinitor[0].communicate()
    print('err:{}\tout:{}'.format(err,out))
    del pmoinitor[0]

print('Job Finished!')



