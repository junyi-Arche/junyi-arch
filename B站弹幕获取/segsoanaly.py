import csv
import datetime

import B站弹幕获取.dm_pb2 as dm_pb2
with open('dm.so', 'rb') as f:
    data = f.read()

anadm = dm_pb2.DmSegMobileReply()
anadm.ParseFromString(data)
# print(len(anadm.elems))
def handleTime(ms, timestamp):
    seconds = ms / 1000
    m, s = divmod(seconds, 60)
    stime = '{:02d}:{:02d}'.format(int(m), int(s))
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M')
    return stime, date
j = 0
data = []
for dm_msg in anadm.elems:
    stime, date = handleTime(dm_msg.stime, dm_msg.date)
    data.append([stime, date, dm_msg.text, dm_msg.color, dm_msg.dmid, dm_msg.mode, dm_msg.size, dm_msg.uhash, dm_msg.weight])
with open('dm.csv', 'a+', newline='', encoding='utf-8') as g:
    writer = csv.writer(g)
    writer.writerows(data)
    j += 1
    if j % 1000 == 0:
        print('dm.csv', '已保存1000条数据')

