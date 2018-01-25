#! /usr/bin/env python3

import re
import xlrd


class mutClass():
    def __init__(self, file):
        self.classfile = file
        self.dict = {}
        self.dictline = {}
        self.titles = []

    def returnloc(self, tloc):
        tloclist = []
        if tloc == None:
            tloclist.append('._yes')
            return tloclist
        else:
            tloc = tloc.replace(r'(', '')
            tloc = tloc.replace(r')', '')
            tlocs = tloc.split(',')
            for tl in tlocs:
                tmps = tl.split('-')
                if len(tmps) == 1:
                    if 'e' in tl and not 'exon' in tl:
                        tt = tl.replace('e', '')
                        tloclist.append('{}_{}'.format(tt, 'not'))
                        tloclist.append('._yes')
                    else:
                        tloclist.append('{}_{}'.format(tl, 'yes'))

                else:
                    for i in range(int(tmps[0]), (int(tmps[1]) + 1)):
                        tloclist.append('{}_{}'.format(i, 'yes'))
        return tloclist

    def returntype(self, mg1):
        ttype = []
        if mg1 == 'nonsense':
            ttype.append('stopgain')
        elif mg1 == 'stoploss':
            ttype.append('stoploss')
        elif mg1 == 'frameshift':
            ttype.append('frameshift deletion')
            ttype.append('frameshift insertion')
            # ttype.append('nonframeshift deletion')
            # ttype.append('nonframeshift insertion')
        elif mg1 == 'splice site':
            ttype.append('splicing')
        elif mg1 == 'missense':
            ttype.append('nonsynonymous SNV')
        elif mg1 == 'nonframeshift':
            ttype.append('nonframeshift deletion')
            ttype.append('nonframeshift insertion')
            # ttype.append('frameshift deletion')
            # ttype.append('frameshift insertion')
        elif mg1 == 'FLT3-ITD':
            ttype.append('FLT3-ITD')
        else:
            print('Strange elements:{}'.format(mg1))
        return ttype

    def dictmake(self, ge, tpl, ll, ncl, nli):
        for tp in tpl:
            for tloc in ll:
                key = '{}_{}_{}_{}'.format(tp, ge, tloc, ncl)
                value = nli
                self.dict[key] = value

    def transInfo2dict(self, line, n_line):
        mutinfo = line[8].value
        gene = line[0].value
        infos = mutinfo.split(';')
        pattern = re.compile(r'([a-zA-Z- |\d]+)(\([\d,a-zA-Z-]+?\))?')
        # print(infos)
        for info in infos:
            # print(info)
            match = pattern.search(info)
            type = self.returntype(match.group(1))
            locallist = self.returnloc(match.group(2))
            for ncol in range(0, 8):
                cellValue = line[ncol].value
                # print('cellvalue:{}----{}'.format(cellValue,line[0].value))
                if cellValue == line[0].value:
                    # print(cellValue)
                    self.dictmake(gene, type, locallist, self.titles[ncol], n_line)

    def fileRead(self):
        workbook = xlrd.open_workbook(self.classfile)
        table = workbook.sheets()[0]
        nrows = table.nrows

        for i in range(0, 8):
            self.titles.append(str(table.cell(0, i).value))
        for row in range(1, nrows):
            mutId = str(table.cell(row, 9).value)
            if not mutId == '':
                self.dictline[row] = mutId
                # print(row)
                self.transInfo2dict(table.row(row), row)
            else:
                pass

    def returndicts(self):
        self.fileRead()
        return self.dict,self.dictline


if __name__ == '__main__':
    test = mutClass('C:\\Users\\acorndx_liting\\Desktop\\北大人民\\20180111test.xlsx')

    mydict1,mydict2 = test.returndicts()
    for i in mydict1:
        tmp = mydict1[i]
        print('key:{}----value:{}----line:{}'.format(i,tmp,mydict2[tmp]))


