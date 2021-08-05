# -*- coding: utf-8 -*-

from libs.textrank.textrank import TextRank, RawTaggerReader

def tagging(contents):
    tr = TextRank(window=5, coef=1)

    print('Load...')
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
    tr.load(RawTaggerReader(contents), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
    print('Build...')
    tr.build()
    kw = tr.extract(0.1)

    for k in sorted(kw, key=kw.get, reverse=True)[:5]: #상위 다섯개만 추출
        '''
            k는 
            (('도쿄', 'NNP'), ('올림픽', 'NNP'))
            (('스포츠', 'NNP'), ('중계', 'NNG'))
            (('이미지', 'NNG'),)
            (('때', 'NNG'),)
            (('자막', 'NNP'),)
            (('사진', 'NNG'),)
            (('구성원', 'NNG'),)
            (('소개', 'NNG'),)
            
            위와 같은 형태로 출력됨

        '''


        if len(k)>1: #pair가 되어있다면
            pair_tagger = []
            for i in k:
                pair_tagger.append(list(i)[0])
            return (''.join(pair_tagger))
        else:
            return (list(k[0])[0])

