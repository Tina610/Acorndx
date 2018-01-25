#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 15:59
# @Author  : liting
# @Mail    : tingli@annoroad.com
# @File    : pathway_dela.py
# @Software: PyCharm

import os, sys
import pandas as pd
from
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))



matrix=pd.read_table('matrix4Hist.txt',header=0)
del matrix['num']
clin=pd.read_table('clin_1',header=0)
prefix=matrix[['gene','pathway']]
#print(matrix)
sample_gt60=clin[(clin['aged']>60) |  (clin['aged']==60)]['sample']
sample_gt60=matrix[sample_gt60]
sample_gt60['num']=sample_gt60.apply(sum,axis=1)
sample_gt60=pd.concat([prefix,sample_gt60],axis=1)
sample_lt60=clin[(clin['aged']<60)]['sample']
sample_gt60['num']=sample_gt60.apply(sum,axis=1)
sample_lt60=matrix[sample_lt60]
#print(sample_gt60)
#print(prefix)
sample_gt60=pd.concat()
sample_lt60=pd.concat([prefix,sample_lt60],axis=1)

def main():
    pass


if __name__ == '__main__':
    main()
