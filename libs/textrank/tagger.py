# -*- coding: utf-8 -*-

from textrank import TextRank, RawTaggerReader

def tagging(contents):
    tr = TextRank(window=5, coef=1)
    print('Load...')
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV'), ('없', 'VV') ])
    tr.load(RawTaggerReader(contents), lambda w: w not in stopword and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))
    print('Build...')
    tr.build()
    kw = tr.extract(0.1)
    for k in sorted(kw, key=kw.get, reverse=True):
        print("%s\t%g" % (k, kw[k]))

contents = [
    '''
    
    2020 도쿄올림픽 개회식 중계부터 부적절한 이미지와 국가 소개로 사고를 치며 국제적으로 망신을 당한 MBC가 축구 중계에서도 선을 넘는 자막 사용으로 논란이 되고 있다. 이를 두고 MBC의 잇따른 올림픽 중계 논란은 '실수'가 아닌 '인재'라는 평이 나오고 있다.
    
    
    ''',
    '''MBC는 올해 1월 스포츠 프로그램 중계 및 제작 기능을 자회사인 MBC 플러스로 이관했다. 김성주, 김정근 등을 배출하며 '스포츠 중계' 명가로 불리던 MBC였기에 내부 구성원들의 반발도 있었다. 당시 MBC 스포츠국 구성원들은 성명서를 통해 "도쿄올림픽을 시작으로 동계올림픽, 아시안게임, 월드컵 등 줄줄이 이어지는 빅이벤트들을 준비조차 못 하는 경영진의 '찔러보기'식 접근은 MBC의 경쟁력 약화를 조장한다"고 우려를 표했다.
    ''',
    '''하지만 경영진은 부서 재배치를 강행했고, 도쿄올림픽 개막을 6개월 앞두고 진행된 인사이동에 자막과 영상 데스킹 작업도 제대로 이뤄지지 못했다는 후문이다.
    MBC는 이날 개회식 생중계 중 우크라이나 대표 이미지로 체르노빌 사진을 선택하고, 엘살바도르에는 비트코인 사진, 아이티에는 '대통령 암살로 정국은 안갯속'이라는 설명과 함께 내전 사진을 사용했다. 뿐만 아니라 아프가니스탄 선수단이 입장할 땐 마약의 재료가 되는 양귀비를 운반하는 이미지를 쓰고, 미셜 군도 소개로는 '한 때 미국의 핵실험장'이라는 문구를 삽입했다.
    '''
]
if __name__ == "__main__":
    tagging(contents)