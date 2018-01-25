#! /usr/bin/env python3
from Gene2Bed import cylGeneRegion
import os, sys, re


class gene2bed():
    def __init__(self, genefile, reffile, output):
        mybed = []
        self.output = output
        lines = open(genefile, 'r').readlines()
        for line in lines:
            line = line.strip()
            regions = cylGeneRegion.geneRegion(line, reffile)
            if regions.exists:
                for region in regions.infos:
                    if region[2] > 0:
                        cdss = region[4]
                        for cds in cdss:
                            if re.search(r'chr', cds[1]):
                                out = '{}\t{}\t{}'.format(cds[1], cds[2], cds[3])
                                mybed.append(out)
                                # print('exists:{}'.format(line))
                                # pass
            else:
                print('不存在这样的基因：{}'.format(line))
        self.bed = mybed

    def writeOut(self):
        f = open(self.output,'w')
        for line in self.bed:
            f.write(line)
            f.write('\n')
        f.close()


if __name__ == '__main__':
    test1 = gene2bed('/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/chenyl/tmp/genelist1_20170316',
                    '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia'
                    '/data/hougy/trans_python/pre/hg19_refGene.20170216.txt',
                    '/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/chenyl/tmp/tmp1.bed')
    test1.writeOut()

    test2 = gene2bed('/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/chenyl/tmp/genelist2_20170316',
                    '/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia'
                    '/data/hougy/trans_python/pre/hg19_refGene.20170216.txt',
                    '/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/chenyl/tmp/tmp2.bed')
    test2.writeOut()