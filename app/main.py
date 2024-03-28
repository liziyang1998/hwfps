import os

from flask import Flask, request, render_template
from get_hw_score import GetHwScoreByPOST

app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

def errorCheck(seasonData):
    try:
        int(seasonData[0])
    except Exception as e:
        return 'input error: 平台类型' + str(e)
    if int(seasonData[0]) < 0:
        return 'input error: 平台类型未选择'
    
    try:
        float(seasonData[1])
    except Exception as e:
        return 'input error: 天梯分未输入或' + str(e)
    
    try:
        float(seasonData[2])
    except Exception as e:
        return 'input error: rating未输入或' + str(e)

    try:
        float(seasonData[3])
    except Exception as e:
        return 'input error: rws/we未输入或' + str(e)

    try:
        float(seasonData[4])
    except Exception as e:
        return 'input error: adr未输入或' + str(e)

    try:
        float(seasonData[5])
    except Exception as e:
        return 'input error: 场次未输入或' + str(e)

    try:
        float(seasonData[6])
    except Exception as e:
        return 'input error: 胜率未输入或' + str(e)

    return None

@app.route('/getHwScore', methods=["POST"])
def getHwScore():
    name = request.json.get("name")
    id = request.json.get("id")
    seasonStr = request.json.get("season")
    if name == None or id == None or seasonStr == None:
        return 'input error, name/id/season is None'
    if type(name) != str:
        return 'input error, name is not str'
    if type(id) != str:
        return 'input error, id is not str'
    try:
        int(seasonStr)
    except Exception as e:
        return 'input error: season未输入或不是整数'
    season = int(seasonStr)
    
    platyType = []
    score = []
    rating = []
    rws = []
    adr = []
    times = []
    rate = []

    seasonData = request.json.get("seasonData")
    if seasonData == None:
        return 'input error, seasonData is None'
    if type(seasonData) != list:
        return 'input error, seasonData is not list'
    for i in range(0, season):
        errorLog = errorCheck(seasonData[i])
        if errorLog != None:
            return errorLog
        platyType.append(seasonData[i][0])
        score.append(seasonData[i][1])
        rating.append(seasonData[i][2])
        rws.append(seasonData[i][3])
        adr.append(seasonData[i][4])
        times.append(seasonData[i][5])
        rate.append(seasonData[i][6])
    data = {
        'name' : name,
        'id' : id,
        'season' : season,
        'seasonData' : []
    }
    for i in range(0, season):
        data['seasonData'].append([platyType[i], score[i], rating[i], rws[i], adr[i], times[i], rate[i]])
    return GetHwScoreByPOST(data)

if __name__ == "__main__":
    # app.run()
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))