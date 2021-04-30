from NW_downloader import NW_download

while True:
    print('콤마로 구분. 이름이 정확히 일치해야 함. 화수는 예고편 등을 포함한 전체화수 기준')
    title, start, end = input('웹툰명, 시작화, 끝화: ').split(',')
    NW_download(title,start,end)
