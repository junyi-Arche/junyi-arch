import csv
import re
import datetime
import threading

import execjs
import matplotlib
import numpy as np
import pandas as pd
from queue import Queue
from time import sleep

from PIL import Image, ImageDraw
from bs4 import BeautifulSoup
from wordcloud import WordCloud

import dm_pb2
import os
import requests
from matplotlib import pyplot as plt


class Dmdategetter(threading.Thread):

    def __init__(self):
        super(Dmdategetter, self).__init__()

        self.dmdategeturl = 'https://api.bilibili.com/x/v2/dm/history/index?month={}&type=1&oid={}'
        self.date_enable_list = date_ableq
        self.date_list = []
        self.pubtime = ''

    def time_set(self):
        global begindateStamp, lastdateStamp
        if not os.path.exists('./弹幕数据'):
            os.mkdir('弹幕数据')
        if not os.path.exists('./so文件'):
            os.mkdir('so文件')
        begindate = None
        lastdate = None
        begindateStamp = None
        while True:
            if not begindateStamp:
                begindate = input('输入开始日期 YEAR/MONTH/DAY(1表示所有时间):')
                if begindate != '1':
                    try:
                        begindateStamp = datetime.datetime.strptime(begindate, '%Y/%m/%d').timestamp()
                        if begindateStamp <= 946656000:
                            raise ValueError
                    except:
                        print('输入错误,请重新输入')
                        continue
                else:
                    begindateStamp = 1
            elif begindateStamp != 1:
                lastdate = input('输入结束日期 YEAR/MONTH/DAY:')
                try:
                    lastdateStamp = datetime.datetime.strptime(lastdate, '%Y/%m/%d').timestamp()
                    if lastdateStamp < begindateStamp:
                        print('输入错误,请重新输入')
                        continue
                    else:
                        break
                except:
                    print('输入错误,请重新输入')
                    continue
            else:
                break
        if begindateStamp != 1:
            y, m, d = [int(i) for i in begindate.split('/')]
            y1, m1, d1 = [int(i) for i in lastdate.split('/')]
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

    def getBvid(self):
        global timelength
        main_html = requests.get(mvurl)
        response = main_html.text
        regx = r'.*<script>window.__INITIAL_STATE__=(.*?)</script>.*'
        regx2 = r'.*"cids":\{"1":(.*?)}.*'
        regx3 = r'.*<script>window.__playinfo__=(.*?)</script>.*'
        regx4 = r'.*"timelength":(.*?),.*'
        playinfo = re.findall(regx, response)[0]
        cid = re.findall(regx2, playinfo)[0]
        playinfo2 = re.findall(regx3, response)[0]
        timelength = int(re.findall(regx4, playinfo2)[0]) / 1000
        beautifulsoup = BeautifulSoup(response, 'lxml')
        self.pubtime = beautifulsoup.find('span', {'class': 'pubdate-text'}).get_text().strip()
        bvtitle = beautifulsoup.find('h1', {'class': 'video-title'}).get_text().strip()
        print('视频长度：{}, 视频名称：{}'.format(timelength, bvtitle))
        return cid

    def run(self):
        global bvid, begindateStamp, lastdateStamp, mvurl
        while True:
            try:
                mvurl = input('输入b站视频url: ')
                if 'bilibili' not in mvurl:
                    continue
                if bvid is None:
                    bvid = self.getBvid()
                    break
            except:
                print('无效的b站视频url')
        self.time_set()
        if len(self.date_list) == 0:
            y, m, d = [int(ti) for ti in self.pubtime.split(' ')[0].split('-')]
            begindateStamp = datetime.datetime.strptime(self.pubtime, '%Y-%m-%d %H:%M:%S').timestamp()
            lastdateStamp = datetime.datetime.now().timestamp()
            while True:
                self.date_list.append('{}-{:02d}'.format(y, m))
                if m < 12:
                    m += 1
                else:
                    y += 1
                    m = 1
                dStamp = datetime.datetime(y, m, 1).timestamp()
                if dStamp > lastdateStamp:
                    break

        for t in self.date_list:
            sleep(1)
            dateres = requests.get(self.dmdategeturl.format(t, bvid), headers=Headers)
            if dateres.status_code == 200:
                dateres = dateres.json().get('data')
                if dateres:
                    for d in dateres:
                        if begindateStamp <= datetime.datetime.strptime(d, '%Y-%m-%d').timestamp() <= lastdateStamp:
                            self.date_enable_list.put(d)


