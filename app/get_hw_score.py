import sys
import math

BASERATING = 1.0
BASERWS = 10
BASEADR = 80
BASERATE = 50
BASEWE = 8

class Weight:
    def __init__(self, exp, basePara, baseScore) -> None:
        self.exp = exp
        self.basePara = basePara
        self.baseScore = baseScore
    def Calc(self, para):
        base = math.pow(self.basePara, self.exp)
        return ((math.pow(para, self.exp) - base) / base) * self.baseScore
    def GetBaseScore(self):
        return self.baseScore
        
class Member:
    def __init__(self, name, id, season) -> None:
        self.name = name
        self.id = id
        self.season = int(season)
        self.platType = []
        self.score = []
        self.rating = []
        self.rwsAndWe = []
        self.adr = []
        self.times = []
        self.rate = []

        self._scoreRate = [[0,0,0], [1,0,0], [0.8,0.2,0], [0.65, 0.2, 0.15]]
        self._winMax = 35
        self._winMin = 15
        self._lossMax = -5
        self._lossMin = -40
        pass

    def AddData(self, platType, score, rating, rwsAndWe, adr, times, rate):
        self.platType.append(int(platType))
        self.score.append(float(score))
        self.rating.append(float(rating))
        self.rwsAndWe.append(float(rwsAndWe))
        self.adr.append(float(adr))
        self.times.append(float(times))
        self.rate.append(float(rate))

    def GetRealScore(self, weight):
        ans = 0
        realScore = []
        for i in range(0, self.season):
            if (self.platType[i]  == 0) and (self.rwsAndWe[i] < 7) and (self.rating[i] > BASERATING or self.adr[i] > BASEADR):
                self.rwsAndWe[i] = self.rwsAndWe[i] * 1.6 
            
        pass


memberList = []
weightList = {}

def getWeightMap():
    weightList['rws'] = Weight(2.0, BASERWS, 100)
    weightList['rating'] = Weight(2.0, BASERATING, 100)
    weightList['adr'] = Weight(2.0, BASEADR, 200)
    weightList['we'] = Weight(2.0, BASEWE, 100)

def getInput():
    getWeightMap()
    n = input('输入人数:\n')
    for loopi in range(0, int(n)):
        info = input('输入姓名、工号、赛季数据数量:\n').split(' ')
        name, id, season = info[0], info[1], int(info[2])
        member = Member(name, id, season)
        memberList.append(member)
        for loopj in range(0, season):
            data = input('输入平台类型(完美是0,5e是1)、天梯分、rating、rws/we、adr、场次、胜率:\n').split(' ')
            print(data)


getInput()