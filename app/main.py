import os

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getHwScore', methods=["POST"])
def getHwScore():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    data = {
        "username": username,
        "password": password
    }
    return data

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))