import json

from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import requests

# configs
# from configs import *

from libs.textrank import summarizer
from libs.textrank import tagger
from libs.sentence_complete import complete


app = Flask(__name__)
app.debug = True
# response order
app.config["JSON_SORT_KEYS"] = False
# DB = dbConnection.DB
app.config["MONGO_URI"] = "mongodb://onego:test123@onegomongo.ddns.net:80/onego?authsource=admin"
mongo = PyMongo(app)


@app.route("/")
def get_contents():
    return '<html><body><h1>contents</h1></body></html>'

@app.route("/summarizer", methods=['POST'])
def get_summarizer():
    contents = request.json["contents"]
    summary = summarizer.summarizing(contents)
    return summary


@app.route("/tagger", methods=['POST'])
def get_tagger():
    contents = request.json["contents"]
    tag = tagger.tagging(contents)
    return tag

@app.route("/complete", methods=['POST'])
def get_complete():
    text = request.json["text"]
    num_samples = request.json["num_samples"]
    length = request.json["length"]
    sentence_complete = complete.sentence_complete(text, num_samples, length)
    result = jsonify(sentence_complete)
    return result



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
