# -*- coding: utf-8 -*-

from libs.textrank.textrank import TextRank, RawSummarizerReader


def summarizing(contents):
    tr = TextRank()
    print('Load...')
    from konlpy.tag import Komoran
    tagger = Komoran()
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV') ])
    tr.loadSents(RawSummarizerReader(contents), lambda sent: filter(lambda x:x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'), tagger.pos(sent)))
    print('Build...')
    tr.build()
    ranks = tr.rank()
    for k in sorted(ranks, key=ranks.get, reverse=True)[:1]: #가장 상위 문장 하나 출력
        # print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
        return (tr.dictCount[k]) #특수기호..?


    # return (tr.summarize(0.15)) #전체 내용 요약.. ratio수치 변경으로 정도 조절



#0.2 (서울=연합뉴스) 신선미 기자 = 방역당국은 국내 신종 코로나바이러스 감염증(코로나19) 확산세를 당분간은 꺾기 어려울 것이라고 평가하면서 일단 4차 대유행 이전 수준으로 확진자 발생을 억제하는 것이 1차 목표라고 밝혔다. 당국은 다만 앞선 2∼3차 유행과는 상황이 다르다며 구체적인 수치는 제시하지 않았다. (서울=연합뉴스) 장예진 기자 = 중앙방역대책본부는 29일 0시 기준으로 코로나19 신규 확진자가 1천674명 늘어 누적 19만5천99명이라고 밝혔다.  코로나19 유행 이후 파견 의료진 수는 누적 5천333명이다.

#0.1 (서울=연합뉴스) 신선미 기자 = 방역당국은 국내 신종 코로나바이러스 감염증(코로나19) 확산세를 당분간은 꺾기 어려울 것이라고 평가하면서 일단 4차 대유행 이전 수준으로 확진자 발생을 억제하는 것이 1차 목표라고 밝혔다.  코로나19 유행 이후 파견 의료진 수는 누적 5천333명이다.
#0.15 (서울=연합뉴스) 신선미 기자 = 방역당국은 국내 신종 코로나바이러스 감염증(코로나19) 확산세를 당분간은 꺾기 어려울 것이라고 평가하면서 일단 4차 대유행 이전 수준으로 확진자 발생을 억제하는 것이 1차 목표라고 밝혔다. 당국은 다만 앞선 2∼3차 유행과는 상황이 다르다며 구체적인 수치는 제시하지 않았다.  코로나19 유행 이후 파견 의료진 수는 누적 5천333명이다.
