#! /usr/bin/env python3

from Gene2Bed import hgyTrans
import os, sys
import re


class geneRegion():
    def detailInfo(self):
        mylist = []
        for i in self.ref_nm:
            refgene = hgyTrans.RefGene(i)
            mysub =[]
            mysub.append(refgene.geneName)
            mysub.append(refgene.nmId)
            mysub.append(refgene.returnCdsLen())
            mysub.append(refgene.returnAllExon())
            mysub.append(refgene.returnAllExonInCDS())
            mylist.append(mysub)
        return mylist

    def __init__(self, gene, hg_ref):
        self.exists = 0
        self.gene = gene
        # print(self.gene)
        # print(hg_ref)
        lines = open(hg_ref, 'r').readlines()
        self.ref_nm = []
        for i in lines:
            i = i.strip()
            cells = i.split('\t')
            # print('gene:'+cells[12])
            if cells[12] == self.gene:
                self.exists = 1
                self.ref_nm.append(i)
        self.infos = self.detailInfo()



if __name__ == '__main__':
    test = geneRegion('DNMT3A', '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/hougy/'
                                'trans_python/pre/hg19_refGene.20170216.txt').infos
    for i in test:
        # print(type(i))
        print(i[4])
        for j in i[4]:
            print(j[1])
            if re.search(r'chr', j[1]):
                out = '{}\t{}\t{}'.format(j[1], j[2], j[3])
                print(out)
