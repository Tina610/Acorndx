#coding=utf8
from abc import ABCMeta, abstractmethod
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Seq import translate
import os
import re


class assistant:
    @classmethod
    def getIdx(cls,faFilePath='/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/data/hougy/trans_python/pre/ucsc.hg19.fasta'):
        idxFilePath = faFilePath + '.idx'
        return SeqIO.index_db(idxFilePath, faFilePath, 'fasta')

    @classmethod
    def getSeq(cls,loc="chr1:0-1"):
        myChrom,myStart,myEnd = re.split(':|-',loc)
        bedtools = "/annoroad/share/software/install/bedtools2-2.20.1/bin/bedtools"
        fasta = "/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/database/Leu/hg19_GATK/ucsc.hg19.fasta"
        cmd = "echo -e \"{}\\t{}\\t{}\" | {} getfasta -fi {} -bed - -fo -".format(myChrom,myStart,myEnd,bedtools,fasta)
        reseq = ""
        fr = os.popen(cmd)
        reseq = fr.readlines()[1].strip()
        fr.close()
        return reseq.upper()


class GetSeq():
    def __init__(self,loc):
        self.loc = loc
        self.getSeq()

    def getSeq(self):
        myChrom, myStart, myEnd = re.split(':|-', self.loc)
        bedtools = "/annoroad/share/software/install/bedtools2-2.20.1/bin/bedtools"
        fasta = "/annoroad/data1/bioinfo/PROJECT/Commercial/Medical/Leukemia/database/Leu/hg19_GATK/ucsc.hg19.fasta"
        cmd = "echo -e \"{}\\t{}\\t{}\" | {} getfasta -fi {} -bed - -fo -".format(myChrom, myStart, myEnd, bedtools,fasta)
        seqStr = ""
        fr = os.popen(cmd)
        seqStr = fr.readlines()[1].strip().upper()
        fr.close()
        self.seq = Seq(seqStr)

    def returnSeq(self):
        return self.seq

    def returnSeqRev(self):
        return self.seq.reverse_complement()

    def returnAA(self):
        return self.seq.translate()

    def returnRevAA(self):
        return self.seq.reverse_complement().translate()

