#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 16:14
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : QHB_adapter.py
# @Software: PyCharm

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

def getfast(indir,outdir):
    qsub=outdir+'qsub.sh'
    qsh=outdir+'qsge.sh'
    Qsub=open(qsub,'w')
    Qsh=open(qsh,'w')
    dirs=os.listdir(indir)
    for dir in dirs:
        os.makedirs(outdir+'/'+dir,exist_ok=True)
        dirroad=os.path.join(outdir,dir)
        r1fq='{0}/{1}_R1.fq.gz'.format(dirroad,dir)
        r2fq='{0}/{1}_R2.fq.gz'.format(dirroad,dir)
        if os.path.isfile(r1fq):
            Qsub.write('/annoroad/share/software/install/cutadapt-1.2.1/bin/cutadapt -a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA -O 5  --info-file={dirroad}_R1.adapter.txt {fqgz} 1>/dev/null 2>/dev/null &&  gzip {dirroad}_R1.adapter.gz\n'
                       .format(dirroad=dirroad,fqgz=r1fq))
        if os.path.isfile(r2fq):
            Qsub.write('/annoroad/share/software/install/cutadapt-1.2.1/bin/cutadapt -a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA -O 5  --info-file={dirroad}_R2.adapter.txt {fqgz} 1>/dev/null 2>/dev/null &&  gzip {dirroad}_R2.adapter.gz\n'
                .format(dirroad=dirroad, fqgz=r2fq))
        Qsub.write('cp {0} {1}/'.format(r1fq,dirroad))
        Qsub.write('cp {0} {1}/'.format(r2fq,dirroad))
    Qsh.write('/annoroad/share/software/install/Python-3.3.2/bin/python3 /annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/bin/Leu_V3/Leu_V3.0.1_beta subscript/qsub_sge.py -m 30 -q cancer.q -re 'vf=10G' -nodu {0}'
    .format(Qsub))



if __name__ == '__main__':
    getfast(sys.argv[1],sys.argv[2])
