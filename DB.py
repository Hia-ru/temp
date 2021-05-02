import sqlite3
from NW_downloader import NW_download
from bs4 import BeautifulSoup
from urllib.request import urlopen
from NW_downloader import NW_download
import os
import glob
import shutil
import time

class DB:
    c = None
    def start(self):
        conn = sqlite3.connect("webtoon_list.db", isolation_level=None)
        self.c = conn.cursor() 
        self.c.execute("CREATE TABLE IF NOT EXISTS webtoon_list \
            (id integer, name text PRIMARY KEY, weekday text, recentEpi integer)")

    def insert(self, id, name, weekday, epi):
        self.c.execute("INSERT INTO webtoon_list(id, name, weekday, recentEpi) \
        VALUES(?,?,?,?)", (int(id), name, weekday, epi))
    
    def select_today(self, weekday):
        self.c.execute('SELECT * FROM webtoon_list WHERE weekday = ?',(weekday,))
        return self.c.fetchall()

    def new_webtoon(self, name):
        titleId, weekday = NW_search(name)
        self.insert(titleId, name, weekday, 0)
        # 웹툰 디렉터리 생성
        name = name.replace('?',chr(0xFF1F)).replace('>',chr(0xFF1E))\
            .replace('\\',chr(0xFF3C)).replace('/',chr(0xFF1F))\
            .replace('"',chr(0xFF02)).replace('<',chr(0xFF1C))\
            .replace(':',chr(0xFF1A)).replace('*',chr(0xFF0A)).replace('|',chr(0xFF5C))
        wtdir = './naver webtoon downloader/'+name
        if not os.path.exists(wtdir):
            os.makedirs(wtdir, exist_ok=True)
        print(name+' 추가됨')
        if weekday == 'end':
            YorN = input('지금 다운로드하시겠습니까?\n지금 다운로드하지 않으면 수동으로 다운로드해야 합니다. Y/N: ')
            if (YorN == 'Y') or (YorN == 'y'):
                current = NW_currentEpi(titleId,weekday)
                NW_download(titleId, name, 1 ,current)
        else:
            YorN = input('지금 다운로드하시겠습니까?\n지금 다운로드하지 않으면 00:01에 다운로드됩니다. Y/N: ')
            if (YorN == 'Y') or (YorN == 'y'):
                current = NW_currentEpi(titleId,weekday)
                NW_download(titleId, name, 1 ,current)
    
    def delete_webtoon(self, name):
        self.c.execute('DELETE FROM webtoon_list WHERE name = ?',(name,))
        wtdir = './naver webtoon downloader/'+name
        if os.path.exists(wtdir):
            shutil.rmtree(wtdir)
        print(name+' 삭제됨')

    def match(self, name):
        self.c.execute('SELECT * FROM webtoon_list')
        webtoons = self.c.fetchall()
        for w in webtoons:
            if w[2] == name:
                return True
        return False
    
    def view_list(self):
        self.c.execute('SELECT * FROM webtoon_list')
        webtoons = self.c.fetchall()
        for w in webtoons:
            print(w)
        print('\n')

db = DB()
db.start()


def NW_search(name):
    url = 'https://comic.naver.com/webtoon/weekday.nhn'
    response = urlopen(url)
    as_weekday = BeautifulSoup(response, 'html.parser').select('div.list_area > div.col > div.col_inner > ul')
    for webtoons in as_weekday:
        for webtoon in webtoons.select('li > a'):
            if webtoon.string == name:
                id = webtoon['href'].replace('/webtoon/list.nhn?titleId=','')
                id = id.replace(id[-12:],'')
                weekday = webtoon['href'][-3:]
                return (id, weekday)
    url = 'https://comic.naver.com/webtoon/finish.nhn'
    response = urlopen(url)
    fins = BeautifulSoup(response, 'html.parser').select_one('div.list_area > ul')
    for webtoon in fins.select('li > div.thumb > a'):
        if webtoon['title'] == name:
            return (webtoon['href'].replace('/webtoon/list.nhn?titleId=',''), 'end')
    print("해당되는 웹툰을 찾을 수 없습니다.")
    return time.sleep(1)

def NW_currentEpi(titleId, weekday):
    response = urlopen('https://comic.naver.com/webtoon/list.nhn?titleId='+f'{titleId}'+'&weekday='+weekday)
    soup = BeautifulSoup(response, 'html.parser')
    current = soup.select_one('.viewList > tr > td.title > a')['href']
    current = current.replace(current[-12:],'').replace('/webtoon/detail.nhn?titleId='+f'{titleId}'+'&no=','')
    return int(current)

