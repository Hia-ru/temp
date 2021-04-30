from NW_downloader import NW_download

while True:
    title, start, end = input('웹툰명 시작화 끝화: ').split()
    NW_download(title,start,end)
