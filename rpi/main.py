import sys

import socketio
from worker import Worker
from PyQt5.QtCore import QThread, QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QHBoxLayout, QLabel, QVBoxLayout, QWidget

sio = socketio.Client()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Python")
        self.showFullScreen()
        # setting geometry
        resolution = QDesktopWidget().screenGeometry(-1)
        screenWidth = resolution.width()
        screenHeight = resolution.height()
        self.setGeometry(0, 0, screenWidth, screenHeight)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()

    def UiComponents(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()

        self.label = QLabel()
        self.label.setText('#: ')
        self.label.setFixedHeight(20)

        self.label2 = QLabel()
        self.label2.setText('CÓDIGO: ______')   
        self.label2.setFixedHeight(20)

        hbox.addWidget(self.label, alignment=Qt.AlignLeft)
        hbox.addWidget(self.label2, alignment=Qt.AlignRight)

        vbox.addLayout(hbox)

        self.webEngineView = QWebEngineView()
        self.navigate_to_url('https://sostaskillbox.it/')
        vbox.addWidget(self.webEngineView)

        self.setLayout(vbox)
        self.show()

        self.thread = QThread()
        self.worker = Worker(self, sio)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.url_changed.connect(self.navigate_to_url)
        self.worker.message.connect(self.notify)
        self.worker.room.connect(self.room_name)

        self.thread.start()

    def navigate_to_url(self, page): # Does not receive the Url
        self.webEngineView.setUrl(QUrl(page))

    def notify(self, message):
        self.label.setText('#: {}'.format(message))

    def room_name(self, room): 
        self.label2.setText('CÓDIGO: {}'.format(room))


    def closeEvent(self, event):
        # sio.emit('close', {})
        # sio.disconnect()
        event.ignore() # let the window close

def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sio.emit('close', {})
        sio.disconnect()
        print(e.message)