class RefGene():
    def __init__(self,strRef):
        cell = strRef.split('\t')
        self.nmId = cell[1]
        self.chromo = cell[2]
        self.zf = cell[3]
        self.txStart = cell[4]
        self.txEnd = cell[5]
        self.cdsStart = cell[6]
        self.cdsEnd = cell[7]
        self.exonNum = cell[8]
        self.geneName = cell[12]
        self.exonLoc1 = cell[9].strip(',').split(',')
        self.exonLoc2 = cell[10].strip(',').split(',')
        self.exonFrames = cell[14].strip(',').split(',')
        self.cdsStartExonNum = self.returnCdsStartExon()
        self.cdsList = self.initCdsList()

    def returnCdsStartExon(self):
        tmpre = 0
        if self.zf == '+':
            for i in self.exonFrames:
                tmpre += 1
                if i != '-1':
                    return tmpre
        elif self.zf == '-':
            for i in self.exonFrames[::-1]:
                tmpre += 1
                if i != '-1':
                    return tmpre
        else:
            return 0

    def initCdsList(self):
        reList = []
        if self.zf == '+':
            cLoc = int(0)
            pLoc = int(0)
            cdsStart = int(self.cdsStart)
            cdsEnd = int(self.cdsEnd)
            for j in range(int(self.exonNum)):
                for i in range(int(self.exonLoc1[j]),int(self.exonLoc2[j])):
                    if i >= cdsStart and i < cdsEnd:
                        cLoc += 1
                        pLoc = int((cLoc-1)/3) + 1
                        reList.append([cLoc,pLoc,i,(j+1)])
        if self.zf == '-':
            cLoc = int(0)
            pLoc = int(0)
            cdsStart = int(self.cdsEnd)
            cdsEnd = int(self.cdsStart)
            #print cdsStart,cdsEnd
            #print GetSeq("{}:{}-{}".format(self.chromo,cdsStart-3,cdsStart)).returnSeqRev()
            for j in range(int(self.exonNum))[::-1]:
                #print self.exonLoc1[j],self.exonLoc2[j]
                for i in range(int(self.exonLoc1[j]), int(self.exonLoc2[j]))[::-1]:
                    if i >= cdsEnd and i < cdsStart:
                        cLoc += 1
                        pLoc = int((cLoc-1)/3) + 1
                        reList.append([cLoc, pLoc, i, (int(self.exonNum) - j)])

        return reList

    def returnCLoc(self,inputStr):
        p = re.compile('c.([AGCT])(\d+?)([AGCT])')
        m = p.search(inputStr)
        myRef = m.group(1)
        myLoc = int(m.group(2))
        myAlt = m.group(3)

        reList = []
        reList.append(self.chromo)
        myCLocList = []
        myPLocList = []
        myGLocList = []
        myExonList = []
        realRef = "NA"
        for line in self.cdsList:
            if line[0] == myLoc:
                realRef = str(GetSeq("{}:{}-{}".format(self.chromo, line[2], line[2] + 1)).returnSeq())
                myCLocList.append(line[0])
                myPLocList.append(line[1])
                myGLocList.append(line[2])
                myExonList.append(line[3])
                break

        reList.append(myCLocList)
        reList.append(myPLocList)
        reList.append(myGLocList)
        reList.append(myExonList)

        if self.zf == '-':
            myRef = str(Seq(myRef).reverse_complement())

        reList = reList + [myRef,realRef]

        if myRef == realRef:
            reList.append(1)
        else:
            reList.append(0)

        return reList

    def returnPLoc(self, inputStr):
        p = re.compile('p.([A-Z])(\d+?)([A-Z])')
        m = p.search(inputStr)
        myRef = m.group(1)
        myLoc = int(m.group(2))
        myAlt = m.group(3)
        myDnaSeq = ""
        myDnaLoc = []
        myCLoc = []
        myPloc = []
        myExonList = []
        reList = []
        reList.append(self.chromo)
        for line in self.cdsList:
            if line[1] == myLoc:
                if self.zf == '-':
                    myDnaSeq += str(GetSeq("{}:{}-{}".format(self.chromo,line[2],line[2] + 1)).returnSeqRev())
                elif self.zf == '+':
                    myDnaSeq += str(GetSeq("{}:{}-{}".format(self.chromo, line[2], line[2] + 1)).returnSeq())

                myDnaLoc.append(line[2])
                myCLoc.append(line[0])
                myPloc.append(line[1])
                myExonList.append(line[3])
        if myDnaSeq:
            myRealAA = translate(myDnaSeq)
        else:
            myRealAA = "NA"

        reList.append(myCLoc)
        reList.append(myPloc)
        reList.append(myDnaLoc)
        reList.append(myExonList)
        reList.append(myRef)
        reList.append(myRealAA)
        if myRef == myRealAA:
            reList.append(1)
        else:
            reList.append(0)
        return reList

    def returnExon(self,inputStr):
        if re.search('^exon(\d+)$',inputStr):
            exonNum = int(re.search('^exon(\d+)$',inputStr).group(1))
            if exonNum > int(self.exonNum):
                return ["NA","NA","NA"]

            if self.zf == '+':
                return [self.chromo,self.exonLoc1[exonNum-1],self.exonLoc2[exonNum-1]]
                #return "{}:{}-{}".format(self.chromo,self.exonLoc1[exonNum-1],self.exonLoc2[exonNum-1])
            elif self.zf == '-':
                return [self.chromo,self.exonLoc1[-exonNum], self.exonLoc2[-exonNum]]
                #return "{}:{}-{}".format(self.chromo,self.exonLoc1[-exonNum], self.exonLoc2[-exonNum])

    def returnExonInCDS(self,inputStr):
        tList = self.returnExon(inputStr)

        if tList[0] == 'NA':
            return tList

        if int(self.cdsStart) == int(self.cdsEnd):
            return ["NA", "NA", "NA"]

        if int(tList[1]) >= int(self.cdsStart) and int(tList[2]) <= int(self.cdsEnd):
            return tList

        if int(tList[1]) <= int(self.cdsStart) and int(tList[2]) >= int(self.cdsEnd):
            return  [tList[0],self.cdsStart,self.cdsEnd]

        if int(self.cdsStart) >= int(tList[1]) and int(self.cdsStart) <= int(tList[2]):
            return [tList[0],self.cdsStart,tList[2]]

        if int(self.cdsEnd) >= int(tList[1]) and int(self.cdsEnd) <= int(tList[2]):
            return [tList[0],tList[1],self.cdsEnd]

        return ["NA","NA","NA"]


    def returnAllExon(self):
        reList = []
        for i in range(int(self.exonNum)):
            reList.append([i + 1] + self.returnExon("exon{}".format(i + 1)))
            #reList.append("{}|{}".format(i+1,self.returnExon("exon{}".format(i))))

        return reList

    def returnAllExonInCDS(self):
        reList = []
        for i in range(int(self.exonNum)):
            reList.append([i + 1] + self.returnExonInCDS("exon{}".format(i + 1)))

        return reList

    def returnIntron(self,inputStr):
        if re.search('^intron(\d+)$',inputStr):
            intronNum = int(re.search('^intron(\d+)$',inputStr).group(1))
            if intronNum > (int(self.exonNum) - 1):
                return ["NA","NA","NA"]

            if self.zf == '+':
                return [self.chromo,self.exonLoc2[intronNum - 1],self.exonLoc1[intronNum]]
            if self.zf == '-':
                return [self.chromo,self.exonLoc2[-intronNum - 1],self.exonLoc1[-intronNum]]

    def returnAllIntron(self):
        reList = []
        for i in range(int(self.exonNum) - 1):
            reList.append([i + 1] + self.returnIntron("intron{}".format(i + 1)))
            #reList.append("{}|{}".format(i+1,self.returnExon("exon{}".format(i))))

        return reList


    def returnNmInfo(self):
        exonTotalLen = 0

        for i in range(int(self.exonNum)):
            exonTotalLen += int(self.exonLoc2[i]) - int(self.exonLoc1[i])

        return [self.nmId,exonTotalLen,self.exonNum,self.geneName]

    def returnCdsLen(self):
        totalLen = 0

        tList = self.returnAllExonInCDS()
        for cell in tList:
            if not cell[1] == "NA":
                totalLen = totalLen + (int(cell[3]) - int(cell[2]))

        return totalLen

    def getStartCodon(self):
        loc = ""
        if self.zf == '+':
            loc = "{}:{}-{}".format(self.chromo, self.cdsStart,(int(self.cdsStart) + 3))
            p = GetSeq(loc)
            return p.returnSeq()
        elif self.zf == '-':
            loc = "{}:{}-{}".format(self.chromo, (int(self.cdsEnd) - 3), self.cdsEnd)
            p = GetSeq(loc)
            return p.returnSeqRev()

    def getStopCodon(self):
        loc = ""
        if self.zf == '+':
            loc = "{}:{}-{}".format(self.chromo, (int(self.cdsEnd) - 3),self.cdsEnd)
            p = GetSeq(loc)
            return p.returnSeq()
        elif self.zf == '-':
            loc = "{}:{}-{}".format(self.chromo, self.cdsStart, (int(self.cdsStart) + 3))
            p = GetSeq(loc)
            return p.returnSeqRev()

    def checkStartStopCodon(self):
        flag = 1
        if self.getStartCodon() != 'ATG':
            flag = 0

        if self.getStopCodon() not in ['TAG','TAA','TGA']:
            flag = 0

        if flag:
            return 1








