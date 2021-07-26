from flask import Flask, jsonify
# mysql
# from flask_mysqldb import MySQL
import mysql.connector
app =   Flask(name)

# mysql start
# app.secret_key ="1234"
# app.configs["MYSQL_HOST"] = "localhost"
# app.configs["MYSQL_USER"] = "root"
# app.configs["MYSQL_PASSWORD"] = "0000"
# app.configs["MYSQL_DB"] = "scott"

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
    database="scott"
)

# mysql end

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/json')
def jsonapi():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT * FROM s_dept")
    rv = cursor.fetchall()
    return jsonify(rv)

# 1. dict(), list() 다루는 법
# 2. str (json)-> dict, list
# 3. mongodb를 사용하는 방법
# 4. configs -> 숨겨놔야 함 ex) db정보, ip, ...