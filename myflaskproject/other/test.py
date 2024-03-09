import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='MySQL',
    db='bookdata',
    charset='utf8'
)
cur = conn.cursor()
sql = """select categories, S_categories from allbooks"""
cur.execute(sql)
catedict = {}
result = cur.fetchall()
for i in result:
    if i[0] in catedict.keys():
        if i[1] not in catedict[i[0]]:
            catedict[i[0]].append(i[1])
    else:
        catedict[i[0]] = [i[1]]
num = 1000
for item in catedict.items():
    sql2= """insert into bookcategories(cateid, categoryname) values('%s', '%s')""" % (num, item[0])
    cur.execute(sql2)
    print(num, item[0])
    sNum = num
    for sCate in item[1]:
        sNum += 1
        print(sNum, sCate)
        sql3 = """insert into bookcategories(cateid, categoryname) values('%s', '%s')""" % (sNum, sCate)
        cur.execute(sql3)
    conn.commit()
    num += 100
print(catedict)