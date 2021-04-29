from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os
import glob
from PIL import Image

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

def NW_url(titleId, epi, weekday):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+titleId+'&no='+epi+'&weekday='+weekday
    return url
titleId = '748105'

def download(name, titleId, weekday, startEpi, endEpi):
    # 웹툰 디렉터리 생성
    wtdir = './downloads/'+name
    if not os.path.exists(wtdir):
        os.mkdir(wtdir)
    for i in range(startEpi, endEpi+1):
        # 각 화별 디렉터리 생성
        epidir = wtdir+f'/{i}'
        if not os.path.exists(epidir):
            os.mkdir(epidir)

        # html에서 필요한부분 가져오기
        response = urlopen(NW_url(titleId,f'{i}',weekday))
        images = BeautifulSoup(response, 'html.parser').find("div", attrs={'class':'wt_viewer'})
        #images = soup.find("div", attrs={'class':'wt_viewer'})

        img_url = get_img_url(images)
        num_of_images = get_N_Image(images,i)
        # 이미지 다운로드
        for j in range(1,int(num_of_images)+1):
            url = img_url+f'{j}'+'.jpg'
            location = epidir+'/'+f'{j}'.zfill(3)+".jpg"
            urllib.request.urlretrieve(url, location)
            print(url)
        print('\n')

# 이미지 주소 찾기
def get_img_url(images):
    img_url = images.find('img', attrs={'id':'content_image_0'})['src']
    return img_url.rstrip('1.jpg')

# 이미지 개수 얻기
def get_N_Image(images,epi):
    num_of_images = images.find_all('img')[-1]['src'].rstrip('.jpg') \
        .replace('https://image-comic.pstatic.net/webtoon/'+titleId+'/'+f'{epi}'+'/','')
    return num_of_images.replace(num_of_images[0:55], '')


download('독립일기','748105','sun',1,3)




#할 것
#이름입력만으로 다운로드 가능하도록 수정
#볼 수 있는 웹페이지 만들기
#봇 만들기or매일 일정시각에 자동실행
