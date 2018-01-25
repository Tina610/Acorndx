#! /usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys, re, os
from Leu_anno import annoFileDivid, extractFromFTP, mutClass, readSampleType
pathscript=os.path.realpath(__file__)
binp=os.path.dirname(pathscript)
#reload(sys)
#sys.setdefaultencoding('utf-8')
import subprocess
import argparse

linenumber = 1


def addi(string):
    if string == '.':
        return '.'
    elif string == 'FLT3-ITD':
        return r'FLT3-ITD'
    else:
        p = re.compile('N[A-Z]_\d+\((.+?)\)')
        pr = p.match(string)
        tmp = pr.group(1)
        string = string.replace(tmp, '<i>{}</i>'.format(tmp))
        return string


# if __name__ == '__main__':
#     print(addi('NM_005957(MTHFR):c.1305C>T(p.F435F)'))
#     print(addi('.'))


def listInDict(tlist, tdict):
    global linenumber
    for tl in tlist:
        if tl in tdict:
            # print(tl)
            # print (tdict[tl])
            linenumber = tdict[tl]
            return True
    return False


def writeFile(filepath, filelines, filetitle):
    with open(filepath, 'w') as f:
        if isinstance(filetitle,str):
            f.write(filetitle)
        else:
            f.write(filetitle.decode('utf-8'))
        f.write('\n')
        for i in filelines:
            if isinstance(i,str):
                f.write(i)
            else:
                f.write(i.decode('utf-8'))
            f.write('\n')


parser = argparse.ArgumentParser()
parser.add_argument('--classification', '-c', help='Gene Mutation Class File', action='store',
                    dest='classf', default='')
parser.add_argument('--samplelist', '-sl', help='SimpleSheet file with sample Class', action='store',
                    dest='samplel', default='')
parser.add_argument('--resultfile', '-rf', help='Result file', action='store',
                    dest='resultf', default='')
parser.add_argument('--sample', '-s', help='Sample ID', action='store',
                    dest='sam', default='')
parser.add_argument('--output', '-o', help='output', action='store',
                    dest='out', default='./result.out')
parser.add_argument('--outbak', '-ob', help='output bak', action='store',
                    dest='outbak', default='./result.out')

args = parser.parse_args()

if args.classf == '' or args.samplel == '' or args.resultf == '' or args.sam == '':
    print('Please input parameters: -c,-sl,-s,-rf')
    print('--help or -h for help!')
    sys.exit(0)

if not os.path.exists(args.out):
    os.makedirs(args.out,exist_ok=True)
if not os.path.exists(args.outbak):
    os.makedirs(args.outbak,exist_ok=True)
sample = args.sam
mc = mutClass.mutClass(args.classf)
linedict, labeldict = mc.returndicts()
rst = readSampleType.readSampleType(args.samplel)
samdict = rst.returndict()
isPositive = 'N'
classdict = {'AML': '1',
             'MDS': '2',
             'MPN': '3',
             'MDS/MPN': '4',
             'allgene': '5',
             'CML': '6',
             'ALL': '7',
             'CLL': '8'
             }

diseasedict = {'AML': '急性髓细胞白血病（AML）',
               'MDS': '骨髓增生异常综合征（MDS）',
               'MPN': '骨髓增殖性肿瘤（MPN）',
               'MDS/MPN': '骨髓增生异常综合征/骨髓增殖性肿瘤（MDS/MPN）',
               'allgene': '血液肿瘤综合性',
               'CML': '慢性粒细胞白血病（CML）',
               'ALL': '急性淋巴细胞白血病（ALL）',
               'CLL': '慢性淋巴细胞白血病（CLL）'
               }
samdict['ASHD15AA00502']='allgene'
if args.sam in samdict.keys():
    sampleType = samdict[args.sam]
else:
    sampleType = 'allgene'
# print(args.sam)
# print(sampleType)
st = sampleType
afd = annoFileDivid.annoFileDivid(args.resultf)
lines = afd.returnlines()
outputRes = []
outputInt = []
title = afd.returntitle()

