from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

def NW_url(titleId, epi, weekday):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+titleId+'&no='+epi+'&weekday='+weekday
    return url
titleId = '748105'

def download(name, titleId, weekday, startEpi, endEpi):
    if not os.path.exists('./'+name):
        os.mkdir('./'+name)
    for i in range(startEpi, endEpi+1):
        if not os.path.exists('./'+name+f'/{i}'):
            os.mkdir('./'+name+f'/{i}')
        response = urlopen(NW_url(titleId,f'{i}',weekday))
        soup = BeautifulSoup(response, 'html.parser') 
        images = soup.find("div", attrs={'class':'wt_viewer'})
        img_url = images.find('img', attrs={'id':'content_image_0'})['src']
        img_url = img_url.rstrip('1.jpg')
        num_of_images = images.find_all('img')[-1]['src'].rstrip('.jpg') \
            .replace('https://image-comic.pstatic.net/webtoon/'+titleId+'/'+f'{i}'+'/','')
        num_of_images = num_of_images.replace(num_of_images[0:55], '')
        for j in range(1,int(num_of_images)+1):
            url = img_url+f'{j}'+'.jpg'
            #os.system("curl " + img_url + " > "+f'{j}'.zfill(3)+".jpg")
            location = './'+name+f'/{i}/'+f'{j}'.zfill(3)+".jpg"
            urllib.request.urlretrieve(url, location)
            print(url)
        print('\n')




download('독립일기','748105','sun',1,3)




#할 것
#이미지 이어붙이기
#볼 수 있는 웹페이지 만들기
#봇 만들기or매일 일정시각에 자동실행

# https://image-comic.pstatic.net/webtoon/748105/2/20200617164815_a69974d2a9ccceb2b3cc6bba19be5664_IMAG01_1.jpg
#https://image-comic.pstatic.net/webtoon/748105/85/20210409104026_7aaa78fd7904d2d5eb3e3588d62b5853_IMAG01_1.jpg
# https://image-comic.pstatic.net/webtoon/748105/85/20210409104026_7aaa78fd7904d2d5eb3e3588d62b5853_IMAG01_2.jpg