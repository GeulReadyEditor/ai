from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
# configs
from configs import *
# libs
from libs.greet import *

app = Flask(__name__)
app.debug = True
# response order
app.config["JSON_SORT_KEYS"] = False
DB = dbConnection.DB
app.config["MONGO_URI"] = f"mongodb://{DB.username}:{DB.password}@{DB.host}:{DB.port}/{DB.database}"
mongo = PyMongo(app)

@app.route("/")
def helloworld():
    message = hello.helloworld()
    return message

# @app.route("/db/", methods=['GET'])
# def dbHello():
#     cursor = mongo.db.tb_diets.find({}, {'_id': 0})
#     list_cur = list(cursor)
#     return jsonify(list_cur)
#
# # host:port/parameter?argument='argument'
# @app.route("/parameter", methods=['GET'])
# def dbKeyword():
#     argument = request.args.get('argument')
#     cursor = mongo.db.tb_diets.find({}, {'_id': 0})
#     list_cur = list(cursor)
#     print(argument)
#     return jsonify(list_cur)
#
# #yoga
#
# @app.route("/getYogas", methods=['GET'])
# def getYogas():
#     returnJson = {'res_state': '', 'res_msg': '', 'res_data': {}}
#
#     trimester = request.args.get('trimester')
#     pose = request.args.get('pose')
#
#     if trimester:
#         if pose:
#             cursor = mongo.db.yogas.find({'trimester': trimester, 'pose': pose}, {'_id': 0})
#             list_cur = list(cursor)
#             returnJson['res_state'] = 'success_get_yoga_pose'
#             returnJson['res_msg'] = '요가 자세를 성공적으로 가져왔습니다.'
#             returnJson['res_data'] = list_cur
#         else:
#             cursor = mongo.db.yogas.find({'trimester': trimester}, {'_id': 0, 'trimester': 0, 'description': 0})
#             list_cur = list(cursor)
#             returnJson['res_state'] = 'success_get_yoga_list'
#             returnJson['res_msg'] = '요가 목록을 성공적으로 가져왔습니다.'
#             returnJson['res_data'] = list_cur
#
#     return jsonify(returnJson)
