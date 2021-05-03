from bs4 import BeautifulSoup
from urllib.request import urlopen
import schedule
import time
import datetime
import glob
from NW_downloader import NW_download
from DB import db
 
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'end']

def update():
    today = datetime.datetime.today().weekday()
    db.start()
    todays = db.select_today(days[today])
    if todays != []:
        print('오늘 다운받을 웹툰')
        for webtoon in todays:
            print(webtoon)
        for webtoon in todays:
            name = webtoon[1]
            NW_download(name)
    else:
        print('오늘은 다운받을 웹툰이 없습니다.')
    print(schedule.jobs)

schedule.every().days.at("00:01").do(update)

while True:
    schedule.run_pending()
    now = datetime.datetime.now()
    print('실행중입니다.', end='')
    print(now)
    time.sleep(50)



#할 것
#볼 수 있는 웹페이지 만들기
#정렬 기능