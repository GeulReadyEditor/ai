from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.debug = True

# response order
app.config["JSON_SORT_KEYS"] = False
# DB = dbConnection.DB
app.config["MONGO_URI"] = "mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin"
mongo = PyMongo(app)

#사용자에게 해당하는 태그 불러오기
def get_keywords():
    cursor = mongo.db.user.find({},
                                {
                                    "_id": 0,
                                    "name": 0,
                                    "nickname": 0,
                                    "intro": 0,
                                    "profileImage": 0,
                                    "scraps": 0,
                                    "likes": 0,
                                    "followers": 0,
                                    "followings": 0
                                }
                                )
    list_cur = list(cursor)
    # print(list_cur)
    result_list = ""
    for x in list_cur:
        result_string = ""
        result_string += x['email']
        result_string += " "
        # print(x) #{'email': 'parktae27@admin.com', 'tags': ['물집', '완주', '지구', '사람', '마라톤', '무릎', '슈퍼맨', '포기', '운동']
        for tag in x['tags']:
            result_string += tag
            result_string += " "
            # print(result_string)
        result_list += result_string
        result_list += "\n"

    '''
    sciencelife@admin.com 사랑 과학 행복 사랑 연애 키스 과학 인문학 교양
    wivlabs@admin.com 광고 페이스북 IT 타겟 효율 키스 광고성과 인문학 구글

    result_list 이러한 형태
    '''
    return result_list



#게시글의 tags 불러오기
def get_post_tags():
    cursor = mongo.db.board.find({},
                                 {
                                     "userId": 0,
                                     "title": 0,
                                     "comments": 0,
                                     "nickName": 0,
                                     "subtitle": 0,
                                     "titleImage": 0,
                                     "likes": 0,
                                     'contents': 0,
                                     "modDatetime": 0,
                                     "_class": 0
                                 }
                                 )
    list_cur = list(cursor)

    # print(list_cur)
    result_list = ""
    for x in list_cur:
        result_string = ""
        result_string += str(ObjectId(x['_id']))
        result_string += " "
        # print(x)
        for tag in x['tags']:
            result_string += tag
            result_string += " "
            # print(result_string)
        result_list += result_string
        result_list += "\n"
        # print(str(ObjectId(x['_id'])))

    # print(result_list)

    return result_list

