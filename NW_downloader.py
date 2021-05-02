from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os
import glob

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)


def NW_download(titleId, name, startEpi, endEpi):
    for i in range(startEpi, endEpi+1):
        # html에서 필요한부분 가져오기
        response = urlopen(NW_url(titleId,i))
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.select_one('div.tit_area > div.view > h3').string
        title = title.replace('?',chr(0xFF1F)).replace('>',chr(0xFF1E))\
            .replace('\\',chr(0xFF3C)).replace('/',chr(0xFF1F))\
            .replace('"',chr(0xFF02)).replace('<',chr(0xFF1C))\
            .replace(':',chr(0xFF1A)).replace('*',chr(0xFF0A)).replace('|',chr(0xFF5C))
        images =soup.find("div", attrs={'class':'wt_viewer'})
        # 각 화별 디렉터리 생성
        epidir = '.\\naver webtoon downloader\\'+name+f'\\{i}. '+title
        if not os.path.exists(epidir):
            os.mkdir(epidir)
        # 이미지 다운로드
            img_url = get_img_url(images)
            num_of_images = get_N_Image(images,titleId,i)
            print(epidir+'/')
            for j in range(1,num_of_images+1):
                url = img_url+f'{j}'+'.jpg'
                file_name = f'{j}'.zfill(3)+".jpg"
                location = epidir+'/'+file_name
                urllib.request.urlretrieve(url, location)
                print('     '+file_name+' <- '+url)
            print(name+f' {i}화 다운로드 완료\n')
    print(name+' 다운로드 완료\n')
        

# 이미지 주소 찾기
def get_img_url(images):
    img_url = images.find('img', attrs={'id':'content_image_0'})['src']
    return img_url.rstrip('1.jpg')

# 이미지 개수 얻기
def get_N_Image(images,titleId,epi):
    num_of_images = images.find_all('img')[-1]['src'].rstrip('.jpg') \
        .replace('https://image-comic.pstatic.net/webtoon/'+f'{titleId}'+'/'+f'{epi}'+'/','')
    return int(num_of_images.replace(num_of_images[0:55], ''))

def NW_url(titleId, epi):
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+f'{titleId}'+'&no='+f'{epi}'
    return url
