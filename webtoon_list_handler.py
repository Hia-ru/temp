from DB import db
from NW_downloader import NW_download, NW_search, NW_download_recover
import os

def new_webtoon(db, name):
    try:
        titleId, weekday = NW_search(name)
    except:
        return 1
    if name[-1] == '.':
        name[-1] == chr(0xFF0E)
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

def split_well(string):
    comma = chr(0xFE50)
    ps = string.replace(chr(0x005C)+',',comma).split(',')
    i=0
    for p in ps:
        if comma in p:
            ps[i] = p.replace(comma,',')
            i=i+1
    return ps

while True:
    mode = input('추가하려면 "a", 삭제하려면 "r", 리스트를 보려면 "l", 다운로드 "d", 중간에 종료시"0": ').strip()
    if mode == 'a':
        while True:
            names = input('\n추가할 웹툰명을 입력, 콤마로 구분. 취소하려면 "c", 리스트를 보려면 "l": ').strip()
            names = split_well(names)
            if names[0] == 'c':
                break
            elif names[0] == 'l':
                db.view_list()
            else:
                for name in names:
                    if db.match(name) == True:
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
        name = input('삭제할 웹툰명을 입력. 취소하려면 "c", 리스트를 보려면 "l": ').strip()
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
        while True:
            i = input('체크할 웹툰 입력 or "all", 콤마로 구분. 제외할 웹툰은"e": 취소하려면 "c", 리스트를 보려면 "l": ').strip()
            i = split_well(i)
            if i[0] == 'all':
                target_list = db.let_0_all()
                for t in target_list:
                    NW_download_recover(t[1])
            elif i[0] == 'c':
                break
            elif i[0] == 'l':
                db.view_list()
            elif i[0] == 'e':
                while True:
                    e = input('제외할 웹툰명을 입력. 콤마로 구분. 취소하려면 "c", 리스트를 보려면 "l": ').strip()
                    e = split_well(e)
                    if e[0] == 'c':
                        break
                    elif e[0] == 'l':
                        db.view_list()
                    else:
                        target_list = db.let_0_except(e)
                        for name in target_list:
                            NW_download_recover(name[1])
            else:
                for name in i:
                    name = name.strip()
                    if not db.match(name):
                        print(f'{name}: 리스트에 없는 웹툰입니다.')
                    else:
                        db.let_0(name)
                        NW_download_recover(name)
    elif mode == 'd':
        while True:
            names = input('다운할 웹툰명을 입력. 콤마로 구분. 새로 추가한 웹툰 다운은 "n" 취소하려면 "c", 리스트를 보려면 "l": ').strip()
            names = split_well(names)
            if names[0] == 'c':
                break
            elif names[0] == 'l':
                db.view_list()
            elif names[0] == 'n':
                w = db.new_webtoons()
                for n in w:
                    NW_download(n[1])
            else:
                for name in names:
                    name = name.strip()
                    if not db.match(name):
                        print(f'{name}: 리스트에 없는 웹툰입니다.')
                    else:
                        NW_download(name)
    else:
        continue


