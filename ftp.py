import ftplib
import sys
from ftplib import FTP
from PyQt5.QtWidgets import *
from widget import Ui_Form

ftp = ftplib.FTP
current_file = ''
file_list = {}



def Pwd():
    print(ftp.pwd())


def refresh_list():
    global file_list
    file_list = {}
    ui.listWidget.clear()
    lines = ftp.dirs()
    for i, val in enumerate(lines):
        file_list[i] = val[39:]
        ui.listWidget.addItem(val)


def login_ftp():
    global ftp
    server = ui.ledit_ip.text()
    ftp = FTP(server)
    username = ui.ledit_name.text()
    password = ui.ledit_passwd.text()
    ftp.login(username, password)
    if ftp.getwelcome() is not None:
        ui.btn_delete.setEnabled(True)
        ui.btn_delete_all.setEnabled(True)
        ui.btn_download.setEnabled(True)
        ui.btn_download_all.setEnabled(True)
        ui.btn_login.setEnabled(False)
        refresh_list()


def get_file_name():
    global current_file
    current_file = ''
    current_file = ui.listWidget.currentItem().text()[39:]
    print(current_file)


def download():
    print(len(current_file))
    if len(current_file):
        result = ftp.retrbinary('RETR %s' % current_file, open(current_file, 'wb').write, bufsize)
        print(result)


def download_all():
    if len(file_list):
        print(len(file_list))
        for i, val in enumerate(file_list):
            result = ftp.retrbinary('RETR %s' % file_list[val], open(file_list[val], 'wb').write, bufsize)
            print(result)


def delete_file():
    global current_file
    if len(current_file):
        ftp.delete(current_file)
        refresh_list()
        current_file = ''


def delete_all():
    for i, val in enumerate(file_list):
        ftp.delete(file_list[val])
    refresh_list()


if __name__ == "__main__":
    bufsize = 10240
    app = QApplication(sys.argv)
    main = QWidget()
    ui = Ui_Form()
    ui.setupUi(main)

    ui.btn_delete.setEnabled(False)
    ui.btn_delete_all.setEnabled(False)
    ui.btn_download.setEnabled(False)
    ui.btn_download_all.setEnabled(False)

    ui.btn_login.clicked.connect(login_ftp)
    ui.btn_refre.clicked.connect(refresh_list)
    ui.btn_delete.clicked.connect(delete_file)
    ui.btn_delete_all.clicked.connect(delete_all)
    ui.listWidget.clicked.connect(get_file_name)
    ui.btn_download.clicked.connect(download)
    ui.btn_download_all.clicked.connect(download_all)

    main.show()
    sys.exit(app.exec_())
