import sqlite3
from NW_downloader import NW_download
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import glob
import shutil

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
    
    def delete_webtoon(self, name):
        self.c.execute('DELETE FROM webtoon_list WHERE name = ?',(name,))
        wtdir = './naver webtoon downloader/'+name
        if os.path.exists(wtdir):
            shutil.rmtree(wtdir)
        print(name+' 삭제됨')
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
    return print("해당되는 웹툰을 찾을 수 없습니다.")


# 웹툰을 추가하는 쓰레드
# while True:
#     name = input('name or -D: ')
#     if name != '-D':
#         db.new_webtoon(name)
#     elif name == '-D':
#         name = input('name or <-: ')
#         if name != '<-':
#             db.delete_webtoon(name)
#         elif name == '<-':
#             continue
#     continue


