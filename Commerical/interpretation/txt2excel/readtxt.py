#! /usr/bin/env python3

import os,sys
import re

class readtxt():
    def __init__(self,file,sep='\t'):
        self.txtfile = file
        self.sep=sep

    def readfile(self):
        self.lines = open(self.txtfile,'r').readlines()
        return self.lines

    def returnsep(self):
        return self.sep


if __name__ == '__main__':
    test = readtxt('HB15GL00231-1-36-SNP.txt')
    lines = test.readfile()
    for line in lines:
        print(line)