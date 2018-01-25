#! /usr/bin/env python3

import argparse
import sys
from txt2excel import trans2excel

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='dir or file path', action='store',
                    dest='input', default='')
parser.add_argument('--output', '-o', help='output', action='store',
                    dest='out', default='')
args = parser.parse_args()
if args.input == '' or args.out == '':
    print(parser.parse_args(['-h']))
    sys.exit(0)

def main():
    t2e = trans2excel.trans2excel(args.input,args.out)
    t2e.generateExcel()

if __name__ == '__main__':
    main()





