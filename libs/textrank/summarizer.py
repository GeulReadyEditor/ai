from textrank import TextRank, RawSummarizerReader

tr = TextRank()
print('Load...')
from konlpy.tag import Komoran
tagger = Komoran()
stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV') ])
# temp = "임의의 글을 넣고 test2.txt 자리에 temp 넣기, 그리고 나중에 request로 받은 param으로 대체"
tr.loadSents(RawSummarizerReader('test2.txt'), lambda sent: filter(lambda x:x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'), tagger.pos(sent)))
print('Build...')
tr.build()
ranks = tr.rank()
for k in sorted(ranks, key=ranks.get, reverse=True)[:100]:
    print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
print(tr.summarize(0.2))