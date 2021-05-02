from DB import db

while True:
    mode = input('추가하려면 "a", 삭제하려면 "d", 리스트를 보려면 "l": ')
    if mode == 'a':
        name = input('추가할 웹툰명을 입력. 취소하려면 "c": ')
        if name == 'c':
            continue
        elif db.match(name):
            print('이미 추가된 웹툰입니다.')
        else:
            db.new_webtoon(name)
    elif mode == 'd':
        name = input('삭제할 웹툰명을 입력. 취소하려면 "c": ')
        if name == 'c':
            continue
        elif not db.match(name):
            print('없는 웹툰입니다.')
        else:
            db.delete_webtoon(name)
    elif mode == 'l':
        db.view_list()
    else:
        continue