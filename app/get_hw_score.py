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
    def calc(self, para):
        base = math.pow(self.basePara, self.exp)
        return ((math.pow(para, self.exp) - base) / base) * self.baseScore
    def getBaseScore(self):
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

    def addData(self, platType, score, rating, rwsAndWe, adr, times, rate):
        self.platType.append(int(platType))
        self.score.append(float(score))
        self.rating.append(float(rating))
        self.rwsAndWe.append(float(rwsAndWe))
        self.adr.append(float(adr))
        self.times.append(float(times))
        self.rate.append(float(rate))
    
    def dataPrint(self):
        print(self.platType, self.score, self.rating, self.rwsAndWe, self.adr, self.times, self.rate)

    def getRealScore(self, weight):
        ans = 0
        realScore = []
        for i in range(0, self.season):
            if (self.platType[i]  == 0) and (self.rwsAndWe[i] < 7) and (self.rating[i] > BASERATING or self.adr[i] > BASEADR):
                self.rwsAndWe[i] = self.rwsAndWe[i] * 1.6 
            fixScore = weight['rating'].calc(self.rating[i]) + weight['adr'].calc(self.adr[i]) + (weight['we'].calc(self.rwsAndWe[i]) if self.platType[i] == 0 else weight['rws'].calc(self.rwsAndWe[i]))
            startScore = self.getStartScore(i, weight)
            realScore.append((self.score[i] + startScore) / 2 + self.getAtan(fixScore * max(0, self.getFixRate(self.times[i]))))
        realScore.sort(reverse=True)
        num = min(self.season, 3)
        for i in range(0, num):
            ans = ans + realScore[i] * self._scoreRate[num][i]
        return ans
    
    def getStartScore(self, index, weight):
        ratingBaseScore = weight['rating'].getBaseScore()
        adrBaseScore = weight['adr'].getBaseScore()
        rwsBaseScore = weight['rws'].getBaseScore()
        weBaseScore = weight['we'].getBaseScore()

        base = self.rating[index]/BASERATING*ratingBaseScore + self.adr[index]/BASEADR*adrBaseScore + (self.rwsAndWe[index]/BASEWE*weBaseScore if self.platType[index] == 0 else self.rwsAndWe[index]/BASERWS*rwsBaseScore)
        base = base / (ratingBaseScore + adrBaseScore + (weBaseScore if self.platType[index] == 0 else rwsBaseScore))

        winTimes = int(self.times[index] * self.rate[index] / 100)
        lossTimes = int(self.times[index] - winTimes)
        # 获胜局加分
        winScore = ((self._winMax-self._winMin)/(2.0-0.5) * (base-0.5) + self._winMin) * winTimes
        # 失败局减分
        lossScore = ((self._lossMax-self._lossMin)/(2.0-0.5) * (base-0.5) + self._lossMin) * lossTimes
        return self.score[index] - max((winScore+lossScore)*max(1, 20/self.times[index]), 0)
    
    def getFixRate(self, times):
        if times >= 10:
            return (times - 10) / 40 + 1
        else:
            return times / 10
    
    def getAtan(self, x):
        res = math.atan(x * 1.732 / 700) * 900 / math.pi
        if x > 0 and x < 300:
            return res - 10
        elif x < 0 and x > -300:
            return res + 10
        else:
            return res

memberList = []
weightList = {
    'rws' : Weight(2.0, BASERWS, 100),
    'rating' : Weight(2.0, BASERATING, 100),
    'adr' : Weight(2.0, BASEADR, 200),
    'we' : Weight(2.0, BASEWE, 100)
}

def getInput():
    n = input('输入人数:\n')
    for loopi in range(0, int(n)):
        info = input('输入姓名、工号、赛季数据数量:\n').split(' ')
        name, id, season = info[0], info[1], int(info[2])
        member = Member(name, id, season)
        memberList.append(member)
        for loopj in range(0, season):
            data = input('输入平台类型(完美是0,5e是1)、天梯分、rating、rws/we、adr、场次、胜率:\n').split(' ')
            member.addData(int(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5]), float(data[6]))

def getAllMemberScore():
    global memberList
    global weightList
    for member in memberList:
        print('%s,%s,%.2f'%(member.name, member.id, member.getRealScore(weightList)))

def GetHwScoreByPOST(data):
    name = data['name']
    id = data['id']
    season = data['season']
    seasonData = data['seasonData']
    member = Member(name, id, season)
    for i in range(0, season):
        member.addData(int(seasonData[i][0]), float(seasonData[i][1]), float(seasonData[i][2]), float(seasonData[i][3]), float(seasonData[i][4]), float(seasonData[i][5]), float(seasonData[i][6]))
    return ('name = %s; id = %s; hwScore = %.2f'%(member.name, member.id, member.getRealScore(weightList)))

def testGetHwScore():
    getInput()
    getAllMemberScore()
