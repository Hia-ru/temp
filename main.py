from NW_downloader import NW_download
from DB import DB_start, select_today
import schedule
import time
import datetime
 
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'end']

def update():
    today = datetime.datetime.today().weekday()
    DB_start()
    for webtoon in select_today(days[today]):
        currunt = NW_currentEpi(webtoon[0],webtoon[2])
        recent = webtoon[3]
        id = webtoon[0]
        NW_download(id, recent+1 ,currunt)

schedule.every(60).day.at("00:01").do(update)

while True:
    schedule.run_pending()
    time.sleep(60)

def NW_currentEpi(titleId, weekday):
    response = urlopen('https://comic.naver.com/webtoon/list.nhn?titleId='+titleId+'&weekday='+weekday)
    soup = BeautifulSoup(response, 'html.parser')
    currunt = soup.select_one('table.viewList > tbody > tr > td.title > a')['href']
    current = current.replace(current[-12:],'').replace('/webtoon/detail.nhn?titleId='+titleId+'&no=','')
    return int(current)


# while True:
#     print('콤마로 구분. 이름이 정확히 일치해야 함. 화수는 예고편 등을 포함한 전체화수 기준')
#     title, start, end = input('웹툰명, 시작화, 끝화: ').split(',')
#     NW_download(title,start,end)
