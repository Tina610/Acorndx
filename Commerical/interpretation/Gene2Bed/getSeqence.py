#! /usr/bin/env python3

import os, sys
from Gene2Bed import hgyTrans


class pip():
    def __init__(self, loc):
        # print(loc)
        cells = loc.split('\t')
        self.chr = cells[0]
        self.loc = int(cells[1])
        self.up = '{}:{}-{}'.format(self.chr, (self.loc - 1000), self.loc)
        self.down = '{}:{}-{}'.format(self.chr, self.loc, (self.loc + 1000))
        self.seqUp = ''
        self.seqDown = ''

    def getseq(self):
        get1 = hgyTrans.GetSeq(self.up)
        self.seqUp = get1.returnSeq()
        get2 = hgyTrans.GetSeq(self.down)
        self.seqDown = get2.returnSeq()

    def returnSeq(self):
        self.getseq()
        # print(self.seqDown)
        return self.seqUp, self.seqDown


if __name__ == '__main__':
    test1 = pip('chr4\t55599321')
    seqs = test1.returnSeq()
    print('{}\t{}'.format(seqs[0], seqs[1]))
    test1 = pip('chr8\t117861196')
    seqs = test1.returnSeq()
    print('{}\t{}'.format(seqs[0], seqs[1]))
    test1 = pip('chr10\t112356214')
    seqs = test1.returnSeq()
    print('{}\t{}'.format(seqs[0], seqs[1]))
    # test1 = pip('chr4	106190861')
    # seqs = test1.returnSeq()
    # print('{}\t{}'.format(seqs[0], seqs[1]))
