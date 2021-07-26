from textrank import TextRank, RawTaggerReader

tr = TextRank(window=5, coef=1)
print('Load...')
stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
# temp = "임의의 글을 넣고 test2.txt 자리에 temp 넣기, 그리고 나중에 request로 받은 param으로 대체"
tr.load(RawTaggerReader('test2.txt'), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
print('Build...')
tr.build()
kw = tr.extract(0.1)
for k in sorted(kw, key=kw.get, reverse=True):
    print("%s\t%g" % (k, kw[k]))