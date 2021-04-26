from bs4 import BeautifulSoup
from urllib.request import urlopen

def NW_url(titleId, epi, weekday):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+titleId+'&no='+epi+'&weekday='+weekday
    return url

for i in range(1, 3):
    response = urlopen(NW_url('748105',f'{i}','sun'))
    soup = BeautifulSoup(response, 'html.parser') 
    images = soup.find("div", attrs={'class':'wt_viewer'})
    for img in images.find_all('img'):
        print(img['src'])

#이미지 주소 가져오기까지 완료

#할 것
#필요한 이미지만 다운
#이미지 이어붙이기
#볼 수 있는 웹페이지 만들기
#봇 만들기or매일 일정시각에 자동실행