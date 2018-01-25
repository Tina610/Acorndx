import subprocess
import os
import re
import itertools


class mutationMerge:
    def __init__(self):
        self.listRawInput = {}
        self.listCandidate = {}
        self._sortedBam = None
        self._samtools = "/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/software/private/python2Lib/201test/mutationMerge/pre/samtools"
        self._selectDict = {}
        self._isHaplotypeDict = {}
        self._maxHaplotypeDict = {}

    def searchCandidate(self, maxLen=10):
        tmpDict = self.listRawInput
        class_i = 0
        for key in tmpDict:
            tmpDict[key].sort(key=lambda x: x[0])
            oldcell_p = None
            for cell in tmpDict[key]:
                if not oldcell_p:
                    pass
                else:
                    oldcell_p.append(cell[0] - oldcell_p[0])
                oldcell_p = cell
            oldcell_p.append(-1)

            for i in range(len(tmpDict[key])):
                if tmpDict[key][i][-1] == -1 or tmpDict[key][i][-1] >= maxLen:
                    class_i += 1
                elif tmpDict[key][i][-1] < -1:
                    raise Exception("error")
                elif tmpDict[key][i][-1] < maxLen:
                    if not str(class_i) in self.listCandidate:
                        self.listCandidate[str(class_i)] = []
                        self.listCandidate[str(class_i)].append([key] + tmpDict[key][i][:-1])
                        self.listCandidate[str(class_i)].append([key] + tmpDict[key][i + 1][:-1])
                    else:
                        self.listCandidate[str(class_i)].append([key] + tmpDict[key][i + 1][:-1])

    def inputVCFFormat(self, inFile):
        tmpDict = {}
        with open(inFile, 'r') as fr:
            for line in fr:
                if line[0] == '#':
                    continue
                cell = line.strip().split('\t')
                if not cell[0] in tmpDict:
                    tmpDict[cell[0]] = []
                tmpDict[cell[0]].append([int(cell[1]), cell[3], cell[4]])
        self.listRawInput = {}
        self.listRawInput = tmpDict

    def inputAnnoVarFormat(self, inFile):
        tmpDict = {}
        with open(inFile, 'r') as fr:
            headCell = fr.readline().strip().split("\t")
            mark = None
            for idx, value in enumerate(headCell):
                if value == "Otherinfo":
                    mark = idx
            if mark == None:
                raise Exception("Error:The target column was not found")

            for line in fr:
                if line[0] == '#':
                    continue
                cell = line.strip().split('\t')
                if not cell[mark] in tmpDict:
                    tmpDict[cell[mark]] = []
                tmpDict[cell[mark]].append([int(cell[mark + 1]), cell[mark + 3], cell[mark + 4]])
        self.listRawInput = {}
        self.listRawInput = tmpDict

    def appendAnnoVarFormat(self, inFile):
        with open(inFile, 'r') as fr:
            headCell = fr.readline().strip().split("\t")
            mark = None
            for idx, value in enumerate(headCell):
                if value == "Otherinfo":
                    mark = idx
            if mark == None:
                raise Exception("Error:The target column was not found")

            for line in fr:
                if line[0] == '#':
                    continue
                cell = line.strip().split('\t')
                if not cell[mark] in self.listRawInput:
                    self.listRawInput[cell[mark]] = []
                self.listRawInput[cell[mark]].append([int(cell[mark + 1]), cell[mark + 3], cell[mark + 4]])

    def appendCandidate(self,inputList):
        keyList = [int(i) for i in self.listCandidate.keys()]
        maxKey = 0
        if len(keyList) > 0:
            maxKey = max(keyList) + 1
        self.listCandidate[str(maxKey)] = inputList.copy()


    def inputSortedBam(self, inBamFile):
        self._sortedBam = inBamFile
        if not os.path.exists(self._sortedBam):
            raise Exception("no such file!")

    def showCandidate(self):
        for key in self.listCandidate:
            for cell in self.listCandidate[key]:
                print(key, cell)

    def returnCandidate(self):
        return self.listCandidate

    def runSelect(self):
        num=0
        chrpos=[]
        tmpList=[]
        commad = "/bin/echo -e \""  ##"/bin/echo -e \""
        for key in self.listCandidate:
            for cell in self.listCandidate[key]:
                commad += r"{} {}\n".format(cell[0], cell[1])  ##chr1 286111180
                if num==100:
                    commad += "\""  ##加个引号而已
                    chrpos.append(commad)
                    num=0
                    commad="/bin/echo -e \""
                else:
                    pass
                num+=1
        if 'chr' in commad:
            commad+="\""
            chrpos.append(commad)
        else:
            pass
        for cmd in chrpos:
            p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            #stdout,stderr=p1.communicate()
            cmd = "{} hgySelect {} -l -".format(self._samtools, self._sortedBam)
            p2 = subprocess.Popen(cmd, stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
            for line in p2.stdout:
                line = line.decode().strip()
                tmpList.append(line)

            p2.wait()
            if p2.poll() != 0:
                raise Exception("Error:hgySelect")

        loc = None
        for line in tmpList:
            cell = re.split(" |\t", line)
            if cell[0][0] == '#':
                loc = "{}:{}".format(cell[1], cell[2])
                if not loc in self._selectDict:
                    self._selectDict[loc] = []
            else:
                self._selectDict[loc].append(cell)

    def isHaplotype(self, num=3):
        for key in self.listCandidate:
            for cell in self.listCandidate[key]:
                loc = "{}:{}".format(cell[0], cell[1])
                refAlt = "{}:{}".format(cell[2], cell[3])
                nameSet = self.getNameSet(loc, refAlt)
                cell.append(nameSet)

            keyLen = len(self.listCandidate[key])
            for i in range(keyLen, 1, -1):
                for com in itertools.combinations(range(keyLen), i):
                    s = self.listCandidate[key][com[0]][-1]
                    for ii in range(1, len(com)):
                        s = s & self.listCandidate[key][com[ii]][-1]
                    if len(s) > num:
                        if not key in self._isHaplotypeDict:
                            self._isHaplotypeDict[key] = []
                        self._isHaplotypeDict[key].append([self.listCandidate[key][iii][:-1] for iii in com])
                    else:
                        pass

    def showHaplotype(self):
        for key in self._isHaplotypeDict:
            print("group {}".format(key))
            for cell in self._isHaplotypeDict[key]:
                print(cell)

    def showMaxHaplotype(self):
        for key in self._maxHaplotypeDict:
            print("group {}".format(key))
            for cell in self._maxHaplotypeDict[key]:
                print(cell)

    def returnHaplotype(self):
        return self._isHaplotypeDict

    def returnMaxHaplotype(self):
        return self._maxHaplotypeDict

    def getMaxHaplotype(self):
        reDist = {}
        for key in self._isHaplotypeDict:
            maxLen = 0
            for cell in self._isHaplotypeDict[key]:
                if len(cell) > maxLen:
                    maxLen = len(cell)

            for cell in self._isHaplotypeDict[key]:
                if len(cell) == maxLen:
                    if not key in reDist:
                        reDist[key] = []
                    reDist[key].append(cell)

        self._maxHaplotypeDict = reDist
        return reDist

    def getNameSet(self, tLoc, tRefAlt):
        if not self._selectDict:
            raise Exception("no self._selectDict")

        if not tLoc in self._selectDict:
            return set()

        ref, alt = tRefAlt.split(":")
        if len(ref) == 1 and len(alt) == 1:
            s = set()
            for cell in self._selectDict[tLoc]:
                if cell[0].upper().find(alt.upper()) != -1:
                    s.add(cell[2])
            return s
        elif len(ref) == 1 and len(alt) > 1:
            alt = "+{}{}".format(len(alt) - 1, alt[1:])
            s = set()
            for cell in self._selectDict[tLoc]:
                if cell[0].upper().find(alt.upper()) != -1:
                    s.add(cell[2])
            return s
        elif len(ref) > 1 and len(alt) == 1:
            altLen = len(ref) - 1
            alt = "-{}{}".format(altLen, 'N' * altLen)
            s = set()
            for cell in self._selectDict[tLoc]:
                if cell[0].upper().find(alt.upper()) != -1:
                    s.add(cell[2])
            return s
        else:
            raise Exception("Unknown variation type!")

    def inputWindowSize(self):
        pass


if __name__ == '__main__':
    # obj = mutationMerge()
    # # obj.inputVCFFormat("./pre/HD15AA01041-1-265.raw.vcf")
    # obj.inputAnnoVarFormat(
    #     "./pre/HD15AA01041-1-265-INDEL-Filter.vcf.hg19_multianno.txt"
    # )
    # obj.appendAnnoVarFormat(
    #     "./pre/HD15AA01041-1-265-SNP-Filter.vcf.hg19_multianno.txt"
    # )
    # obj.searchCandidate()
    # obj.appendCandidate([
    #     ['chr3', 128200119, 'GA', 'G'],
    #     ['chr3', 128200121, 'GT', 'G'],
    #     ['chr5', 128200127, 'GT', 'G']
    # ])
    # obj.appendCandidate([
    #     ['chr3', 128200119, 'GA', 'G'],
    #     ['chr3', 128200121, 'GT', 'G'],
    #     ['chr5', 128200127, 'GT', 'G']
    # ])
    # obj.showCandidate()
    # obj.inputSortedBam(
    #     "/annoroad/data1/bioinfo/PROJECT/RD/Medical/Leukemia/software/p"
    #     "rivate/python2Lib/201test/mutationMerge/pre/assembled.bam")
    # obj.runSelect()
    # obj.isHaplotype()
    # # obj.showHaplotype()
    # obj.getMaxHaplotype()
    # print("############")
    # obj.showHaplotype()
    # print("############")
    # obj.showMaxHaplotype()
    # reDict = obj.returnMaxHaplotype()
    # print(reDict)
    # print(obj.returnHaplotype())
    #
    #
    # # re = obj.returnCandidate()
    obj = mutationMerge()
    obj.inputAnnoVarFormat("/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial/HB_278_2017061110130325/result/HB15GL00379-1-117/Variant/SNP-INDEL_MT/ANNO/HB15GL00379-1-117-SNP-Filter.vcf.hg19_multianno.txt")
    obj.appendAnnoVarFormat("/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/Commercial/HB_278_2017061110130325/result/HB15GL00379-1-117/Variant/SNP-INDEL_MT/ANNO/HB15GL00379-1-117-INDEL-Filter.vcf.hg19_multianno.txt")
    obj.searchCandidate(maxLen=30)
    obj.showCandidate()
