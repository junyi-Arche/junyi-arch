import csv
import re
import datetime
import sys
import threading
import time
import pandas as pd
from queue import Queue
from time import sleep
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QThread, pyqtSlot, Qt, QDate
from PyQt5.QtGui import QFont, QTextOption, QStandardItemModel, QStandardItem, QClipboard
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QApplication, QScrollArea, QLabel, QDateEdit, \
    QPlainTextEdit, QTableView, QAbstractItemView, QHeaderView, QDialog, QVBoxLayout, QAction, QFileDialog, QMessageBox
from bs4 import BeautifulSoup
from loguru import logger
from pyecharts.charts import Bar, Line, Page, Pie
import dm_pb2
import os
import requests
from functools import partial
import sqlite3
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from wordcloud import WordCloud as WC
from pyecharts.globals import SymbolType, CurrentConfig


class StartWork(QThread):
    MesSignal = QtCore.pyqtSignal(dict)
    threadStarted = QtCore.pyqtSignal()  # 自定义线程启动信号
    threadFinished = QtCore.pyqtSignal(list)  # 自定义线程结束信号
    headers = {
        "authority": "www.bilibili.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.bilibili.com/",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    def __init__(self, burl, start, end):
        super().__init__()
        self.bvid = ''
        self.bvurl = burl
        self.start_t = start
        self.end_t = end
        self.date_list = []
        self.dmdategeturl = 'https://api.bilibili.com/x/v2/dm/history/index?month={}&type=1&oid={}'
        self.pubtime = None

    def run(self):
        self.threadStarted.emit()  # 发送线程启动信号
        try:
            self.getBvid()
            self.time_set()
        except Exception as e:
            self.MesSignal.emit({'type': 'log', 'fail': True, 'msg': str(e)})
        logger.info(self.date_list)
        self.threadFinished.emit(['start'])

    def getBvid(self):
        main_html = requests.get(self.bvurl, headers=self.headers, cookies=Cookies)
        response = main_html.text
        regx = r'.*<script>window.__INITIAL_STATE__=(.*?)</script>.*'
        regx2 = r'.*"cids":\{"1":(.*?)}.*'
        regx3 = r'.*<script>window.__playinfo__=(.*?)</script>.*'
        regx4 = r'.*"timelength":(.*?),.*'
        playinfo = re.findall(regx, response)[0]
        bvid = re.findall(regx2, playinfo)[0]
        playinfo2 = re.findall(regx3, response)[0]
        timelength = int(re.findall(regx4, playinfo2)[0]) / 1000
        beautifulsoup = BeautifulSoup(response, 'lxml')
        self.pubtime = beautifulsoup.find('span', {'class': 'pubdate-text'}).get_text().strip()
        bvtitle = beautifulsoup.find('h1', {'class': 'video-title'}).get_text().strip()
        # 删除不允许的字符
        bvtitle = re.sub(r'[\\/*?:"<>|]', '', bvtitle)

        # 替换空格和其他特殊字符
        bvtitle = bvtitle.replace(' ', '')
        self.MesSignal.emit({'type': 'info',
                             'msg': '视频名称：{}, 视频长度：{}, 发布时间：{}'.format(bvtitle, self.getMVlength(timelength),
                                                                       self.pubtime)})
        self.bvid = bvid
        MainWindow.bvid = bvid
        MainWindow.bvtitle = bvtitle
        MainWindow.bvpubtime = self.pubtime
        MainWindow.bvlength = timelength
        Headers['Referer'] = self.bvurl

    def getMVlength(self, tim):
        if tim < 3600:
            return '{}分钟'.format(round(tim / 60))
        else:
            t = '{:.2f}'.format(tim / 3600).split('.')
            if int(t[1]) >= 60:
                h = int(t[1]) // 60
                m = int(t[1]) % 60

                t = '{}小时{}分钟'.format(int(t[0]) + h, m)
                return t
            else:
                return '{}小时{}分钟'.format(t[0], t[1])

    def time_set(self):
        begindateStamp = datetime.datetime.strptime(str(self.start_t), '%Y-%m-%d').timestamp()
        lastdateStamp = datetime.datetime.strptime(str(self.end_t), '%Y-%m-%d').timestamp()
        bv_pubtime = datetime.datetime.strptime(self.pubtime[:10], '%Y-%m-%d').timestamp()
        if bv_pubtime > begindateStamp:
            self.MesSignal.emit({'type': 'log', 'fail': True, 'msg': '开始时间不能小于视频发布时间'})
            return
        if not os.path.exists('./弹幕数据'):
            os.mkdir('弹幕数据')
        if not os.path.exists('./so文件'):
            os.mkdir('so文件')
        y, m, d = [int(i) for i in str(self.start_t).split('-')]
        y1, m1, d1 = [int(i) for i in str(self.end_t).split('-')]
        while True:
            self.date_list.append('{}-{:02d}'.format(y, m))
            if y < y1:
                if m < 12:
                    m += 1
                elif m == 12:
                    y += 1
                    m = 1
            elif y == y1:
                if m < m1:
                    m += 1
                else:
                    break

        for t in self.date_list:
            sleep(1)
            dateres = requests.get(self.dmdategeturl.format(t, self.bvid), cookies=Cookies, headers=self.headers)
            print(dateres.text)
            if dateres.status_code == 200:
                dateres = dateres.json().get('data')
                if dateres:
                    for d in dateres:
                        if begindateStamp <= datetime.datetime.strptime(d, '%Y-%m-%d').timestamp() <= lastdateStamp:
                            MainWindow.date_ableq.put(d)
        if MainWindow.date_ableq.qsize() == 0:
            self.MesSignal.emit({'type': 'info', 'msg': '所选时间没有评论内容'})


class Dmdatasogetter(QThread):
    getso_singal = QtCore.pyqtSignal(dict)
    threadStarted = QtCore.pyqtSignal()
    threadFinished = QtCore.pyqtSignal(list)

    def __init__(self, a, b, c, d, e):
        super().__init__()
        self.bvid = a
        self.dmdataurl = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={}&date='
        self.proxyurl = 'https://sch.shanchendaili.com/api.html?action=get_ip&key=HU086e4a5c0804070028Y3LH&time=5&count=1&protocol=http&type=json&only=1'
        self.date_ableq = b
        self.date_urlq = c
        self.sofileq = d
        self.proxy = None
        self.proxyTime = None
        self.remainTime = None
        self.stop_parseSO = e

    def run(self):
        self.threadStarted.emit()
        while True:
            if self.date_ableq.empty():
                break
            date = self.date_ableq.get()
            self.date_urlq.put(self.dmdataurl.format(self.bvid) + date)
        self.sendrequest()
        self.threadFinished.emit(['dmget'])

    def sendrequest(self):
        while True:
            if self.date_urlq.empty():
                self.stop_parseSO.set()
                break
            else:
                content_url = self.date_urlq.get()
                for i in range(4):
                    if self.proxyTime:
                        if int(time.time()) - self.proxyTime > self.remainTime:
                            self.proxy = None
                            self.proxyTime = None
                    file_name = ''
                    try:
                        sleep(1)
                        if self.proxy is not None:
                            res_bytes = requests.get(url=content_url, cookies=Cookies, headers=Headers, timeout=10,
                                                     proxies={'http': self.proxy, 'hppts': self.proxy}).content
                        else:
                            res_bytes = requests.get(url=content_url, cookies=Cookies, headers=Headers, timeout=10).content
                        file_name = content_url[-10:] + '.so'
                        with open('./so文件/' + file_name, 'wb') as f:
                            f.write(res_bytes)
                        self.sofileq.put(file_name)
                        self.getso_singal.emit({'type': 'info', 'msg': f'{file_name}文件保存成功！！！！'})
                        break
                    except requests.exceptions.Timeout:
                        # 超时错误
                        self.getso_singal.emit({'type': 'log', 'msg': f'{file_name}请求超时！！！'})
                        continue
                    except Exception as e:
                        self.getso_singal.emit({'type': 'log', 'msg': f'{file_name}请求失败！！！'})
                        self.getProxy()
                        self.getso_singal.emit({'type': 'log', 'msg': f'{file_name}refetch'})
                        print(f'{file_name}refetch')
                        with open('.error.txt', 'a+', encoding='utf-8') as f:
                            f.write(
                                str(file_name) + f' 抓取失败 {e} - Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
                        continue

    def getProxy(self):
        try:
            data = requests.get(self.proxyurl).json()
            proxy = data['list']
            self.proxy = proxy['sever'] + ':' + proxy['port']
            if not self.remainTime:
                self.remainTime = re.match(r'time=(.*)', self.proxyurl).group(1)
            self.proxyTime = int(time.time())
            self.getso_singal.emit({'type': 'info', 'msg': f'获取到代理: {proxy}'})
        except Exception as e:
            self.getso_singal.emit({'type': 'log', 'msg': e})


class ParseSo(QThread):
    threadStarted = QtCore.pyqtSignal()
    threadFinished = QtCore.pyqtSignal(list)

    def __init__(self, a, b, c, d):
        super().__init__()
        self.data = a
        self.sofile = b
        self.stop_e = c
        self.stop_download = d

    def run(self):
        self.threadStarted.emit()
        while True:
            if self.stop_e.is_set() and self.sofile.empty():
                self.stop_download.set()
                break
            try:
                file_name = self.sofile.get_nowait()
                with open('./so文件/' + file_name, 'rb') as f:
                    data = f.read()
                anadm = dm_pb2.DmSegMobileReply()
                anadm.ParseFromString(data)
                for dm_msg in anadm.elems:
                    stime, date = self.handleTime(dm_msg.stime, dm_msg.date)
                    data = [stime, date, dm_msg.text, dm_msg.mode, dm_msg.weight, dm_msg.color, dm_msg.size,
                            dm_msg.uhash,
                            dm_msg.dmid]
                    self.data.put(data)
                os.remove('./so文件/' + file_name)
            except:
                pass
        self.threadFinished.emit(['parse', str(self)])

    def handleTime(self, ms, timestamp):
        seconds = ms / 1000
        m, s = divmod(seconds, 60)
        stime = '{:02d}:{:02d}'.format(int(m), int(s))
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M')
        return stime, date


class Download(QThread):
    threadStarted = QtCore.pyqtSignal()
    threadFinished = QtCore.pyqtSignal(list)
    d_singal = QtCore.pyqtSignal(dict)

    def __init__(self, a, b, c, d, e, f):
        super().__init__()
        self.index = a
        self.data = b
        self.sofile = c
        self.event = d
        self.stop_e = e
        self.merge_e = f

    def run(self):
        self.threadStarted.emit()
        j = 0
        while True:
            if self.data.empty() and self.sofile.empty() and self.stop_e.isSet():
                self.event.clear()
                self.merge_e.set()
                break
            data = self.data.get()
            j += 1
            with open('./弹幕数据/dm{}.csv'.format(self.index), 'a+', newline='', encoding='utf-8') as g:
                writer = csv.writer(g)
                writer.writerow(data)
            if j % 100 == 0:
                self.d_singal.emit({'type': 'info', 'msg': 'dm{}.csv已保存100条数据'.format(self.index)})
        self.threadFinished.emit(['download', str(self)])


class Merge(QThread):
    threadStarted = QtCore.pyqtSignal()
    threadFinished = QtCore.pyqtSignal(list)
    m_singal = QtCore.pyqtSignal(dict)

    def __init__(self, a, b, c, d):
        super().__init__()
        self.merge_e = a
        self.event2 = b
        self.lines_seen = set()  # 用于记录出现过的行
        self.file_path = d
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        self.file_name = f'{c}.csv'

    def remove_duplicates(self):
        with open('data/combined_file.csv', 'r', newline='', encoding='utf-8') as file_in, open(
                self.file_path + self.file_name, 'w',
                newline='',
                encoding='utf-8') as file_out:
            reader = csv.reader(file_in)
            writer = csv.writer(file_out)
            for row in reader:
                row_str = ','.join(row)  # 将行内容转换成字符串，以逗号分隔（可根据实际情况修改分隔符）
                if row_str not in self.lines_seen:
                    writer.writerow(row)
                    self.lines_seen.add(row_str)
        self.m_singal.emit({'type': 'info', 'msg': f'数据合并完成, 文件名称: {self.file_name}'})

    def run(self):
        self.threadStarted.emit()
        self.merge_e.wait()
        self.m_singal.emit({'type': 'info', 'msg': '开始合并文件'})
        combined_csv = pd.DataFrame()
        column_names = ['Time', 'Date', 'Comment', 'Mode', 'Weight', 'Color', 'Size', 'Uhash', 'Dmid']
        filelist = os.listdir('./弹幕数据')
        for file in filelist:
            df = pd.read_csv('./弹幕数据/' + file, skip_blank_lines=True, names=column_names)
            combined_csv = pd.concat([combined_csv, df])
            os.remove('./弹幕数据/' + file)
        combined_csv.to_csv(self.file_path + 'combined_file.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
        self.remove_duplicates()
        self.merge_e.clear()
        self.event2.clear()
        os.rmdir('弹幕数据')
        os.rmdir('so文件')
        self.threadFinished.emit(['merge', len(self.lines_seen)])


class MainWindow(QMainWindow):
    bvid = ''
    bvtitle = ''
    bvlength = 0
    bvpubtime = ''
    save_file_path = ''
    date_ableq = Queue(500)
    date_urlq = Queue(500)
    sofileq = Queue(500)
    dataq = Queue(8000)
    threadEvent = threading.Event()
    threadEvent2 = threading.Event()
    mergeevent = threading.Event()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    font = QFont()
    font.setPointSize(12)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('bilibili.ui', self)
        self.startbtn = self.findChild(QPushButton, "start")
        self.startbtn.clicked.connect(self.start_spider)
        self.analy_btn = self.findChild(QPushButton, 'analy')
        self.analy_btn.clicked.connect(self.show_analy)
        self.burl = self.findChild(QLineEdit, "burl")
        self.log_area = self.findChild(QScrollArea, "logarea")
        self.log_text = QPlainTextEdit()
        self.info_area = self.findChild(QScrollArea, "infoarea")
        self.info_text = QPlainTextEdit()
        self.startDate = self.findChild(QDateEdit, "dateEdit")
        self.endDate = self.findChild(QDateEdit, "dateEdit_2")
        self.reset_time = self.findChild(QPushButton, "resetTime")
        self.reset_time.clicked.connect(self.time_reset)
        self.history_area = self.findChild(QTableView, 'historylog')
        self.history_datamodel = QStandardItemModel()
        self.select_history = self.findChild(QLabel, 'selecthis')
        self.delhistory = self.findChild(QPushButton, 'delselect')
        self.file_select = self.findChild(QPushButton, 'fileselect')
        self.file_select.clicked.connect(self.file_sel)
        self.init_view()
        self.time_ok = True
        self.start_thread = None
        self.spider_thread = None
        self.parse_num = 2
        self.parsers = {}
        self.load_num = 3
        self.loads = {}
        self.merge = None
        self.thread_count = 0
        self.file_path_act = self.findChild(QAction, 'filepath_2')
        self.file_path_act.triggered.connect(partial(self.handle_menu, 'filepath'))
        self.change_path_act = self.findChild(QAction, 'changefilepath')
        self.change_path_act.triggered.connect(partial(self.handle_menu, 'change'))

    def handle_menu(self, txt):
        if txt == 'filepath':
            if self.save_file_path:
                filepath = self.save_file_path
            else:
                filepath = os.getcwd() + '\\data'
            msg = QDialog(self)
            msg.setWindowTitle('保存地址')
            layout = QVBoxLayout()
            label = QLabel(filepath)
            label.setFont(self.font)
            layout.addWidget(label)
            button = QPushButton("复制文本")
            button.clicked.connect(partial(self.copy_filepath, filepath))
            layout.addWidget(button)
            msg.setLayout(layout)
            msg.exec_()
        elif txt == 'change':
            folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
            if folder_path:
                self.save_file_path = folder_path + '/'

    def copy_filepath(self, path):
        clipboard = QApplication.clipboard()
        clipboard.setText(path, QClipboard.Clipboard)

    def on_selection_change(self, row):
        item = self.history_datamodel.item(row, 2)
        self.bvlength = float(self.history_datamodel.item(row, 3).text())
        self.select_history.setText(os.getcwd() + '\\data\\' + item.text() + '.csv')
        self.delhistory.clicked.connect(self.del_history)

    def init_view(self):
        self.history_datamodel.setHorizontalHeaderLabels(
            ['时间', '弹幕总数', '视频标题', '视频长度', '弹幕开始日期', '弹幕结束日期', '发布时间', '视频地址'])
        self.history_area.setModel(self.history_datamodel)
        self.history_area.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置表格可伸缩
        self.history_area.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_area.clicked.connect(lambda index: self.on_selection_change(index.row()))
        self.history_area.verticalHeader().sectionClicked.connect(self.on_selection_change)
        # 获取水平标头
        horizontal_header = self.history_area.horizontalHeader()
        # 设置行宽可根据内容自动调整
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # 设置字体大小为16像素

        self.log_text.setFont(self.font)
        self.log_text.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.log_text.setReadOnly(True)
        # 使用 ensureCursorVisible() 方法确保光标可见，从而将视图滚动到文本框的底部
        self.log_text.ensureCursorVisible()
        self.log_area.setWidget(self.log_text)

        self.info_text.setFont(self.font)
        self.info_text.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.info_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.info_text.setReadOnly(True)
        self.info_text.ensureCursorVisible()
        self.info_area.setWidget(self.info_text)
        self.startDate.dateChanged.connect(partial(self.on_date_changed, 'startDate'))
        self.endDate.dateChanged.connect(partial(self.on_date_changed, 'endDate'))

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history 
               (id TEXT PRIMARY KEY UNIQUE, timestamp TIMESTAMP, sum INTEGER, title TEXT,bvlength TIME, startTime TEXT, endTime TEXT, pubdate TEXT, bvurl TEXT);
               ''')
        self.update_history()

    def update_history(self):
        self.cursor.execute('''select * from history''')
        data = self.cursor.fetchall()
        if data:
            for d in data:
                row_items = [QStandardItem(str(item)) for item in d[1:]]
                self.history_datamodel.appendRow(row_items)

    def del_history(self):
        title = self.select_history.text().split('\\')[-1].split('.csv')[0]
        self.cursor.execute('''DELETE FROM history where title="%s"''' % title)
        self.conn.commit()
        rows_to_delete = []
        for row in range(self.history_datamodel.rowCount()):
            index = self.history_datamodel.index(row, 2)
            value = index.data()
            if title in value:
                rows_to_delete.append(row)
        # 删除行
        for row in rows_to_delete:
            self.history_datamodel.removeRow(row)
        # 更新视图
        self.history_area.update()
        self.select_history.setText('')

    def file_sel(self):
        self.bvlength = 0
        file_path = QFileDialog.getOpenFileUrl(self, '选择文件')
        if file_path:
            self.select_history.setText(file_path[0].toLocalFile())

    def time_reset(self):
        self.endDate.setDate(QDate.currentDate())
        self.startDate.setDate(QDate.currentDate())

    @pyqtSlot(QDate)
    def on_date_changed(self, t, date):
        selected_time = datetime.datetime.combine(date.toPyDate(), datetime.time()).timestamp()
        if t == 'startDate':
            end_date = self.endDate.date().toPyDate()
            timestamp = datetime.datetime.combine(end_date, datetime.time()).timestamp()
            if timestamp < selected_time:
                self.time_ok = False
            else:
                self.time_ok = True
        elif t == 'endDate':
            start_date = self.startDate.date().toPyDate()
            timestamp = datetime.datetime.combine(start_date, datetime.time()).timestamp()
            if timestamp > selected_time:
                self.time_ok = False
            else:
                self.time_ok = True

    def start_spider(self):
        if self.burl.text() != '':
            if 'bilibili' not in self.burl.text():
                self.Slot({'type': 'log', 'msg': '请输入正确的b站视频url'})
                return
            else:
                if self.time_ok:
                    self.startbtn.disconnect()
                    self.reset_time.disconnect()
                    self.burl.setReadOnly(True)
                    self.startDate.setReadOnly(True)
                    self.endDate.setReadOnly(True)
                    self.start_thread = StartWork(self.burl.text(), self.startDate.date().toPyDate(),
                                                  self.endDate.date().toPyDate())
                    self.start_thread.MesSignal.connect(self.Slot)
                    self.start_thread.threadStarted.connect(self.onThreadStarted)
                    self.start_thread.threadFinished.connect(self.onThreadFinished)
                    self.start_thread.start()
                else:
                    self.Slot({'type': 'log', 'msg': '请输入正确的时间范围'})
        else:
            self.Slot({'type': 'log', 'msg': '请输入b站视频url'})

    @pyqtSlot(dict)
    def Slot(self, msg):
        t = msg.get('type')
        if t == 'log':
            if msg.get('fail'):
                self.burl.setReadOnly(False)
                self.startDate.setReadOnly(False)
                self.endDate.setReadOnly(False)
                self.startbtn.clicked.connect(self.start_spider)
                self.reset_time.clicked.connect(self.time_reset)
            self.log_text.appendPlainText('[*]' + msg.get('msg'))
        elif t == 'info':
            self.info_text.appendPlainText('[*]' + msg.get('msg'))

    def show_analy(self):
        if self.select_history.text():
            self.ui = DManalyUi(self.select_history.text(), self.bvlength)
            if os.path.exists(self.select_history.text()):
                try:
                    self.ui.setupUi()
                except:
                    self.ui.File_not_fund('无法对该文件进行分析')
                    return
            else:
                self.ui.File_not_fund('文件不存在！')
                return
            self.ui.show()
            self.ui.closed.connect(self.on_window_closed)

    def on_window_closed(self):
        # 执行线程关闭操作
        print("Window closed")

    # 槽函数，处理子线程启动信号
    @pyqtSlot()
    def onThreadStarted(self):
        self.thread_count += 1
        print(f"子线程启动，当前线程数量：{self.thread_count}")

    # 槽函数，处理子线程结束信号
    @pyqtSlot(list)
    def onThreadFinished(self, data):
        if data[0] == 'start':
            if MainWindow.date_ableq.qsize() != 0:
                self.spider_thread = Dmdatasogetter(self.bvid, self.date_ableq, self.date_urlq, self.sofileq,
                                                    self.threadEvent)
                self.spider_thread.threadStarted.connect(self.onThreadStarted)
                self.spider_thread.threadFinished.connect(self.onThreadFinished)
                self.spider_thread.getso_singal.connect(self.Slot)
                self.spider_thread.start()
                for i in range(self.parse_num):
                    parser = ParseSo(self.dataq, self.sofileq, self.threadEvent, self.threadEvent2)
                    parser.threadStarted.connect(self.onThreadStarted)
                    parser.threadFinished.connect(self.onThreadFinished)
                    parser.start()
                    self.parsers[str(parser)] = parser
                for i in range(self.load_num):
                    load = Download(i, self.dataq, self.sofileq, self.threadEvent, self.threadEvent2,
                                    self.mergeevent)
                    load.threadStarted.connect(self.onThreadStarted)
                    load.threadFinished.connect(self.onThreadFinished)
                    load.d_singal.connect(self.Slot)
                    load.start()
                    self.loads[str(load)] = load
                if self.save_file_path:
                    self.merge = Merge(self.mergeevent, self.threadEvent2, self.bvtitle, self.save_file_path)
                else:
                    self.merge = Merge(self.mergeevent, self.threadEvent2, self.bvtitle, os.getcwd() + '\\data\\')
                self.merge.threadStarted.connect(self.onThreadStarted)
                self.merge.threadFinished.connect(self.onThreadFinished)
                self.merge.m_singal.connect(self.Slot)
                self.merge.start()
        elif data[0] == 'parse':
            self.parsers.pop(data[1])
        elif data[0] == 'download':
            self.loads.pop(data[1])
        elif data[0] == 'merge':
            try:
                burl = self.burl.text()
                start_T = str(self.startDate.date().toPyDate())
                end_T = str(self.endDate.date().toPyDate())
                now = str(datetime.datetime.now())
                hash_val = hash(burl + start_T + end_T + now)
                rowitems = [QStandardItem(now), QStandardItem(str(data[1])), QStandardItem(self.bvtitle),
                            QStandardItem(str(self.bvlength)), QStandardItem(start_T), QStandardItem(end_T),
                            QStandardItem(self.bvpubtime),
                            QStandardItem(burl)]
                self.history_datamodel.appendRow(rowitems)
                self.cursor.execute(
                    '''insert into history(id, timestamp, title, bvurl, bvlength, startTime, endTime, pubdate, sum) values('%s','%s', '%s', '%s', '%s',%s, '%s', '%s', '%d')''' %
                    (hash_val, now, self.bvtitle, burl, str(self.bvlength), start_T, end_T, self.bvpubtime,
                     data[1]))
                self.conn.commit()
                self.burl.setReadOnly(False)
                self.startDate.setReadOnly(False)
                self.endDate.setReadOnly(False)
                self.startbtn.clicked.connect(self.start_spider)
                self.reset_time.clicked.connect(self.time_reset)
            except Exception as e:
                print(e)
        self.thread_count -= 1
        print(f"子线程结束，当前线程数量：{self.thread_count}")


class DManalyUi(QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, file, timelength):
        super(DManalyUi, self).__init__()
        self.file = file
        self.timelength = timelength
        self.DM_times = None
        self.interval_size = 20
        self.words_interval = 5
        self.setObjectName("Analy")
        self.setWindowTitle("Analy")
        self.resize(1080, 900)

    def setupUi(self):
        CurrentConfig.ONLINE_HOST = "./pyecharts-assets/"
        self.webview = QWebEngineView()
        self.data = pd.read_csv(self.file, sep=',', encoding='utf-8', escapechar='\\')
        self.genLine()
        self.genWordCloud()
        self.genPie()
        # 生成HTML文件
        html = "chart.html"
        page = Page()
        page.add(self.line)
        page.add(self.wordcloud)
        page.add(self.pie)
        page.render(html)
        self.webview.load(
            QtCore.QUrl.fromLocalFile(os.path.abspath(html)))
        self.setCentralWidget(self.webview)

    def genLine(self):
        Time = []
        for row in self.data['Time']:
            timelist = [int(i) for i in row.split(':')]
            if timelist[0] > 0:
                times = timelist[0] * 60 + timelist[1]
            else:
                times = timelist[1]
            Time.append(times)
        if not self.timelength:
            self.timelength = max(Time)
        if self.timelength >= 3600:
            self.timelength = round(self.timelength / 60)
            self.textunit = '分钟'
        else:
            self.timelength = round(self.timelength)
            self.textunit = '秒'
        self.line = Line()
        DMtime = {}
        mulnum = int(str(self.timelength)[0]) * 10 ** (len(str(self.timelength)) - 1)
        if self.timelength == mulnum:
            interval_all = mulnum
        elif self.timelength - mulnum < 10 ** (len(str(self.timelength)) - 1) / 2:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1) / 2
        else:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1)
        for times in Time:
            for n in range(self.interval_size):
                interval = n * interval_all / self.interval_size
                if interval <= times < interval + interval_all / self.interval_size:
                    if interval not in DMtime:
                        DMtime[interval] = 1
                    else:
                        DMtime[interval] += 1
                    break
        self.DM_times = pd.Series(DMtime)
        self.DM_times.sort_index(axis=0, inplace=True)
        x_data = [str(i) for i in list(self.DM_times.index)]
        self.line.add_xaxis(xaxis_data=x_data)
        y_data = [int(j) for j in self.DM_times.values]
        self.line.add_yaxis(series_name='折线图', y_axis=y_data)
        # 设置标题和坐标轴标签
        self.line.set_global_opts(
            title_opts=opts.TitleOpts(title="弹幕发送量分析"),
            xaxis_opts=opts.AxisOpts(name=f'视频时间/{self.textunit}'),
            yaxis_opts=opts.AxisOpts(name='数值')
        )

    def genWordCloud(self):
        text = ' '.join(self.data['Comment'])
        # 创建一个WordCloud对象
        self.wordcloud = WordCloud()
        # 生成词频
        word_freq = WC().process_text(text)
        # 将词频转为（词，频率）的二元组列表
        word_freq_list = [(k, v) for k, v in word_freq.items()]
        # 通过add方法添加数据并进行设置相关参数
        self.wordcloud.add("", word_freq_list, word_size_range=[20, 50], shape=SymbolType.DIAMOND)
        # 设置全局配置项
        self.wordcloud.set_global_opts(title_opts=opts.TitleOpts(title='弹幕词云图'))

    def genPie(self):
        Unhash = self.data['Uhash']
        dic = {}
        for i in Unhash:
            if i in dic.keys():
                dic[i] += 1
            else:
                dic[i] = 1
        dmNUM_dic = {'1条弹幕': 0, '2条到5条': 0, '6条到10条': 0, '10条以上': 0}
        for x in dic.values():
            if x == 1:
                dmNUM_dic['1条弹幕'] += 1
            elif 1 < x <= 5:
                dmNUM_dic['2条到5条'] += 1
            elif 5 < x <= 10:
                dmNUM_dic['6条到10条'] += 1
            elif 10 < x:
                dmNUM_dic['10条以上'] += 1
        self.pie = Pie()
        self.pie.add('用户弹幕发送量', list(dmNUM_dic.items()))
        self.pie.set_global_opts(title_opts=opts.TitleOpts(title='发送量', pos_left='center'),
                                 legend_opts=opts.LegendOpts(orient='vertical', pos_top='middle', pos_left='0%'))
        self.pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    def File_not_fund(self, err):
        msg = QMessageBox()
        msg.setWindowTitle("error")
        msg.setText(err)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


if __name__ == '__main__':
    Cookies = {
        "buvid3": "64E974A8-04F8-3F70-39B4-7DEF8D91E92B94390infoc",
        "b_nut": "1705633594",
        "i-wanna-go-back": "-1",
        "b_ut": "7",
        "_uuid": "75D1083E10-41037-6985-6222-B1B5BC417AB595426infoc",
        "enable_web_push": "DISABLE",
        "buvid4": "7DB2CE23-75B0-3B7F-F903-BD24F02A260E15099-023121502-",
        "rpdid": "^|(J^|Y^|umll^|Y0J'u~^|lYJJYY^|",
        "header_theme_version": "CLOSE",
        "hit-dyn-v2": "1",
        "is-2022-channel": "1",
        "CURRENT_BLACKGAP": "0",
        "CURRENT_FNVAL": "4048",
        "fingerprint": "959c9334ab17c56899570db552be874a",
        "buvid_fp_plain": "undefined",
        "buvid_fp": "959c9334ab17c56899570db552be874a",
        "bp_video_offset_638341836": "892769120709247088",
        "CURRENT_QUALITY": "64",
        "LIVE_BUVID": "AUTO3017067826754478",
        "home_feed_column": "5",
        "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDczOTUyNTcsImlhdCI6MTcwNzEzNTk5NywicGx0IjotMX0.PV8ic3rSAcXUu-uzjWRdj2CmjnzY44DCX2PvY5ybZ44",
        "bili_ticket_expires": "1707395197",
        "browser_resolution": "1594-836",
        "PVID": "2",
        "b_lsid": "ED256186_18D7D22080A",
        "DedeUserID": "638341836",
        "DedeUserID__ckMd5": "847c2fa3b1f3ca2b",
        "SESSDATA": "a3936181%2C1722755670%2C8f1dc%2A21CjBhF1xNMU3BOr_uFgg48rGeB8zFXsQ8m6fxYV3NfFNQADEwtTadNSIZy2LMDDw3mgYSVnM1ZlJ3UHNNN2pOZXg3X05KbE1Nb1pkWGxRUlpnWUNfdXZIOXBjbVZTSUw5bkFwY1lLZkRUWlJOV3haX1R6MVJ5NzFxWjRPc3kyZS1ENk5kYnF2UDJRIIEC",
        "bili_jct": "06422a76d6a344d5588988062208ebc0",
        "sid": "ouv5oq4t"
    }
    Headers = {
        'Origin': 'https://www.bilibili.com',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
