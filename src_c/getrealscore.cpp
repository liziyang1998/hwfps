/*
    本程序功能是测算一个人csgo的真实水平，最终分数对应完美分数，用于后续solo和major分组

    输入格式要求如下：
    第一行一个数n，代表几个人
    接下来n项
    每一项第一行包含三个项目：姓名、游戏id、数字m，数字m代表有几个赛季的数据，完美或者5e都可以
    接下来m行，每一行7个数据，分别是：
    平台类型、分数、rating、rws/we、adr、场次、胜率
    （完美是we，5e是rws）

    注：
    1、平台类型完美是0，5e是1

    举例：
    1
    aaa 工号 id 3
    0   1816    1.04    10.66   81.72   43  53
    1   2231    0.97    10.23   75      26  50
    0   1775    1.09    11.13   84      5   40      
*/

#include <cmath>
#include <iostream>
#include <cstring>
#include <algorithm>
#include <map>
#include <fstream>
using namespace std;

#define BASERATING 1.0
#define BASERWS 10
#define BASEADR 80
#define BASERATE 50
#define BASEWE 8
#define SEASONNUM 10

enum PLATTYPE {perfect, EEEEE_Non_Priority, EEEEE_Priority};

std::istream& operator>>(std::istream& is, PLATTYPE& t)
{
    int a;
    is >> a;
    t = static_cast<PLATTYPE>(a);
    return is;
}

class Weight {
public:
    Weight(): exp(1), basePara(0), baseScore(0) {}
    Weight(double e, double bp, double bs): exp(e), basePara(bp), baseScore(bs) {}
    double Calc(double para) {
        double base = pow(basePara, exp);
        return ((pow(para, exp) - base) / base) * baseScore;
    }
    double GetBaseScore() {
        return baseScore;
    }
private:
    double exp;
    double basePara;
    double baseScore;
};

class Member {
public:
    char name[50], id[30];
    int season;
    PLATTYPE platType[SEASONNUM];
    double score[SEASONNUM], times[SEASONNUM], rate[SEASONNUM];
    double rating[SEASONNUM], rwsAndWe[SEASONNUM], adr[SEASONNUM];
    double getRealScore(map<string, Weight> m) {
        double ans = 0;
        double realScore[SEASONNUM];
        for (int i = 0; i < season; i++) {
            if (platType[i] == 0 && rwsAndWe[i] < 7 && (rating[i] > BASERATING || adr[i] > BASEADR)) {
                rwsAndWe[i] *= 1.6;
            }
            // 完美使用we计算，5e使用rws计算
            double s = m["rating"].Calc(rating[i]) + m["adr"].Calc(adr[i])  + (platType[i] == 0? m["we"].Calc(rwsAndWe[i]):m["rws"].Calc(rwsAndWe[i]));
            double startScore = getStartScore(i, m);

            // 真实分数 = 现在分数和赛季初始分的平均分 + 修正分
            realScore[i] = (score[i] + startScore)/2 + getAtan(s * (Max(0, getFixRate(times[i]))));
        }
        sort(realScore, realScore+season, greater<double>());
        int num = Min(season, 3);
        for (int i = 0; i < num; i++) {
            ans += realScore[i] * scoreRate[num][i];
        }
        return ans;
    }

private:
    double scoreRate[4][3] = {
        {0, 0, 0},
        {1, 0, 0},
        {0.8, 0.2, 0},
        {0.7, 0.15, 0.15}
    };

    double winMax = 35, winMin = 15;
    double lossMax = -5, lossMin = -40;

    double getFixRate(double times) {
        if (times >= 10) {
            return (times - 10) / 40 + 1;
        }
        return times / 10;
    }
    
    double Max(double a, double b) {
        return a > b? a:b;
    }
    double Min(double a, double b) {
        return a > b? b:a;
    }

    double getStartScore(int index, map<string, Weight> m) {
        double ratingBaseScore = m["rating"].GetBaseScore();
        double adrBaseScore = m["adr"].GetBaseScore();
        double rwsBaseScore = m["rws"].GetBaseScore();
        double weBaseScore = m["we"].GetBaseScore();
        
        double base = rating[index]/BASERATING*ratingBaseScore + adr[index]/BASEADR*adrBaseScore + (platType[index] == 0? (rwsAndWe[index]/BASEWE*weBaseScore) : (rwsAndWe[index]/BASERWS*rwsBaseScore));
        base /= (ratingBaseScore + adrBaseScore + (platType[index] == 0? weBaseScore:rwsBaseScore));

        double winScore = 0;
        double lossScore = 0;
        double winTimes = times[index] * rate[index] / 100;
        double lossTimes = times[index] - winTimes;
        // 获胜局加分
        winScore = ((winMax-winMin)/(2.0-0.5) * (base-0.5) + winMin) * winTimes;
        // 失败局减分
        lossScore = ((lossMax-lossMin)/(2.0-0.5) * (base-0.5) + lossMin) * lossTimes;
        return score[index] - Max((winScore+lossScore)*(1, 20/times[index]), 0);
    }

    double getAtan(double x) {
        // atan(x * 根号3 / 700) * 900 / (pi/3)
        double res = atan(x * 1.732 / 700) * 900 / M_PI;
        if (x > 0 && x < 300) {
            return res - 10;
        } else if (x < 0 && x > -300) {
            return res + 10;
        }
        return res;
    }
};

map<string, Weight> WeightMap;
Member majorMember[200];
int n;

void init()
{
    // Weight三个参数代表：指数、基本值、影响分数
    WeightMap.insert(make_pair<string, Weight>("rws", Weight(2.0, BASERWS, 100)));
    WeightMap.insert(make_pair<string, Weight>("rating", Weight(2.0, BASERATING, 100)));
    WeightMap.insert(make_pair<string, Weight>("adr", Weight(2.0, BASEADR, 200)));
    WeightMap.insert(make_pair<string, Weight>("we", Weight(2.0, BASEWE, 100)));
}

void input()
{
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> majorMember[i].name >> majorMember[i].id >> majorMember[i].season;
        for (int j = 0; j < majorMember[i].season; j++) {
            cin >> majorMember[i].platType[j] >> majorMember[i].score[j] >> majorMember[i].rating[j] >> majorMember[i].rwsAndWe[j] >> majorMember[i].adr[j] >> majorMember[i].times[j] >> majorMember[i].rate[j];
        }
    }
}

void FilePrint()
{
    ofstream p;
    p.open("output.csv", ios::out|ios::trunc);
    char c1 = 0xEF;
    char c2 = 0xBB;
    char c3 = 0xBF;
    p << c1 << c2 << c3;
    for (int i = 0; i < n; i++) {
        p << majorMember[i].name << "," << majorMember[i].id << "," << majorMember[i].getRealScore(WeightMap) << endl;
    }
}

void print()
{
    for (int i = 0; i < n; i++) {
        cout << majorMember[i].name << "," << majorMember[i].id << "," << majorMember[i].getRealScore(WeightMap) << endl;
    }
}

int main()
{
    init();
    input();
    // FilePrint();
    print();
}