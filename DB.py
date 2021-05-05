import sqlite3
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

    def select(self, name):
        self.c.execute('SELECT * FROM webtoon_list WHERE name = ?',(name,))
        return self.c.fetchone()
    
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
            if w[1] == name:
                return True
        return False
    
    def view_list(self):
        self.c.execute('SELECT * FROM webtoon_list')
        webtoons = self.c.fetchall()
        for w in webtoons:
            print(w)
        print('\n')

    def updateRecentEpi(self, name, recentEpi):
        self.c.execute('UPDATE webtoon_list SET recentEpi = ? WHERE name = ?',(recentEpi,name))
    
    def let_0_all(self):
        self.c.execute('SELECT * FROM webtoon_list')
        target_list = self.c.fetchall()
        self.c.execute('UPDATE webtoon_list SET recentEpi = 0')
        return target_list

    def let_0(self, name):
        self.c.execute('UPDATE webtoon_list SET recentEpi = 0 WHERE name = ?',(name,))

    def let_0_except(self, names):
        self.c.execute('SELECT * FROM webtoon_list WHERE recentEpi != 0')
        not_0_list = self.c.fetchall()
        target_list = not_0_list
        for t in not_0_list:
            for n in names:
                if t[1] == n:
                    target_list.remove(t)
        for t in target_list:
            self.let_0(t[1])
        return target_list

    def new_webtoons(self):
        self.c.execute('SELECT * FROM webtoon_list WHERE recentEpi == 0')
        return self.c.fetchall()
    
    # def all(self):
    #     print(self.c.execute('SELECT * FROM webtoon_list WHERE recentEpi != -1'))
    #     self.c.execute('UPDATE webtoon_list SET recentEpi = 0 WHERE recentEpi != -1')
    #     print('1')


db = DB()
db.start()
