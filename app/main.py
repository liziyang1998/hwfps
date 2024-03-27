import os

from flask import Flask, request
from get_hw_score import GetHwScoreByPOST

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getHwScore', methods=["POST"])
def getHwScore():
    name = request.json.get("name")
    id = request.json.get("id")
    season = request.json.get("season")
    if name == None or id == None or season == None:
        return 'input error'
    if type(name) != str:
        return 'input error'
    if type(id) != str:
        return 'input error'
    if type(season) != int:
        return 'input error'
    
    platyType = []
    score = []
    rating = []
    rws = []
    adr = []
    times = []
    rate = []

    seasonData = request.json.get("seasonData")
    if type(seasonData) != list:
        return 'input error'
    for i in range(0, season):
        try:
            int(seasonData[i][0])
            float(seasonData[i][1])
            float(seasonData[i][2])
            float(seasonData[i][3])
            float(seasonData[i][4])
            float(seasonData[i][5])
            float(seasonData[i][6])
        except Exception as e:
            return 'input error: ' + str(e)
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
    # app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
    app.run()