import datetime
import threading

import matplotlib
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from wordcloud import WordCloud


class DManaly(threading.Thread):
    def __init__(self):
        super(DManaly, self).__init__()
        self.data = pd.read_csv('B站弹幕获取/finally_file.csv', sep=',', encoding='utf-8', escapechar='\\')
        # self.timelength = round(int(152043) / 1000)
        if int(152043) / 1000 >= 3600:
            self.timelength = round(int(152043) / 1000 / 60)
        else:
            self.timelength = round(int(152043) / 1000)
        self.interval_size = 20
        self.DM_times = None
        self.words_interval = 5

    def DMsendNums(self):
        DMtime = {}
        mulnum = int(str(self.timelength)[0]) * 10 ** (len(str(self.timelength)) - 1)
        print(mulnum)
        if self.timelength == mulnum:
            interval_all = mulnum
        elif self.timelength - mulnum < 10 ** (len(str(self.timelength)) - 1) / 2:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1) / 2
        else:
            interval_all = mulnum + 10 ** (len(str(self.timelength)) - 1)
        print(interval_all)
        num = 0
        for row in self.data['Time']:
            timelist = [int(i) for i in row.split(':')]
            print(timelist)
            if timelist[0] > 0:
                seconds = timelist[0] * 60 + timelist[1]
            else:
                seconds = timelist[1]

            for n in range(self.interval_size):
                interval = n * interval_all // self.interval_size
                print(interval, seconds)
                if interval <= seconds < interval + interval_all / self.interval_size:
                    num += 1
                    if interval not in DMtime:
                        DMtime[interval] = 1
                    else:
                        DMtime[interval] += 1
                    break
        self.DM_times = pd.Series(DMtime)
        self.DM_times.sort_index(axis=0, inplace=True)
        print(self.DM_times.index, self.DM_times.values)
        print('num', num)
        matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        matplotlib.rcParams['font.size'] = 16
        plt.figure(figsize=(12, 7), dpi=80)
        plt.plot(self.DM_times.index, self.DM_times.values)
        plt.xlabel('视频时间/分钟', fontsize=15, color='blue')
        plt.ylabel('弹幕数量', fontsize=15, color='green')
        plt.show()

    def run(self):
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
        print(wordsDict.keys())
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
            wc = WordCloud(mask=mask, font_path='C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc', width=1600,
                           height=1600, mode="RGBA",
                           background_color='white').generate(text)
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()


if __name__ == '__main__':
    dmanaly = DManaly()
    dmanaly.start()
