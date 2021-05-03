from DB import db
from NW_downloader import NW_download, NW_search
import os

def new_webtoon(db, name):
    try:
        titleId, weekday = NW_search(name)
    except:
        return 1
    db.insert(titleId, name, weekday, 0)
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
        YorN = input('지금 다운로드하시겠습니까?\n지금 다운로드하지 않으면 수동으로 다운로드해야 합니다. Y/N: ').strip()
        if (YorN == 'Y') or (YorN == 'y'):
            NW_download(name)
    else:
        YorN = input('지금 다운로드하시겠습니까?\n지금 다운로드하지 않으면 00:01에 다운로드됩니다. Y/N: ').strip()
        if (YorN == 'Y') or (YorN == 'y'):
            NW_download(name)
    return 0


while True:
    mode = input('추가하려면 "a", 삭제하려면 "r", 리스트를 보려면 "l", 다운로드 "d", 화수 초기화"0": ').strip()
    if mode == 'a':
        while True:
            name = input('추가할 웹툰명을 입력. 취소하려면 "c", 리스트를 보려면 "l": ').strip()
            if name == 'c':
                break
            elif name == 'l':
                db.view_list()
            elif db.match(name) == True:
                opt = input('이미 추가된 웹툰입니다. 다운하려면 "d". 취소하려면 "c": ').strip()
                if opt == 'd':
                    NW_download(name)
                else:
                    continue
            else:
                #예외처리
                if 1 == new_webtoon(db, name):
                    print("다시 입력하세요.")
    elif mode == 'r':
        name = input('삭제할 웹툰명을 입력. 취소하려면 "c", 리스트를 보려면 "l": ').rstrip()
        if name == 'c':
            continue
        elif name == 'l':
            db.view_list()
        elif not db.match(name):
            print('없는 웹툰입니다.')
        else:
            db.delete_webtoon(name)
    elif mode == 'l':
        db.view_list()
    elif mode == '0':
        i = input('초기화 할 웹툰 입력 or "all": ').strip()
        if i == 'all':
            db.let_0_all()
        elif not db.match(name):
            print('없는 웹툰입니다.')
        else:
            db.let_0(i)
    elif mode == 'd':
        while True:
            name = input('다운할 웹툰명을 입력. 취소하려면 "c", 리스트를 보려면 "l": ').strip()
            if name == 'c':
                break
            elif name == 'l':
                db.view_list()
            elif not db.match(name):
                print('없는 웹툰입니다.')
            else:
                NW_download(name)
    else:
        continue