for line in lines:
    st = sampleType
    linenumber = 1
    readgoing = 'needMore'
    cells = line.split('\t')
    exon = '/'
    percentage = '/'
    print(cells[16])
    if cells[0] == '.':
        readgoing = 'needMore'
    elif cells[16] == 'FLT3-ITD':
        percentage = cells[1]
        exon = 'Exon 13/14({})'.format(len(cells[14]))
        flag = '{}_{}_._yes_{}'.format(cells[16], cells[16], sampleType)
        flag111gene = '{}_{}_._yes_allgene'.format(cells[16], cells[16])
        if flag in linedict:
            readgoing = 'sample'
            linenumber = linedict[flag]
            isPositive = 'Y'
        elif flag111gene in linedict:
            st = 'allgene'
            readgoing = 'allgene'
            isPositive = 'Y'
            linenumber = linedict[flag111gene]
        else:
            readgoing = 'needMore'
        print('ITD')
    elif cells[15] == 'splicing':
        flag = '{}_{}_._yes_{}'.format(cells[15], cells[16], sampleType)
        flag111gene = '{}_{}_._yes_allgene'.format(cells[15], cells[16])
        percentage = cells[1]
        if flag in linedict:
            readgoing = 'sample'
            linenumber = linedict[flag]
            isPositive = 'Y'
        elif flag111gene in linedict:
            st = 'allgene'
            readgoing = 'allgene'
            isPositive = 'Y'
            linenumber = linedict[flag111gene]
        else:
            readgoing = 'needMore'
    else:
        nmp = re.compile('(NM_[\d]+)')
        nmId = nmp.search(cells[0]).group(1)
        mutp = re.compile('{}:(exon[\d]+):c\..+?:p\.(.*?([\d]+)[_A-Za-z]+?)'.format(nmId))
        mutpRes = mutp.search(cells[19])
        exon = mutpRes.group(1)
        percentage = cells[1]
        comHgvs = mutpRes.group(2)
        partHgvs = mutpRes.group(3)

        thislist = []
        alllist = []
        notthislist = []
        notalllist = []

        flag1 = '{}_{}_{}_yes_{}'.format(cells[18], cells[16], exon, sampleType)
        flag2 = '{}_{}_{}_yes_{}'.format(cells[18], cells[16], comHgvs, sampleType)
        flag3 = '{}_{}_{}_yes_{}'.format(cells[18], cells[16], partHgvs, sampleType)

        flag1d = '{}_{}_._yes_{}'.format(cells[18], cells[16], sampleType)
        flag2d = '{}_{}_._yes_{}'.format(cells[18], cells[16], sampleType)
        flag3d = '{}_{}_._yes_{}'.format(cells[18], cells[16], sampleType)

        thislist.append(flag1)
        thislist.append(flag2)
        thislist.append(flag3)
        thislist.append(flag1d)
        thislist.append(flag2d)
        thislist.append(flag3d)

        flag1all = '{}_{}_{}_yes_allgene'.format(cells[18], cells[16], exon)
        flag2all = '{}_{}_{}_yes_allgene'.format(cells[18], cells[16], comHgvs)
        flag3all = '{}_{}_{}_yes_allgene'.format(cells[18], cells[16], partHgvs)

        flag1dall = '{}_{}_._yes_allgene'.format(cells[18], cells[16])
        flag2dall = '{}_{}_._yes_allgene'.format(cells[18], cells[16])
        flag3dall = '{}_{}_._yes_allgene'.format(cells[18], cells[16])

        alllist.append(flag1all)
        alllist.append(flag2all)
        alllist.append(flag3all)
        alllist.append(flag1dall)
        alllist.append(flag2dall)
        alllist.append(flag3dall)

        flag1not = '{}_{}_{}_not_{}'.format(cells[18], cells[16], exon, sampleType)
        flag2not = '{}_{}_{}_not_{}'.format(cells[18], cells[16], comHgvs, sampleType)
        flag3not = '{}_{}_{}_not_{}'.format(cells[18], cells[16], partHgvs, sampleType)

        notthislist.append(flag1not)
        notthislist.append(flag2not)
        notthislist.append(flag3not)

        flag1allnot = '{}_{}_{}_not_allgene'.format(cells[18], cells[16], exon)
        flag2allnot = '{}_{}_{}_not_allgene'.format(cells[18], cells[16], comHgvs)
        flag3allnot = '{}_{}_{}_not_allgene'.format(cells[18], cells[16], partHgvs)

        notalllist.append(flag1not)
        notalllist.append(flag2not)
        notalllist.append(flag3not)

        if listInDict(thislist, linedict) and not listInDict(notthislist, linedict):
            readgoing = 'sample'
            isPositive = 'Y'
        elif listInDict(alllist, linedict) and not listInDict(notalllist, linedict):
            readgoing = 'allgene'
            # isPositive = 'Y'
            st = 'allgene'
        elif listInDict(notthislist, linedict):
            readgoing = ''
        elif listInDict(notalllist, linedict):
            readgoing = ''
        else:
            readgoing = 'needMore'
    # print(linenumber)
    exon = exon.replace('exon','Exon ')
    tmpout ="{}\t{}\t{}\t{}\t{}" \
        .format(addi(cells[0]), exon, percentage, diseasedict[st], labeldict[linenumber])

    if readgoing == 'needMore':
        outputInt.append(line)
    elif readgoing == 'sample':
        outputRes.append(tmpout)
    elif readgoing == 'allgene':
        outputRes.append(tmpout)
    else:
        print('不要{}'.format(line))
fileleu='{}/{}-{}-{}.txt'.format(args.out, sample, classdict[sampleType], isPositive)
fileext='{}/{}-待解读.txt'.format(args.outbak, sample)
leutitle=u"rs号或HGVS\\t外显子\\t突变频率\\t疾病\\t突变类号"
subprocess.Popen("/annoroad/data1/bioinfo/PMO/chenyuelong/bin/perl {0}/LeuResult.pl {1} {2} {3}".format(binp,fileleu,leutitle,outputRes),stdout=subprocess.PIPE,shell=True)

#writeFile('{}/{}-{}-{}.txt'.format(args.out, sample, classdict[sampleType], isPositive),
#          outputRes,
#          u'rs号或HGVS\t外显子\t突变频率\t疾病\t突变类号')
#writeFile('{}/{}-待解读.txt'.format(args.outbak, sample), outputInt,
#          title
#          )
