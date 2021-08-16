from flask import Flask, jsonify, request, render_template
from libs.textrank import summarizer
from libs.textrank import tagger
from libs.sentence_complete import complete



app = Flask(__name__)
app.debug = True


@app.route("/summarizer", methods=['POST'])
def get_summarizer():
    contents = request.get_json()['contents']
    summary = summarizer.summarizing(contents)
    return summary


@app.route("/tagger", methods=['POST'])
def get_tagger():
    contents = request.get_json()['contents']
    tag = tagger.tagging(contents)
    return jsonify(tag)

@app.route("/complete", methods=['POST'])
def get_complete():
    text = request.form['text']
    sentence_complete = complete.sentence_complete(text)
    complete_sentences = []
    for r in sentence_complete:
        complete_sentences.append(r)
    return jsonify(complete_sentences)







