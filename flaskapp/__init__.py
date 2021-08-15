import json

import pymongo
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import requests


# configs
# from configs import *

from libs.textrank import summarizer
from libs.textrank import tagger
# from libs.sentence_complete import complete



app = Flask(__name__)
app.debug = True


@app.route("/summarizer", methods=['POST'])
def get_summarizer():
    contents = request.form["contents"]
    summary = summarizer.summarizing(contents)
    return summary


@app.route("/tagger", methods=['POST'])
def get_tagger():
    contents = request.form["contents"]
    tag = tagger.tagging(contents)
    return tag

# @app.route("/complete", methods=['POST'])
# def get_complete():
#     text = request.form['text']
#     num_samples = 5
#     length = 60
#     sentence_complete = complete.sentence_complete(text, num_samples, length)
#     result = ""
#     for r in sentence_complete:
#         result += r
#     return result







