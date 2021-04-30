from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os
import glob
from PIL import Image
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

class NW_input:
    title = ''
    startEpi = ''
    endEpi = ''
    def put_title(self, string):
        self.title = string
    def put_start(self, string):
        self.startEpi = string
    def put_end(self, string):
        self.endEpi = string

class NW_signal(QObject):
    noMatch = pyqtSignal()
    epiFin = pyqtSignal()
    wtFin = pyqtSignal()
    i = 0
    def no_match(self):
        self.noMatch.emit()
    def epi_fin(self, epi):
        self.i = epi
        self.epiFin.emit()
    def wt_fin(self):
        self.wtFin.emit()

signal = NW_signal()

def download_NW(name, startEpi, endEpi):
    titleId = search(name)
    # 웹툰 디렉터리 생성
    wtdir = './downloads/'+name
    if not os.path.exists(wtdir):
        os.mkdir(wtdir)
    for i in range(int(startEpi), int(endEpi)+1):
        # html에서 필요한부분 가져오기
        response = urlopen(get_url(titleId,f'{i}'))
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.select_one('div.tit_area > div.view > h3').string
        images = soup.find("div", attrs={'class':'wt_viewer'})

        # 각 화별 디렉터리 생성
        epidir = wtdir+f'/{i}. '+title
        if not os.path.exists(epidir):
            os.mkdir(epidir)

        img_url = get_img_url(images)
        num_of_images = get_N_Image(images,titleId,i)
        img_url.lstrip('https://image-comic.pstatic.net/webtoon/')
        # 이미지 다운로드
        for j in range(1,int(num_of_images)+1):
            url = img_url+f'{j}'+'.jpg'
            location = epidir+'/'+f'{j}'.zfill(3)+".jpg"
            urllib.request.urlretrieve(url, location)
        signal.epi_fin(i)
    signal.wt_fin()

# 이미지 주소 찾기
def get_img_url(images):
    img_url = images.find('img', attrs={'id':'content_image_0'})['src']
    return img_url.rstrip('1.jpg')

# 이미지 개수 얻기
def get_N_Image(images,titleId,epi):
    num_of_images = images.find_all('img')[-1]['src'].rstrip('.jpg') \
        .replace('https://image-comic.pstatic.net/webtoon/'+titleId+'/'+f'{epi}'+'/','')
    return num_of_images.replace(num_of_images[0:55], '')

def get_url(titleId, epi):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+titleId+'&no='+epi
    return url

def search(name):
    url = 'https://comic.naver.com/webtoon/weekday.nhn'
    response = urlopen(url)
    weekdays = BeautifulSoup(response, 'html.parser').select('div.list_area > div.col > div.col_inner > ul')
    for weekday in weekdays:
        for webtoon in weekday.select('li > a'):
            if webtoon.string == name:
                id = webtoon['href'].replace('/webtoon/list.nhn?titleId=','')
                return id.replace(id[-12:],'')
    url = 'https://comic.naver.com/webtoon/finish.nhn'
    response = urlopen(url)
    fins = BeautifulSoup(response, 'html.parser').select_one('div.list_area > ul')
    for webtoon in fins.select('li > div.thumb > a'):
        if webtoon['title'] == name:
            return webtoon['href'].replace('/webtoon/list.nhn?titleId=','')
    return signal.no_match()

