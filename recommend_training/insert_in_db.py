from flask import Flask
from flask_pymongo import PyMongo, MongoClient
import training
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin"
mongo = PyMongo(app)

# DB에 사용자 주입
client = MongoClient('mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin')
db = client['onego']
collection = db['recommended']

def insert_into():
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
                                    "followings": 0,
                                    "tags": 0,
                                    "nickName": 0
                                }
                                )
    want_users = list(cursor)
    list_want_user = []
    for x in want_users:
        list_want_user.append(x['email'])

    for want_user in list_want_user:
        most = training.most_similar(want_user, 11)
        list_sim = []
        for sim in most[1:11]:
            list_sim.append(sim[0])

            recommend = {
                "email": want_user,
                "recommendation": list_sim
            }
        print(recommend)
        recommended = db.recommended
        recommended.insert(recommend)
    return 'insert_finish'