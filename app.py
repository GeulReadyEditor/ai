from flask import Flask, jsonify
# mysql
# from flask_mysqldb import MySQL
app = Flask(__name__)

# mysql start
# app.secret_key ="1234"
app.config["USERNAME"] = "onego"
app.config["PASSWORD"] = "test123"
app.config["HOST"] = "onegomongo.ddns.net"
app.config["PORT"] = "80"
app.config["DATABASE"] = "onego"


# mysql = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="0000",
#     database="scott"
# )

# mysql end

@app.route('/')
def hello():
    return "Hello world!"


# 1. dict(), list() 다루는 법
# 2. str (json)-> dict, list
# 3. mongodb를 사용하는 방법
# 4. configs -> 숨겨놔야 함 ex) db정보, ip, ...