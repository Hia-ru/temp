from NW_downloader import download_NW, NW_input, signal
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QTextBrowser)
from PyQt5.QtGui import QIcon

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    nwi = NW_input()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('제목:'), 0, 0)
        title_input = QLineEdit(self)
        title_input.textChanged[str].connect(self.nwi.put_title)
        grid.addWidget(title_input, 0, 1)
        
        start_input = QLineEdit(self)
        start_input.textChanged[str].connect(self.nwi.put_start)
        grid.addWidget(start_input, 0, 2)
        grid.addWidget(QLabel('화에서'), 0, 3)
        
        end_input = QLineEdit(self)
        end_input.textChanged[str].connect(self.nwi.put_end)
        grid.addWidget(end_input, 0, 4)
        grid.addWidget(QLabel('화까지'), 0, 5)
        
        title_input.returnPressed.connect(self.start_download)
        start_input.returnPressed.connect(self.start_download)
        end_input.returnPressed.connect(self.start_download)

        signal.noMatch.connect(self.no_match)
        signal.epiFin.connect(lambda: self.epi_fin(signal.i))
        signal.wtFin.connect(self.wt_fin)

        self.box = QTextBrowser()
        grid.addWidget(self.box, 1, 0,1, 6)

        self.setWindowTitle('다운로더')
        self.setWindowIcon(QIcon('logo.png'))
        self.move(300, 300)
        self.resize(400, 500)
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def no_match(self):
        self.box.append("해당되는 웹툰을 찾을 수 없습니다.")
    def epi_fin(self, i):
        self.box.append(self.nwi.title+f' {i}화 다운로드 완료\n')
    def wt_fin(self):
        self.box.append(self.nwi.title+' 다운로드 완료\n')

    def start_download(self):
        if not (self.nwi.title == '' and self.nwi.startEpi == '' and self.nwi.endEpi == ''):
            download_NW(self.nwi.title, self.nwi.startEpi, self.nwi.endEpi)
        else:
            self.box.append("입력되지 않은 값이 있습니다.")



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Downloader()
   sys.exit(app.exec_())



# name, startEpi, endEpi = input('이름, 시작화, 끝화: ').split()
# 



#할 것
#볼 수 있는 웹페이지 만들기
#봇 만들기or매일 일정시각에 자동실행