class Dmdatasogetter(threading.Thread):
    def __init__(self, headers):
        super().__init__()
        self.dmdataurl = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={}&date='
        self.date_url = Queue(500)
        self.sofilename = sofileq
        self.date_enable_list = date_ableq
        self.headers = headers
        self.proxy_input = threading.Event()
        self.proxy = None
        self.stop_parseSO = threadEvent

    def run(self):
        # today_stamp = int(time.mktime(datetime.date.today().timetuple()))
        while True:
            if self.date_enable_list.empty():
                break
            date = self.date_enable_list.get()
            # if time_stamp == today_stamp:
            #     self.date_url.put(
            #         'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=410995386&pid=763056111&segment_index=1&pull_mode=1&ps=0&pe=120000')
            #     self.date_url.put(
            #         'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=410995386&pid=763056111&segment_index=1&pull_mode=1&ps=120000&pe=360000')
            # else:
            self.date_url.put(self.dmdataurl.format(bvid) + date)
        self.sendrequest()

    def sendrequest(self):
        global file_name
        while True:
            if self.date_url.empty():
                self.stop_parseSO.set()
                break
            else:
                content_url = self.date_url.get()
                for i in range(4):
                    try:
                        sleep(1)
                        if self.proxy is not None:
                            res_bytes = requests.get(url=content_url, headers=self.headers, timeout=10,
                                                     proxies={'http': self.proxy, 'hppts': self.proxy}).content
                        else:
                            res_bytes = requests.get(url=content_url, headers=self.headers, timeout=10).content
                        file_name = content_url[-10:] + '.so'
                        with open('./so文件/' + file_name, 'wb') as f:
                            f.write(res_bytes)
                        self.sofilename.put(file_name)
                        print(f'**************{file_name}文件保存成功！！！！！')
                        break
                    except requests.exceptions.Timeout:
                        # 超时错误
                        print(f'{file_name}请求超时！！！')
                        continue
                    except Exception as e:
                        print(f'{file_name}请求失败！！！')
                        self.proxy_input.set()
                        self.proxy_input.wait()
                        myinput = input('是否输入代理：1/0')
                        if myinput == '1':
                            newhost = input('输入新代理host：')
                            newport = input('输入新代理port：')
                            self.proxy = f'http://{newhost}:{newport}'
                            if self.proxy is not None:
                                self.proxy_input.clear()
                        else:
                            self.proxy_input.clear()
                        print(f'{file_name}refetch')
                        with open('.error.txt', 'a+', encoding='utf-8') as f:
                            f.write(str(file_name) + f' 抓取失败 {e}\n')
                        continue


class ParseSo(threading.Thread):
    def __init__(self):
        super().__init__()
        self.data = dataq
        self.sofile = sofileq
        self.stop_e = threadEvent
        self.stop_download = threadEvent2

    def run(self):
        while True:
            if self.stop_e.isSet() and self.sofile.empty():
                self.stop_download.set()
                break
            file_name = self.sofile.get()
            with open('./so文件/' + file_name, 'rb') as f:
                data = f.read()
            anadm = dm_pb2.DmSegMobileReply()
            anadm.ParseFromString(data)
            for dm_msg in anadm.elems:
                stime, date = self.handleTime(dm_msg.stime, dm_msg.date)
                data = [stime, date, dm_msg.text, dm_msg.mode, dm_msg.weight, dm_msg.color, dm_msg.size, dm_msg.uhash, dm_msg.dmid]
                self.data.put(data)
            os.remove('./so文件/' + file_name)

    def handleTime(self, ms, timestamp):
        seconds = ms / 1000
        m, s = divmod(seconds, 60)
        stime = '{:02d}:{:02d}'.format(int(m), int(s))
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M')
        return stime, date


class Download(threading.Thread):
    def __init__(self, i):
        super().__init__()
        self.data = dataq
        self.sofile = sofileq
        self.index = i
        self.event = threadEvent
        self.stop_e = threadEvent2
        self.merge_e = mergeevent

    def run(self):
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
                print('dm{}.csv'.format(self.index), '已保存100条数据')


