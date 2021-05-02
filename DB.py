import sqlite3
from NW_downloader import NW_download

c = None

def DB_start():
    conn = sqlite3.connect("webtoon_list.db", isolation_level=None)
    c = conn.cursor() 
    c.execute("CREATE TABLE IF NOT EXISTS webtoon_list \
        (id integer PRIMARY KEY, name text, weekday text, recentEpi integer)")

def DB_insert(id, name, weekday, epi):
    c.execute("INSERT INTO webtoon_list(id, name, weekday, recentEpi) \
    VALUES(?,?,?,?)", (id, name, weekday, epi))

def select_today(weekday):
    c.execute(f'SELECT * FROM webtoon_list WHERE weekday {weekday}')
    print(c.fetchall())

#웹툰을 추가하는 쓰레드
while True:
    name = input('name: ')
    new_webtoon(name)
#웹툰을 삭제하는 쓰레드


def new_webtoon(name):
    titleId, weekday = NW_search(name)
    DB_insert(titleId, name, weekday, 1)
    # 웹툰 디렉터리 생성
    wtdir = './naver webtoon downloader/'+name
    if not os.path.exists(wtdir):
        os.makedirs(wtdir, exist_ok=True)

def NW_search(name):
    url = 'https://comic.naver.com/webtoon/weekday.nhn'
    response = urlopen(url)
    as_weekday = BeautifulSoup(response, 'html.parser').select('div.list_area > div.col > div.col_inner > ul')
    for webtoons in as_weekday:
        for webtoon in webtoons.select('li > a'):
            if webtoon.string == name:
                id = webtoon['href'].replace('/webtoon/list.nhn?titleId=','').replace(id[-12:],'')
                weekday = webtoon['href'][-3:]
                return (id, weekday)
    url = 'https://comic.naver.com/webtoon/finish.nhn'
    response = urlopen(url)
    fins = BeautifulSoup(response, 'html.parser').select_one('div.list_area > ul')
    for webtoon in fins.select('li > div.thumb > a'):
        if webtoon['title'] == name:
            return (webtoon['href'].replace('/webtoon/list.nhn?titleId=',''), 'end')
    return print("해당되는 웹툰을 찾을 수 없습니다.")



