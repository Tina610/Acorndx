#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/7/10 14:43
# @Author  : liting
# @Mail    : liting@annoroad.com
# @Site    :
# @File    : Merge2Result.py
# @Software: PyCharm
from mutationMerge import mutationMerge as Merge
import glob
import sys
import os
import re
from multiprocessing import Pool
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
def multiRun(fun, parameters):
    pool = Pool(50)
    results = pool.map(fun, parameters)
    pool.close()
    pool.join()
    # return results
def filter(dirs):
    direct=[]
    for dir in dirs:
        if re.findall("(out)|(PTD)|(sh)", dir):
            continue
        else:
            direct.append(dir)
    return direct
def getdir(dir):
    sample = os.path.basename(dir)
    assembam = '{0}/Alignment/{1}.assemble.bam'.format(dir, sample)
    rawvcf = '{0}/Variant/SNP-INDEL_MT/{1}.raw.vcf'.format(dir, sample)
    result = '{0}/Variant/SNP-INDEL_MT/FILTER/{1}-RESULT.xls'.format(dir, sample)
    mydict = merge(rawvcf, assembam)
    nmsdict = {}
    with open(result, 'r+') as Fr:
        temp = Fr.readline()
        for line in Fr:
            line = line.strip('\n').split('\t')
            nms = line[0]
            if re.search("^NM_\d+", nms):
                try:
                    per = line[1]
                    per = per.replace('%','')
                    logo = [line[65], int(line[66]), line[68], line[69]]
                except Exception as err:
                    print('{0}-{1}-{2}'.format(err,line,result))
                # print(logo)
                for keys in mydict:
                    for cells in mydict[keys]:
                        if logo in cells:
                            if not keys in nmsdict:
                                nmsdict[keys] = []
                                nmsdict[keys].append([nms,per])
                            else:
                                nmsdict[keys].append([nms,per])
                        else:
                            pass
            else:
                pass
        if nmsdict:
            Fr.write('Here are the Mutation that can be Merged(Please reference)\n')
            for group in nmsdict:
                if len(nmsdict[group])>1:
                    #print(nmsdict[group])
                    minusL=[]
                    oldcell=None
                    for cell in nmsdict[group]:
                        if not oldcell:
                            pass
                        else:
                            minus=abs(float(cell[1])-oldcell)
                            minusL.append(minus)
                        oldcell=float(cell[1])
                    if max(minusL)>5:
                        continue
                # if len(nmsdict[group])==1:
                #     continue
                # else:
                # print('{0}\n{1}\n'.format(mydict[group], nmsdict[group]))
                Fr.write('{0}\n{1}\n'.format(nmsdict[group], mydict[group]))
        else:
            pass

def merge(vcf,bam):
    obj = Merge()
    obj.inputVCFFormat(vcf)
    obj.inputSortedBam(bam)
    obj.searchCandidate(maxLen=20)
    obj.runSelect()
    obj.isHaplotype()
    obj.getMaxHaplotype()
    return obj.returnMaxHaplotype()

def main(indir):
    dirs= glob.glob(indir + '/*')
    direct=filter(dirs)
    multiRun(getdir, direct)
if __name__ == '__main__':
    main(sys.argv[1])