class Merge(threading.Thread):
    def __init__(self):
        super().__init__()
        self.merge_e = mergeevent
        self.event2 = threadEvent2

    def remove_duplicates(self):
        lines_seen = set()  # 用于记录出现过的行
        with open('combined_file.csv', 'r', newline='', encoding='utf-8') as file_in, open(save_file_path, 'w',
                                                                                           newline='',
                                                                                           encoding='utf-8') as file_out:
            reader = csv.reader(file_in)
            writer = csv.writer(file_out)
            for row in reader:
                row_str = ','.join(row)  # 将行内容转换成字符串，以逗号分隔（可根据实际情况修改分隔符）
                if row_str not in lines_seen:
                    writer.writerow(row)
                    lines_seen.add(row_str)
        print('合并完成')

    def run(self):
        self.merge_e.wait()
        print('开始合并文件')
        combined_csv = pd.DataFrame()
        column_names = ['Time', 'Date', 'Comment', 'Mode', 'Weight', 'Color', 'Size', 'Uhash', 'Dmid']
        filelist = os.listdir('./弹幕数据')
        for file in filelist:
            df = pd.read_csv('./弹幕数据/' + file, skip_blank_lines=True, names=column_names)
            combined_csv = pd.concat([combined_csv, df])
            os.remove('./弹幕数据/' + file)
        combined_csv.to_csv('combined_file.csv', index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
        self.remove_duplicates()
        self.merge_e.clear()
        self.event2.clear()
        os.rmdir('弹幕数据')
        os.rmdir('so文件')


class DManaly(threading.Thread):
    def __init__(self):
        super(DManaly, self).__init__()
        self.data = pd.read_csv(save_file_path, sep=',', encoding='utf-8', escapechar='\\')
        if timelength >= 3600:
            self.timelength = round(timelength / 60)
            self.textunit = '分钟'
        else:
            self.timelength = round(timelength)
            self.textunit = '秒'
        self.interval_size = 20
        self.words_interval = 5
        self.DM_times = None

    def DMsendNums(self):
        DMtime = {}
        mulnum = int(str(self.timelength)[0]) * 10 ** (len(str(self.timelength)) - 1)
        if self.timelength == mulnum:
            interval_all = mulnum
        elif self.timelength - mulnum < 10 ** (len(str(self.timelength)) - 1) / 2:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1) / 2
        else:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1)
        for row in self.data['Time']:
            timelist = [int(i) for i in row.split(':')]
            if timelist[0] > 0:
                times = timelist[0] * 60 + timelist[1]
            else:
                times = timelist[1]
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
        matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        matplotlib.rcParams['font.size'] = 16
        plt.figure(figsize=(16, 8), dpi=80)
        plt.plot(self.DM_times.index, self.DM_times.values)
        plt.xlabel('视频时间/{}'.format(self.textunit), fontsize=15, color='blue')
        plt.ylabel('弹幕数量', fontsize=15, color='green')
        plt.show()

    def DMwords(self):
        comment_items = self.data.itertuples(index=False)
        wordsDict = {}
        for row in comment_items:
            timelist = [int(i) for i in row[0].split(':')]
            if timelist[0] > 0:
                times = timelist[0] * 60 + timelist[1]
            else:
                times = timelist[1]
            for n in range(self.words_interval):
                interval = n * self.timelength / self.words_interval
                if interval <= times < interval + self.timelength / self.words_interval:
                    if interval not in wordsDict:
                        wordsDict[interval] = []
                        wordsDict[interval].append(row[2])
                    else:
                        wordsDict[interval].append(row[2])
                    break
        sorted_items = sorted(wordsDict.items(), key=lambda x: x[0])
        wordsDict.clear()
        wordsDict.update(sorted_items)
        # 创建一个白色背景的图片
        width, height = 1600, 1600
        image = Image.new("RGB", (width, height), (255, 255, 255))

        # 创建画笔对象
        draw = ImageDraw.Draw(image)

        center_x = width // 2
        triangle_vertices = np.array([
            [center_x, 0],  # 顶点
            [0, height],  # 左下角
            [width, height],  # 右下角
        ])
        draw.polygon([tuple(v) for v in triangle_vertices], fill=(0, 0, 0))

        # 创建遮罩对象
        mask = np.array(image)
        for item in wordsDict:
            comments = wordsDict[item]
            text = ' '.join(comments)
            wc = WordCloud(mask=mask, font_path='C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc', width=1600, height=900, mode="RGBA",
                           background_color='white').generate(text)
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()

    def run(self):
        self.DMsendNums()
        self.DMwords()


if __name__ == '__main__':
    save_file_path = 'finally_file.csv'
    mvurl = ''
    Headers = {
        'Cookie': "buvid3=686669AB-27FC-F858-ED22-9F72C508B15D59660infoc; b_nut=1693215659; CURRENT_FNVAL=4048; b_lsid=451BE10E9_18A3B84A15E; _uuid=645C7981-D3C4-E814-A9107-8AE3458AD103162439infoc; buvid_fp=2f6a01b058e9dde9f110fab181763e80; buvid4=044AC8A4-B5A5-CF5F-7C13-825CE4AB34EA61110-023082817-%2BQGnwQAgbpqp%2BFtpVUl84Q%3D%3D; rpdid=|(JRuY~)lkY|0J'uYmJkulYYk; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTM0NzQ4NjMsImlhdCI6MTY5MzIxNTY2MywicGx0IjotMX0.RuJqNCIOh9yAH92rvfLOrdrAu6xLNLay8aUXiUA1Qys; bili_ticket_expires=1693474863; header_theme_version=CLOSE; SESSDATA=e3b27870%2C1708767793%2C09da9%2A823eY0trnVQPAD2M3HHd9hXq1VkwxpjUVoGv-qa5luakJ_InzBTU7rU0ffrxQVHZzP75W5AAAAJAA; bili_jct=888153049e6b9f4b009e4ad9a6697481; DedeUserID=638341836; DedeUserID__ckMd5=847c2fa3b1f3ca2b; home_feed_column=5; browser_resolution=1920-420; sid=7amk60rr",
        'Origin': 'https://www.bilibili.com',
        'Referer': mvurl,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    bvid = None
    date_ableq = Queue(500)
    dmdate = Dmdategetter()
    dmdate.start()
    dmdate.join()

    threadEvent = threading.Event()
    threadEvent2 = threading.Event()
    mergeevent = threading.Event()
    dataq = Queue(8000)
    sofileq = Queue(500)

    # for i in range():
    spider = Dmdatasogetter(Headers)
    spider.start()

    for i in range(2):
        paser = ParseSo()
        paser.start()
    for i in range(3):
        load = Download(i)
        load.start()
    merge = Merge()
    merge.start()
    merge.join()
    DMana = DManaly()
    DMana.start()
