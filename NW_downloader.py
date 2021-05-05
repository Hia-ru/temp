from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os
import glob
from DB import db
import time

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

def NW_url(titleId, epi):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+f'{titleId}'+'&no='+f'{epi}'
    return url

def NW_currentEpi(titleId, weekday):
    response = urlopen('https://comic.naver.com/webtoon/list.nhn?titleId='+f'{titleId}'+'&weekday='+weekday)
    soup = BeautifulSoup(response, 'html.parser')
    current = soup.select_one('.viewList > tr > td.title > a')['href']
    current = current.replace(current[-12:],'').replace('/webtoon/detail.nhn?titleId='+f'{titleId}'+'&no=','')
    return int(current)

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

# 이미지 주소 찾기
# def get_img_url(images):
#     img_url = images.find('img', attrs={'id':'content_image_0'})['src']
#     return img_url.replace('1.jpg','')

# 이미지 개수 얻기
def get_N_Image(images):
    num_of_images = 0
    for img in images:
        if img.has_attr('id'):
            if 'content_image_' in img['id']:
                num_of_images = num_of_images +1
    return num_of_images


def NW_download(name):
    try:
        if name[-1] == '.':
            name[-1] == chr(0xFF0E)
        print(name+' 시작\n')
        titleId, weekday = NW_search(name)
        endEpi = NW_currentEpi(titleId,weekday)
        startEpi = db.select(name)[3] + 1
        for i in range(startEpi, endEpi+1):
            # html에서 필요한부분 가져오기
            response = urlopen(NW_url(titleId,i))
            soup = BeautifulSoup(response, 'html.parser')
            title = soup.select_one('div.tit_area > div.view > h3').string
            title = title.replace('?',chr(0xFF1F)).replace('>',chr(0xFF1E))\
                .replace('\\',chr(0xFF3C)).replace('/',chr(0xFF1F))\
                .replace('"',chr(0xFF02)).replace('<',chr(0xFF1C))\
                .replace(':',chr(0xFF1A)).replace('*',chr(0xFF0A))\
                .replace('|',chr(0xFF5C)).replace('...',chr(0x2026))
            images = soup.select('div.wt_viewer > img')
            # 각 화별 디렉터리 생성
            epidir = './naver webtoon downloader/'+name+f'/{i}. '+title
            if not os.path.exists(epidir):
                os.mkdir(epidir)
            # 이미지 다운로드
            print(epidir+'/')
            j=1
            for img in images:
                file_name = f'{j}'.zfill(3)+".jpg"
                location = epidir+'/'+file_name
                if not os.path.exists(location):
                    if img.has_attr('id'):
                        if 'content_image_' in img['id']:
                            url = img['src']
                            urllib.request.urlretrieve(url, location)
                            print('     '+file_name+' <- '+url)
                            j=j+1
            print(name+f' {i}'+f'/{endEpi} 화 완료\n')
            db.updateRecentEpi(name, i)
        print(name+' 완료\n')
    except:
        print('error')
        time.sleep(1)
        
def NW_download_recover(name):
    if name[-1] == '.':
        name[-1] == chr(0xFF0E)
    print(name+' 시작\n')
    titleId, weekday = NW_search(name)
    endEpi = NW_currentEpi(titleId,weekday)
    startEpi = db.select(name)[3] + 1
    for i in range(startEpi, endEpi+1):
        # html에서 필요한부분 가져오기
        response = urlopen(NW_url(titleId,i))
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.select_one('div.tit_area > div.view > h3').string
        title = title.replace('?',chr(0xFF1F)).replace('>',chr(0xFF1E))\
            .replace('\\',chr(0xFF3C)).replace('/',chr(0xFF1F))\
            .replace('"',chr(0xFF02)).replace('<',chr(0xFF1C))\
            .replace(':',chr(0xFF1A)).replace('*',chr(0xFF0A))\
            .replace('|',chr(0xFF5C)).replace('...',chr(0x2026))
        images = soup.select('div.wt_viewer > img')
        # 각 화별 디렉터리 생성
        epidir = './naver webtoon downloader/'+name+f'/{i}. '+title
        if not os.path.exists(epidir):
            os.makedirs(epidir, exist_ok=True)
        # 이미지 다운로드
        print(epidir+'/')
        j=0
        for img in images:
            if img.has_attr('id'):
                if 'content_image_' in img['id']:
                    j=j+1
                    file_name = f'{j}'.zfill(3)+".jpg"
                    location = epidir+'/'+file_name
                    url = img['src']
                    urllib.request.urlretrieve(url, location)
                    print('     '+file_name+' <- '+url)
        print(name+f' {i}'+f'/{endEpi} 화 완료\n')
        db.updateRecentEpi(name, i)
    print(name+' 완료\n')

    

