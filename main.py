from NW_downloader import NW_download
from bs4 import BeautifulSoup
from urllib.request import urlopen
from DB import db
import schedule
import time
import datetime
import glob
 
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'end']

def update():
    today = datetime.datetime.today().weekday()
    db.start()
    for webtoon in db.select_today(days[today]):
        current = NW_currentEpi(webtoon[0],webtoon[2])
        recent = webtoon[3]
        id = webtoon[0]
        name = webtoon[1]
        NW_download(id, name, recent+1 ,current)

# schedule.every(60).day.at("00:01").do(update)

# while True:
#     schedule.run_pending()
#     time.sleep(60)

def NW_currentEpi(titleId, weekday):
    response = urlopen('https://comic.naver.com/webtoon/list.nhn?titleId='+f'{titleId}'+'&weekday='+weekday)
    soup = BeautifulSoup(response, 'html.parser')
    current = soup.select_one('.viewList > tr > td.title > a')['href']
    current = current.replace(current[-12:],'').replace('/webtoon/detail.nhn?titleId='+f'{titleId}'+'&no=','')
    return int(current)

today = datetime.datetime.today().weekday()
db.start()
todays = db.select_today('fri')
if todays != []:
    for webtoon in todays:
        current = NW_currentEpi(webtoon[0],webtoon[2])
        recent = webtoon[3]
        id = webtoon[0]
        name = webtoon[1]
        NW_download(id, name, recent+1 ,current)
else:
    print('오늘은 다운받을 웹툰이 없습니다.')

# while True:
#     print('콤마로 구분. 이름이 정확히 일치해야 함. 화수는 예고편 등을 포함한 전체화수 기준')
#     title, start, end = input('웹툰명, 시작화, 끝화: ').split(',')
#     NW_download(title,start,end)
