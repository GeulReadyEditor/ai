# -*- coding: utf-8 -*-
import requests
import json
import re

def sentence_complete(text):
    response = requests.post(
        #브런치, 말뭉치 학습한 api
        url = "https://train-bc1rqj6ngwhfyti9fyf0-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-ko-small-finetune",
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps({
            "text": text,
            "num_samples": 5,
            "length": 60
        })
    )

    results =[]
    for r in response.json():
        cutting = r.split('.', 1)[1]  # 온점 이후
        sentence = r.replace(cutting, '')  # 마지막 온점이후 전부 버림
        hanguel = re.compile('[^ ㄱ-ㅣ가-힣.,\d+]')  # 한글, 띄어쓰기, 숫자, 온점만 가능. 물음표도 제거되는 문제
        text = hanguel.sub('', sentence)
        result = re.sub('[-=+#/:^$@*\"※~&%ㆍ_!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)  # 혹시모르는 특수문자 전부제거
        results.append(result)

    return results