if __name__ == '__main__':
    refGene = RefGene("97	NM_175629	chr2	-	25455829	25565459	25457147	25536853	23	25455829,25458575,25459804,25461998,25463170,25463508,25464430,25466766,25467023,25467408,25468121,25468888,25469028,25469488,25469919,25470459,25470905,25497809,25498368,25505309,25523007,25536781,25565298,	25457289,25458694,25459874,25462084,25463319,25463599,25464576,25466851,25467207,25467521,25468201,25468933,25469178,25469645,25470027,25470618,25471121,25497956,25498412,25505580,25523112,25537030,25565459,	0	DNMT3A	cmpl	cmpl  2,0,2,0,1,0,1,0,2,0,1,1,1,0,0,0,0,0,1,0,0,0,-1,")
    print(refGene.exonLoc1)
    print(refGene.exonLoc2)
    print(refGene.returnCLoc("c.G3707C"))
    print(refGene.returnCLoc("c.G1707C"))
    print("##",refGene.returnCLoc("c.C1707C"))
    print(refGene.returnPLoc("p.P2569P"))
    print(refGene.returnPLoc("p.P569P"))
    print("##",refGene.returnPLoc("p.X569P"))
    print(refGene.returnExon("exon1"))
    print("CDS:", refGene.cdsStart,refGene.cdsEnd)
    print("CDS:",refGene.returnExonInCDS("exon1"))
    print("CDS:", refGene.returnExonInCDS("exon2"))
    print("CDS:", refGene.returnExonInCDS("exon3"))
    print(refGene.returnExon("exon23"))
    print(refGene.returnExon("exon24"))
    print(refGene.returnIntron("intron1"))
    print(refGene.returnIntron("intron23"))
    print(refGene.returnNmInfo())
    print(refGene.returnAllExon())
    print(refGene.returnAllExonInCDS())
    print(refGene.returnAllIntron())
    print("#####################################################################################")

    refGene = RefGene("1888	NM_002520	chr5	+	170814707	170837888	170814952	170837569	11	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170827842,170832305,170834703,170837530,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170827929,170832407,170834778,170837888,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,0,")
    print(refGene.exonLoc1)
    print(refGene.exonLoc2)
    print(refGene.returnCLoc("c.C2865T"))
    print(refGene.returnCLoc("c.C865T"))
    print(refGene.returnPLoc("p.Q2289X"))
    print(refGene.returnPLoc("p.Q289X"))
    print(refGene.returnExon("exon1"))
    print(refGene.returnExon("exon11"))
    print(refGene.returnExon("exon12"))
    print(refGene.returnIntron("intron1"))
    print(refGene.returnIntron("intron11"))
    print(refGene.returnNmInfo())
    print(refGene.returnAllExon())
    print(refGene.returnAllExonInCDS())
    print(refGene.returnAllIntron())
    print("NPM1_CDS",refGene.returnCdsLen())
    print("#####################################################################################")

    refGene = RefGene("1888	NM_002520	chr5	+	170814707	170837888	170814952	170837569	11	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170827842,170832305,170834703,170837530,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170827929,170832407,170834778,170837888,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,0,")
    print(refGene.returnCLoc("c.C959T"))
    refGene = RefGene(
        "1888	NM_001037738	chr5	+	170814707	170833731	170814952	170833409	10	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170827842,170832305,170833400,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170827929,170832407,170833731,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,")
    print(refGene.returnCLoc("c.C959T"))
    refGene = RefGene(
        "1888	NM_199185	chr5	+	170814707	170837888	170814952	170837569	10	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170832305,170834703,170837530,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170832407,170834778,170837888,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,")
    print(refGene.returnCLoc("c.C959T"))

    print("#####################################################################################")

    refGene = RefGene(
        "176	NM_000051	chr11	+	108093558	108239826	108098351	108236235	63	108093558,108098321,108098502,108099904,108106396,108114679,108115514,108117690,108119659,108121427,108122563,108123543,108124540,108126941,108128207,108129712,108137897,108139136,108141790,108141977,108143258,108143448,108150217,108151721,108153436,108154953,108158326,108159703,108160328,108163345,108164039,108165653,108168013,108170440,108172374,108173579,108175401,108178623,108180886,108183137,108186549,108186737,108188099,108190680,108192027,108196036,108196784,108198371,108199747,108200940,108202170,108202605,108203488,108204612,108205695,108206571,108213948,108216469,108218005,108224492,108225537,108235808,108236051,	108093913,108098423,108098615,108100050,108106561,108114845,108115753,108117854,108119829,108121799,108122758,108123639,108124766,108127067,108128333,108129802,108138069,108139336,108141873,108142133,108143334,108143579,108150335,108151895,108153606,108155200,108158442,108159830,108160528,108163520,108164204,108165786,108168109,108170612,108172516,108173756,108175579,108178711,108181042,108183225,108186638,108186840,108188248,108190785,108192147,108196271,108196952,108198485,108199965,108201148,108202284,108202764,108203627,108204695,108205836,108206688,108214098,108216635,108218092,108224607,108225601,108235945,108239826,	0	ATM	cmpl	cmpl	-1,0,0,2,1,1,2,1,0,2,2,2,2,0,0,0,0,1,0,2,2,0,2,0,0,2,0,2,0,2,0,0,1,1,2,0,0,1,2,2,0,2,0,2,2,2,0,0,0,2,0,0,0,1,0,0,0,0,1,1,2,0,2,")
    print(refGene.returnPLoc("p.S1054T"))
    print(refGene.returnCdsLen())

    print("#####################################################################################")

    refGene = RefGene(
        "21	NM_001134373	chr10	-	104847773	104953063	104849428	104934715	18	104847773,104850367,104850692,104851320,104852895,104853728,104854104,104855695,104857047,104858687,104859682,104860801,104860991,104865462,104866345,104899162,104934614,104952992,	104849665,104850544,104850753,104851372,104853066,104853795,104854212,104855737,104857131,104858741,104859776,104860859,104861083,104865558,104866463,104899236,104934739,104953063,	0	NT5C2	cmpl	cmpl	0,0,2,1,1,0,0,0,0,0,2,1,2,2,1,2,0,-1,")
    print("NT5C2",refGene.returnExonInCDS("exon11"))

    print("#####################################################################################")

    refGene = RefGene(
        "176	NM_000051	chr11	+	108093558	108239826	108098351	108236235	63	108093558,108098321,108098502,108099904,108106396,108114679,108115514,108117690,108119659,108121427,108122563,108123543,108124540,108126941,108128207,108129712,108137897,108139136,108141790,108141977,108143258,108143448,108150217,108151721,108153436,108154953,108158326,108159703,108160328,108163345,108164039,108165653,108168013,108170440,108172374,108173579,108175401,108178623,108180886,108183137,108186549,108186737,108188099,108190680,108192027,108196036,108196784,108198371,108199747,108200940,108202170,108202605,108203488,108204612,108205695,108206571,108213948,108216469,108218005,108224492,108225537,108235808,108236051,	108093913,108098423,108098615,108100050,108106561,108114845,108115753,108117854,108119829,108121799,108122758,108123639,108124766,108127067,108128333,108129802,108138069,108139336,108141873,108142133,108143334,108143579,108150335,108151895,108153606,108155200,108158442,108159830,108160528,108163520,108164204,108165786,108168109,108170612,108172516,108173756,108175579,108178711,108181042,108183225,108186638,108186840,108188248,108190785,108192147,108196271,108196952,108198485,108199965,108201148,108202284,108202764,108203627,108204695,108205836,108206688,108214098,108216635,108218092,108224607,108225601,108235945,108239826,	0	ATM	cmpl	cmpl	-1,0,0,2,1,1,2,1,0,2,2,2,2,0,0,0,0,1,0,2,2,0,2,0,0,2,0,2,0,2,0,0,1,1,2,0,0,1,2,2,0,2,0,2,2,2,0,0,0,2,0,0,0,1,0,0,0,0,1,1,2,0,2,")
    print("ATM", refGene.returnCLoc("c.C7636T"))
    print("ATM CDS",refGene.returnCdsLen())

    print("RUNX1#####################################################################################")

    refGene = RefGene(
        "107	NM_001754	chr21	-	36160097	36421595	36164431	36421196	9	36160097,36171597,36206706,36231770,36252853,36259139,36265221,36421138,36421464,	36164907,36171759,36206898,36231875,36253010,36259393,36265260,36421255,36421595,	RUNX1	cmpl	cmpl	1,1,1,1,0,1,1,0,-1,")
    print("RUNX1", refGene.returnCdsLen())
    refGene = RefGene(
        "107	NM_001001890	chr21	-	36160097	36260987	36164431	36259409	6	36160097,36171597,36206706,36231770,36252853,36259139,	36164907,36171759,36206898,36231875,36253010,36260987,	0	RUNX1	cmpl	cmpl	1,1,1,1,0,0,")
    print("RUNX1", refGene.returnCdsLen())
    refGene = RefGene(
        "861	NM_001122607	chr21	-	36193573	36260987	36193964	36259409	5	36193573,36206706,36231770,36252853,36259139,	36193993,36206898,36231875,36253010,36260987,	0	RUNX1	cmpl	cmpl	1,1,1,0,0,")
    print("RUNX1", refGene.returnCdsLen())

    print("CBL#####################################################################################")

    refGene = RefGene(
        "186	NM_005188	chr11	+	119076985	119178859	119077127	119170491	16	119076985,119103157,119142444,119144577,119145541,119146706,119148466,119148875,119149219,119155678,119155898,119158561,119167627,119168093,119169067,119170204,	119077322,119103405,119142591,119144734,119145663,119146844,119148554,119149007,119149423,119155810,119156276,119158656,119167744,119168191,119169250,119178859,	0	CBL	cmpl	cmpl	0,0,2,2,0,2,2,0,0,0,0,0,2,2,1,1,")
    print("CBL", refGene.returnCdsLen())

    print("PTEN#####################################################################################")

    refGene = RefGene(
        "158	NM_001304717	chr10	+	89623194	89731687	89623706	89725229	10	89623194,89623861,89653781,89685269,89690802,89692769,89711874,89717609,89720650,89725043,	89623860,89624305,89653866,89685314,89690846,89693008,89712016,89717776,89720875,89731687,	0	PTEN	cmpl	cmpl	0,1,1,2,2,1,0,1,0,0,")
    print("PTEN", refGene.returnCdsLen())

    print("MAP2K4#####################################################################################")

    refGene = RefGene(
        "84	NM_001281435	chr17	+	11924134	12047148	11924203	12044577	12	11924134,11935582,11958205,11984672,11998891,12011106,12013691,12016549,12028610,12032455,12043155,12044463,	11924318,11935615,11958308,11984847,11999011,12011226,12013743,12016677,12028688,12032604,12043201,12047148,	0	MAP2K4	cmpl	cmpl	0,1,1,2,0,0,0,1,0,0,2,0,")
    print("MAP2K4", refGene.returnCdsLen())

    print("DNMT3A#####################################################################################")

    refGene = RefGene(
        "97	NM_175629	chr2	-	25455829	25565459	25457147	25536853	23	25455829,25458575,25459804,25461998,25463170,25463508,25464430,25466766,25467023,25467408,25468121,25468888,25469028,25469488,25469919,25470459,25470905,25497809,25498368,25505309,25523007,25536781,25565298,	25457289,25458694,25459874,25462084,25463319,25463599,25464576,25466851,25467207,25467521,25468201,25468933,25469178,25469645,25470027,25470618,25471121,25497956,25498412,25505580,25523112,25537030,25565459,	0	DNMT3A	cmpl	cmpl  2,0,2,0,1,0,1,0,2,0,1,1,1,0,0,0,0,0,1,0,0,0,-1,")
    print("DNMT3A", refGene.returnPLoc("p.S803T"))

    print("FLT3#####################################################################################")

    refGene = RefGene(
        "803	NM_004119	chr13	-	28577410	28674729	28578188	28674647	24	28577410,28588588,28589293,28589726,28592603,28597486,28598997,28601224,28602314,28608023,28608218,28608437,28609631,28610071,28611321,28622411,28623520,28623771,28624231,28626681,28631483,28636003,28644627,28674604,	28578311,28588694,28589393,28589838,28592726,28597614,28599080,28601378,28602425,28608128,28608351,28608544,28609810,28610180,28611425,28622580,28623674,28623911,28624359,28626811,28631599,28636206,28644749,28674729,	0	FLT3  cmpl	cmpl	0,2,1,0,0,1,2,1,1,1,0,1,2,1,2,1,0,1,2,1,2,0,1,0,")
    print("FLT3", refGene.returnIntron("intron14"))
    refGene = RefGene(
        "803	NM_004119	chr13	-	28577410	28674729	28578188	28674647	24	28577410,28588588,28589293,28589726,28592603,28597486,28598997,28601224,28602314,28608023,28608218,28608437,28609631,28610071,28611321,28622411,28623520,28623771,28624231,28626681,28631483,28636003,28644627,28674604,	28578311,28588694,28589393,28589838,28592726,28597614,28599080,28601378,28602425,28608128,28608351,28608544,28609810,28610180,28611425,28622580,28623674,28623911,28624359,28626811,28631599,28636206,28644749,28674729,	0	FLT3  cmpl	cmpl	0,2,1,0,0,1,2,1,1,1,0,1,2,1,2,1,0,1,2,1,2,0,1,0,")
    print("FLT3", refGene.returnIntron("intron15"))

    print("NPM1#####################################################################################")

    refGene = RefGene(
        "1888	NM_002520	chr5	+	170814707	170837888	170814952	170837569	11	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170827842,170832305,170834703,170837530,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170827929,170832407,170834778,170837888,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,0,")
    print("NPM1", refGene.returnPLoc("p.L287Q"))
    print("NPM1", refGene.returnExon("exon10"))
    print("NPM1", refGene.returnIntron("intron10"))
    print("NPM1", refGene.returnExon("exon11"))

    print("CEBPA#####################################################################################")

    refGene = RefGene(
        "1888	NM_002520	chr5	+	170814707	170837888	170814952	170837569	11	170814707,170817054,170818308,170818709,170819713,170819917,170827156,170827842,170832305,170834703,170837530,	170815010,170817134,170818428,170818803,170819820,170819982,170827214,170827929,170832407,170834778,170837888,	0	NPM1	cmpl	cmpl	0,1,0,0,1,0,2,0,0,0,0,")
    print("NPM1", refGene.returnPLoc("p.L287Q"))
    print("NPM1", refGene.returnExon("exon10"))
    print("NPM1", refGene.returnIntron("intron10"))
    print("NPM1", refGene.returnExon("exon11"))

    print("TERT#####################################################################################")

    refGene = RefGene(
        "594	NM_001193376	chr5	-	1253286	1295162	1253842	1295104	15	1253286,1254482,1255401,1258712,1260588,1266578,1268634,1271233,1272299,1278755,1279405,1280272,1282543,1293427,1294885,	1253946,1254620,1255526,1258774,1260715,1266650,1268748,1271319,1272395,1278911,1279585,1280453,1282739,1294781,1295162,	0	TERT	cmpl	cmpl	1,1,2,0,2,2,2,0,0,0,0,2,1,0,0,")
    print(refGene.returnPLoc("p.S2371T"))
    print(refGene.returnCdsLen())

    print("ELANE#####################################################################################")

    refGene = RefGene(
        "591	NM_001972	chr19	+	852208	856246	852328	856164	5	852208,852875,853261,855563,855957,	852395,853032,853403,855794,856246,	0	ELANE	cmpl	cmpl	0,1,2,0,0,")
    print(refGene.returnPLoc("p.S292T"))
    print(refGene.returnCdsLen())

    print("HAX1#####################################################################################")

    refGene = RefGene(
        "1761	NM_006118	chr1	+	154245038	154248355	154245199	154248177	7	154245038,154245811,154246249,154247425,154247629,154247868,154248091,	154245252,154246074,154246437,154247477,154247736,154247959,154248355,	0	HAX1	cmpl	cmpl  0,2,1,0,1,0,1,")
    print(refGene.returnPLoc("p.S376T"))
    print(refGene.returnCdsLen())

    print("DNMT3A#####################################################################################")

    refGene = RefGene(
        "97	NM_175629	chr2	-	25455829	25565459	25457147	25536853	23	25455829,25458575,25459804,25461998,25463170,25463508,25464430,25466766,25467023,25467408,25468121,25468888,25469028,25469488,25469919,25470459,25470905,25497809,25498368,25505309,25523007,25536781,25565298,	25457289,25458694,25459874,25462084,25463319,25463599,25464576,25466851,25467207,25467521,25468201,25468933,25469178,25469645,25470027,25470618,25471121,25497956,25498412,25505580,25523112,25537030,25565459,	0	DNMT3A	cmpl	cmpl  2,0,2,0,1,0,1,0,2,0,1,1,1,0,0,0,0,0,1,0,0,0,-1,")
    print("DNMT3A", refGene.returnPLoc("p.P47S"))
    print("DNMT3A", refGene.returnPLoc("p.P72R"))

    print("TET2#####################################################################################")

    refGene = RefGene(
        "174	NM_001127208	chr4	+	106067841	106200960	106155099	106197676	11	106067841,106111516,106155053,106162495,106163990,106164726,106180775,106182915,106190766,106193720,106196204,	106068136,106111662,106158508,106162586,106164084,106164935,106180926,106183005,106190904,106194075,106200960,	0	TET2	cmpl	cmpl	-1,-1,0,1,2,0,2,0,0,0,1,")
    print("TET2", refGene.returnPLoc("p.P1134S"))
    print("TET2", refGene.returnPLoc("p.P1444R"))
    print("TET2", refGene.returnPLoc("p.P1842S"))
    print("TET2", refGene.returnPLoc("p.P1921R"))







