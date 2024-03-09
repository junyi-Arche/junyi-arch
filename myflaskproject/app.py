import base64
import gzip
import hashlib
import hmac
import io
import json
import math
import time
import uuid
from functools import wraps
from flask.views import MethodView
from sqlalchemy import func
from form import *
from flask import request, jsonify, make_response, session, render_template_string, render_template
from flask_cors import *
import jwt
from models import *
import bookStack_pb2
from flask_mail import Message

book_fetch = Booksfetch()


def verify_Model(verify_type, verify_mode):
    varify_model = '''
    <head>
        <base target="_blank"/>
        <style type="text/css">
            ::-webkit-scrollbar {
                display: none;
            }
        </style>
        <style id="cloudAttachStyle" type="text/css">
            #divNeteaseBigAttach,
            #divNeteaseBigAttach_bak {
                display: none;
            }
        </style>
        <style id="blockquoteStyle" type="text/css">
            blockquote {
                display: none;
            }
        </style>
        <style type="text/css">
            body {
                font-size: 14px;
                font-family: arial, verdana, sans-serif;
                line-height: 1.666;
                padding: 0;
                margin: 0;
                overflow: auto;
                white-space: normal;
                word-wrap: break-word;
                min-height: 100px
            }

            td,
            input,
            button,
            select,
            body {
                font-family: Helvetica, 'Microsoft Yahei', verdana
            }

            pre {
                white-space: pre-wrap;
                white-space: -moz-pre-wrap;
                white-space: -o-pre-wrap;
                word-wrap: break-word;
                width: 95%
            }

            th,
            td {
                font-family: arial, verdana, sans-serif;
                line-height: 1.666
            }

            img {
                border: 0
            }

            header,
            footer,
            section,
            aside,
            article,
            nav,
            hgroup,
            figure,
            figcaption {
                display: block
            }

            blockquote {
                margin-right: 0px
            }
        </style>
    </head>

    <body tabindex="0" role="listitem">
    <table width="700" border="0" align="center" cellspacing="0" style="width:700px;">
        <tbody>
        <tr>
            <td>
                <div style="width:700px;margin:0 auto;border-bottom:1px solid #ccc;margin-bottom:30px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="700" height="39"
                           style="font:12px Tahoma, Arial, 宋体;">
                        <tbody>
                        <tr>
                            <td width="210"></td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div style="width:680px;padding:0 10px;margin:0 auto;">
                    <div style="line-height:1.5;font-size:14px;margin-bottom:25px;color:#4d4d4d;">
                        <strong style="display:block;margin-bottom:15px;">尊敬的用户：<span
                                style="color:#f60;font-size: 16px;"></span>您好！</strong>
                        <strong style="display:block;margin-bottom:15px;">
                            您正在进行<span style="color: red">''' + verify_type + '''</span>操作，请在验证码输入框中输入：<span
                                style="color:#f60;font-size: 24px">''' + verify_mode + '''</span>，以完成操作。
                        </strong>
                    </div>
                    <div style="margin-bottom:30px;">
                        <small style="display:block;margin-bottom:20px;font-size:12px;">
                            <p style="color:#747474;">
                                注意：此操作可能会修改您的密码、登录邮箱或绑定手机。如非本人操作，请及时登录并修改密码以保证帐户安全
                                <br>(工作人员不会向你索取此验证码，请勿泄漏!)
                            </p>
                        </small>
                    </div>
                </div>
                <div style="width:700px;margin:0 auto;">
                    <div
                            style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                        <p>此为系统邮件，请勿回复<br>
                            请保管好您的邮箱，避免账号被他人盗用
                        </p>
                        <p>网络科技团队</p>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </body>'''
    return varify_model


def login_required(user_key):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get(user_key) is None:
                # 用户未登录，重定向到登录页面
                return jsonify({
                    'status': 403,
                })
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.route('/CaptchaGet', methods=['POST'])
def send_Captcha():
    data = request.form
    user_email = data.get('email')
    ts_tp = data.get('_')
    if user_email and ts_tp:
        if len(ts_tp) == 14:
            ts = ts_tp[:13]
            tp = ts_tp[13]
            if int(time.time()) - int(ts) <= 5:
                if tp == '1':
                    verify_type = '登录验证'
                elif tp == '2':
                    verify_type = '注册验证'
                else:
                    return jsonify({
                        'status': 403,
                        'msg': '出错了！'
                    })
                verify_mode = str(random.randint(0, 999999)).zfill(6)
                model = verify_Model(verify_type, verify_mode)
                msg = Message(subject='消息验证', recipients=[user_email], html=model)
                mail.send(msg)
                session[user_email.split('.')[0]] = [verify_mode, int(time.time())]
                print(session.items())
                return jsonify({
                    'status': 200,
                    'msg': '发送成功'
                })
            else:
                return jsonify({
                    'status': 403,
                    'msg': '发送失败'
                })
        else:
            return jsonify({
                'status': 403,
                'msg': '发送失败'
            })
    else:
        return jsonify({
            'status': 403,
            'msg': '出错了！！'
        })


def returnAndclear(email, msg):
    session.pop(email)
    return msg


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    mode = data.get('mode')
    userNum = data.get('usernum')
    userPwd = data.get('userpwd')
    Email = data.get('email')
    if mode and userPwd and userNum and Email:
        if mode == session.get(Email)[0]:
            if int(time.time()) - session.get(Email)[1] > 360:
                return returnAndclear(Email, jsonify({
                    'status': 403,
                    'msg': '验证码过期！'
                }))
            if RegisterForm(data):
                user = Userinfo(usernum=userNum, userpwd=userPwd)
                res = user.add()
                if res:
                    return jsonify({
                        'username': res,
                        'msg': '注册成功',
                        'register': True
                    })
                else:
                    return returnAndclear(Email, jsonify({
                        'status': 403,
                        'msg': '用户名存在不可用',
                        'register': False
                    }))
            else:
                print('验证失败')
                return returnAndclear(Email, jsonify({
                    'status': 403,
                    'msg': '注册失败',
                    'register': False
                }))
        else:
            return returnAndclear(Email, jsonify({
                'status': 403,
                'msg': '验证失败！'
            }))
    else:
        return returnAndclear(Email, jsonify({
            'status': 403,
            'msg': '出错了！'
        }))


class Login(MethodView):
    def __init__(self):
        self.SECRET_KEY = '010999'

    def post(self):
        data = request.form
        usernum = data.get('usernum')
        pwd = data.get('pwd')
        mode = data.get('mode')
        Email = data.get('email')
        if usernum and pwd and mode and Email:
            user = db.session.query(Userinfo).filter(Userinfo.usernum == usernum).first()
            if user is not None:
                if mode == session.get(Email)[0]:
                    if int(time.time()) - session.get(Email)[1] > 360:
                        return returnAndclear(Email, jsonify({
                            'status': 403,
                            'msg': '验证码过期！'
                        }))
                    if self.verify_pwd(user.userpwd, pwd):
                        session[usernum] = user.username
                        token = self.create_token(usernum)
                        return jsonify(
                            {'status': 200, 'login': True, 'uname': user.username, 'ulog': token})
                    else:
                        return returnAndclear(Email, jsonify({'status': 200, 'login': False}))
                else:
                    return returnAndclear(Email, jsonify({
                        'status': 403,
                        'msg': '验证码错误'
                    }))
            else:
                return returnAndclear(Email, jsonify({'status': 200, 'login': False, 'msg': '用户名不存在！！'}))

    def get(self):
        # 使用token自动登录
        data = request.values
        token = data.get('token')
        if token:
            account = self.verify_token(token)
            if account:
                session[account.usernum] = account.username
                return jsonify({'status': True, 'username': account.username, 'userid': account.usernum})
            else:
                return jsonify({'status': False})

    def time_str_int(self, date_str):
        """将时间字符串转换为时间数组"""
        timeArray = time.strptime(date_str, '%Y-%m-%d-%H-%M-%S')
        """将时间转换为时间戳"""
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def create_token(self, account):
        """生成token"""
        overdue_time = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d-%H-%M-%S')
        overdue_timeStamp = self.time_str_int(overdue_time)
        own_token = jwt.encode({'account': account, 'overdue_time': overdue_timeStamp}, self.SECRET_KEY,
                               algorithm='HS256')
        return own_token

    def verify_token(self, own_token):
        try:
            decode_token = jwt.decode(own_token, self.SECRET_KEY, algorithms=['HS256'])
            token_account = decode_token['account']
            _account = Userinfo.query.filter_by(usernum=token_account).first()
            if _account is not None:
                token_overdue_time = decode_token['overdue_time']
                now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                now_timeStamp = self.time_str_int(now_time)
                if now_timeStamp < token_overdue_time:
                    return _account
                else:
                    return None
            else:
                return None
        except:
            return None

    def verify_pwd(self, relpwd, pwd):
        now = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')
        stamp = datetime.datetime.strptime(now, '%m/%d/%Y, %H:%M').timestamp()
        text = ''.join([relpwd, str(int(stamp))])
        hash_object = hashlib.md5(text.encode('utf-8'))
        hashed_text = base64.b64encode(hash_object.digest())
        hmac_object = hmac.new(self.SECRET_KEY.encode(), hashed_text, hashlib.sha1)
        encrypted_text = hmac_object.hexdigest()
        if encrypted_text == pwd:
            return True
        else:
            return False


app.add_url_rule('/login', view_func=Login.as_view('login_view'), methods=['POST', 'GET'])


@app.route('/logout', methods=['POST'])
def logout():
    data = request.form
    session.pop(data['usernum'], None)
    session.modified = True
    return jsonify({'status': 200})


@app.route('/forgetpwd', methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        data = request.values
        userNum = data.get('usernum')
        if userNum:
            user = Userinfo.query.filter_by(usernum=userNum).first()
            if user is None:
                return {'status': 404}
            else:
                return {'status': 200, 'id': user.id}
        raise Exception()
    else:
        data = request.form
        id = data.get('id')
        userPwd = data.get('userpwd')
        mode = data.get('mode')
        Email = data.get('email')
        if id and userPwd and mode and Email:
            if mode == session.get(Email)[0]:
                session.pop(Email)
                if int(time.time()) - session.get(Email)[1] > 360:
                    return jsonify({
                        'status': 403,
                        'msg': '验证码过期！'
                    })
                Userinfo.query.filter_by(id=id).update({Userinfo.userpwd: userPwd})
                db.session.commit()
                print(db.session.query(Userinfo.userpwd).all())
                return {'status': 200}


class BookStacks(MethodView):
    def __init__(self):
        self.message = bookStack_pb2.MyData()

    def get(self):
        data = request.args
        if '_page' not in data.keys():
            return {'status': 404}
        if 'category' in data.keys():
            allbooks = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname, Allbooks.descipe,
                                                    Allbooks.imgurl).filter_by(categories=data['category']).limit(
                30).offset((int(data['_page']) - 1) * 30).all()
            if 'f' in data.keys():
                pages = math.ceil(
                    db.session.query(Allbooks).filter(Allbooks.categories == data['category']).count() / 30)
                return self.gMessage(allbooks=allbooks, pages=pages)
            return self.gMessage(allbooks)
        elif 'scategory' in data.keys():
            allbooks = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname, Allbooks.descipe,
                                                    Allbooks.imgurl).filter_by(S_categories=data['scategory']).limit(
                30).offset((int(data['_page']) - 1) * 30).all()
            if 'f' in data.keys():
                pages = math.ceil(
                    db.session.query(Allbooks).filter(Allbooks.S_categories == data['scategory']).count() / 30)
                return self.gMessage(allbooks=allbooks, pages=pages)
            return self.gMessage(allbooks)
        else:
            allbooks = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname, Allbooks.descipe,
                                                    Allbooks.imgurl).limit(30).offset(
                (int(data['_page']) - 1) * 30).all()
            pages = math.ceil(db.session.query(Allbooks).count() / 30)
        # random.shuffle(allbook)
        if 'f' in data:
            Allcategorydict = {}
            # 获取数据库的所有书籍类型
            categories = Bookcategories.query.with_entities(Bookcategories.cateid,
                                                            Bookcategories.categoryname).order_by(
                Bookcategories.cateid).all()
            num = 0
            for i in range(len(categories)):
                if categories[i][0] % 100 == 0:
                    categorylist = []
                    categorydict = {}
                    for j in range(i + 1, len(categories)):
                        if categories[j][0] % 10 == 0:
                            categorydict[categories[i][1]] = categorylist
                            Allcategorydict[num] = categorydict
                            num += 1
                            break
                        elif j == len(categories) - 1:
                            categorylist.append(categories[j][1])
                            categorydict[categories[i][1]] = categorylist
                            Allcategorydict[num] = categorydict
                            break
                        else:
                            categorylist.append(categories[j][1])
            return self.gMessage(allbooks, Allcategorydict, pages)
        return self.gMessage(allbooks)

    def gMessage(self, allbooks, Allcategorydict=None, pages=None):
        bookdata = []
        for item in allbooks:
            bookdata.append({
                'id': item[0],
                'author': item[1],
                'bookname': item[2],
                'bookdescri': item[3],
                'bookimgurl': '/api/getbookimg/2023/' + item[4].split('/')[-1] if item[4] else None
            })
        for item in bookdata:
            new_book = self.message.bookdata.add()
            new_book.id = item['id']
            new_book.author = item['author']
            new_book.bookname = item['bookname']
            new_book.bookdescri = item['bookdescri']
            if item['bookimgurl'] is not None:
                new_book.bookimgurl = item['bookimgurl']
            else:
                new_book.bookimgurl = ''
        if Allcategorydict:
            for category_key, category_value in Allcategorydict.items():
                new_category = self.message.category.category_map.add()
                new_category.key = category_key
                for catename, catelist in category_value.items():
                    new_categoryList = new_category.category_items.category_list.add()
                    new_categoryList.catekey = catename
                    new_categoryList.values.extend(catelist)
        if pages:
            self.message.mpage = pages
        serialized_data = self.message.SerializeToString()
        compressed_data = gzip.compress(serialized_data)
        base64_data = base64.b64encode(compressed_data).decode('utf-8')
        return jsonify(base64_data)


app.add_url_rule('/bookdata', view_func=BookStacks.as_view('bookstacks_view'), methods=['GET'])


@app.route('/books', methods=['GET'])
def book():
    if request.method == 'GET':
        # print('user', session['username'])
        lunboData = []
        successBData = []
        hotsuccessData = []
        netvolData = []
        hotnetvoldata = []
        success_n = random.randint(0, 40)
        success_bookd = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname, Allbooks.descipe,
                                                     Allbooks.imgurl).filter_by(categories='成功励志').limit(15).offset(
            success_n).all()
        netvol_n = random.randint(0, 113)
        netvol_bookd = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname, Allbooks.descipe,
                                                    Allbooks.imgurl).filter_by(categories='小说作品').limit(17).offset(
            netvol_n).all()
        for i in range(10):
            lunbo_n = random.randint(0, 571)
            lunbo_bookd = Allbooks.query.offset(lunbo_n).limit(1).first()
            lunboData.append({
                'id': lunbo_bookd.bid,
                'bookname': lunbo_bookd.bookname,
                'bookimgurl': '/api/getbookimg/2023/' + lunbo_bookd.imgurl.split('/')[-1] if lunbo_bookd.imgurl else '',
                'bookdescri': lunbo_bookd.descipe
            })
        for i in range(len(success_bookd)):
            data = {
                'id': success_bookd[i][0],
                'bookauthor': success_bookd[i][1],
                'bookname': success_bookd[i][2],
                'bookdescri': success_bookd[i][3],
                'bookimgurl': '/api/getbookimg/2023/' + success_bookd[i][4].split('/')[-1] if success_bookd[i][
                    4] else ''
            }
            if i < 5:
                successBData.append(data)
            else:
                hotsuccessData.append(data)
        for i in range(len(netvol_bookd)):
            data = {
                'id': netvol_bookd[i][0],
                'bookauthor': netvol_bookd[i][1],
                'bookname': netvol_bookd[i][2],
                'bookdescri': netvol_bookd[i][3],
                'bookimgurl': '/api/getbookimg/2023/' + netvol_bookd[i][4].split('/')[-1] if netvol_bookd[i][4] else ''
            }
            if i < 7:
                netvolData.append(data)
            else:
                hotnetvoldata.append(data)
        binery_data = json.dumps({
            'bookdata': {'lunboData': lunboData, 'storyData': {'stories': successBData, 'hotbookData': hotsuccessData},
                         'netvols': {'novels': netvolData, 'hotnovels': hotnetvoldata}
                         },
            'status': 200}).encode('utf-8')

        gzip_data = gzip.compress(binery_data)
        data = io.BytesIO(gzip_data)
        # 创建响应对象
        res = make_response(data)
        # 设置响应头
        res.headers['Content-Encoding'] = 'gzip'
        res.headers['Content-Type'] = 'application/octet-stream'
        return res


@app.route('/bookrank', methods=['GET'])
def bookranks():
    novels = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname,
                                          Allbooks.imgurl).filter_by(categories='小说作品').limit(15).all()
    histories = Allbooks.query.with_entities(Allbooks.bid, Allbooks.author, Allbooks.bookname,
                                             Allbooks.imgurl).filter_by(categories='历史传记').limit(15).all()
    rankbooks = {'novels': [], 'histories': []}
    for i in novels:
        rankbooks['novels'].append({
            'id': i[0],
            'bookname': i[2],
            'bookauthor': i[1],
            'bookimgurl': '/api/getbookimg/2023/' + i[3].split('/')[-1] if i[3] else ''
        })
    for j in histories:
        rankbooks['histories'].append({
            'id': j[0],
            'bookname': j[2],
            'bookauthor': j[1],
            'bookimgurl': '/api/getbookimg/2023/' + j[3].split('/')[-1] if j[3] else ''
        })
    return jsonify(rankbooks)


@app.route('/bookdetail', methods=['GET'])
def bookdetail():
    data = request.args
    bookid = data.get('b_id')
    try:
        bookitem = Allbooks.query.filter_by(bid=bookid).first()
    except:
        return {'msg': 'null'}
    if bookitem is None:
        return {'msg': 'null'}
    else:
        bookcate = Allbooks.query.with_entities(Allbooks.categories).filter_by(bid=bookid).first()
        '''设置书籍详情页推荐图书，order_by() 方法用于指定按照哪个字段排序，我们使用 func.random() 函数作为排序条件，它将对结果进行随机排序'''
        recomendbooks = Allbooks.query.with_entities(Allbooks.bid, Allbooks.bookname, Allbooks.author,
                                                     Allbooks.imgurl).filter(Allbooks.categories == bookcate[0],
                                                                             Allbooks.bid != bookid).order_by(
            func.random()).limit(4).all()
        recomendbooklist = []
        for i in recomendbooks:
            recomendbooklist.append({
                'id': i[0],
                'bookname': i[1],
                'author': i[2],
                'bookimgurl': '/api/getbookimg/2023/' + i[3].split('/')[-1] if i[3] else ''
            })
        btable = 'b' + str(bookid)
        bookchaptertitle = book_fetch.getbookchaptertitle(btable)
        bookdatadict = {
            'id': bookitem.bid,
            'author': bookitem.author,
            'bookname': bookitem.bookname,
            'publisher': bookitem.publisher,
            'bookimgurl': '/api/getbookimg/2023/' + bookitem.imgurl.split('/')[-1] if bookitem.imgurl else '',
            'bookdescri': bookitem.descipe,
            'bookchaptertitle': [item[0] for item in bookchaptertitle]
        }
        if 'utoken' in data.keys():
            result = Login().verify_token(data['utoken'])
            uid = result.usernum
            userhavbooks = Usertobooks.query.with_entities(Usertobooks.bookid).filter_by(userid=uid).all()
            for i in userhavbooks:
                if bookid in i:
                    return jsonify(
                        {'bookdata': bookdatadict, 'recomends': recomendbooklist, 'userhaving': 1, 'status': 200})
            return jsonify({'bookdata': bookdatadict, 'recomends': recomendbooklist, 'userhaving': 0, 'status': 200})
        return jsonify({'bookdata': bookdatadict, 'recomends': recomendbooklist, 'status': 200})


@app.route('/searchbook', methods=['GET', 'POST'])
def searchbook():
    if request.method == 'GET':
        data = request.values
        if 'bn' not in data.keys():
            return {'msg': 'null'}
        search = [{'id': i.bid, 'value': i.bookname} for i in
                  Allbooks.query.filter(Allbooks.bookname.like('%' + data['bn'] + '%')).all()]
        random.shuffle(search)
        return jsonify({'searchbooks': search})
    else:
        data = request.form
        search = Allbooks.query.filter(Allbooks.bookname.like('%' + data['bn'] + '%')).all()
        if not search:
            return {'msg': 'null', 'status': 404}
        else:
            searchbooks = []
            for item in search:
                searchbooks.append({
                    'id': item.bid,
                    'bookname': item.bookname,
                    'bookauthor': item.author,
                    'bookimgurl': '/api/getbookimg/2023/' + item.imgurl.split('/')[-1] if item.imgurl else '',
                    'bookdescri': item.descipe
                })
            return jsonify({'searchbooks': searchbooks, 'status': 200})


@app.route('/getuserbook', methods=['GET', 'POST'])
def Getuserbook():
    if request.method == 'POST':
        data = request.form
        result = Login().verify_token(data['user'])
        if result:
            uid = result.usernum

            @login_required(uid)
            def getuserbook():
                userhavbooks = Usertobooks.query.filter_by(userid=uid).all()
                if len(userhavbooks) >= 1:
                    alluserbooks = []
                    for book in userhavbooks:
                        alluserbooks.append({
                            'id': book.booktouser.bid,
                            'bookname': book.booktouser.bookname,
                            'bookimgurl': '/api/getbookimg/2023/' + book.booktouser.imgurl.split('/')[
                                -1] if book.booktouser.imgurl else ''
                        })
                    return jsonify({'userbooks': alluserbooks, 'status': 200})
                else:
                    return jsonify({'msg': 'null', 'status': 404})

            return getuserbook()
        else:
            return jsonify({'msg': 'null', 'status': 404})
    else:
        return {'error': 1000, 'msg': 'null'}


@app.route('/getbookimg/2023/<string:imgname>', methods=['GET'])
def getbookimg(imgname):
    # image_path = 'G:/mysqlimgFile/bookimgs/' + imgname
    try:
        with open("G:/mysqlimgFile/bookimgs/" + imgname, 'rb') as f:
            img = f.read()
    except:
        return {'msg': 'null'}
    compressed_img = gzip.compress(img)
    response = make_response(compressed_img)
    response.headers['Content-Encoding'] = 'gzip'
    # expires = datetime.datetime.now() + datetime.timedelta(hours=1)
    # response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    # return send_file(image_path, mimetype='image/jpeg')
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


@app.route('/BookChapterContent/<string:bid>', methods=['GET'])
def getchaptercontent(bid):
    # global booktable
    data = request.args
    if 'cid' not in data.keys():
        return {'msg': 'null'}
    booktable = 'b' + str(bid)
    try:
        bookchaptercontent = book_fetch.getbookchaptercontent(booktable, int(data['cid']) + 1)
    except:
        return {'msg': 'null', 'status': 404}
    return jsonify({'content': bookchaptercontent[0][0], 'chaptertitle': bookchaptercontent[0][1], 'status': 200})


@app.route('/addtoshelf', methods=['POST'])
def addtoShelf():
    data = request.form
    try:
        result = Login().verify_token(data['utoken'])
        if result:
            # 验证用户是否登录
            @login_required(result.usernum)
            def Add():
                userTObook = Usertobooks(userid=result.usernum, bookid=data['b_id'])
                db.session.add(userTObook)
                db.session.commit()
                return jsonify({'status': 200})

            return Add()
        else:
            return jsonify({'msg': 'null', 'status': 404})
    except:
        return {'msg': 'null', 'error': 1000}


@app.route('/deleteUserbookshelf', methods=['POST'])
def deluserbook():
    data = request.form
    dictkeys = data.keys()
    result = Login().verify_token(data['utoken'])
    if result:
        @login_required(result.usernum)
        def Del():
            for i in dictkeys:
                if i != 'utoken':
                    userTObook = Usertobooks.query.filter_by(userid=result.usernum, bookid=data[i]).first()
                    db.session.delete(userTObook)
                    db.session.commit()
            return jsonify({'status': 200})

        return Del()
    else:
        return jsonify({'msg': 'null', 'status': 404})


@app.route('/addbookcomment', methods=['POST'])
def bookcomment():
    data = request.form
    result = Login().verify_token(data['utoken'])
    if result:

        @login_required(result.usernum)
        def addcomment():
            uid = uuid.uuid3(uuid.NAMESPACE_DNS, result.usernum + data['b_id']).hex
            comment = Bookcomments(uid=uid, userid=result.usernum, bookid=data['b_id'], comment=data['con'])
            res = comment.addcomment()
            if res:
                return jsonify({'status': 200, 'comid': uid})
            else:
                return jsonify({'status': 404, 'error': 1000})

        return addcomment()
    return jsonify({'status': 404, 'error': 1000})


@app.route('/getbookcomment', methods=['GET'])
def getbookcomment():
    data = request.args
    comment = Bookcomments.query.filter_by(bookid=data['b_id']).order_by(Bookcomments.addtimestamp.desc()).all()
    if len(comment) >= 1:
        commentslist = []
        for item in comment:
            commentslist.append({
                'comid': item.uid,
                'comment': item.comment,
                'username': item.usertocom.username,
                'userid': item.userid,
                'addtime': datetime.datetime.fromtimestamp(item.addtimestamp).strftime("%Y-%m-%d %H:%M"),
            })
        return jsonify({'status': 200, 'comments': commentslist})
    else:
        return jsonify({'status': 404, 'error': 1000})


@app.route('/delbookcomment', methods=['POST'])
def delbookcomment():
    data = request.form
    result = Login().verify_token(data['utoken'])
    if result:
        @login_required(result.usernum)
        def delcomment():
            comment = Bookcomments.query.filter_by(uid=data['comid']).first()
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'status': 200})

        return delcomment()
    return jsonify({'status': 404, 'error': 1000})


# 首先定义一个处理页面不存在的错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    # 这里可以根据需要自定义导航到的页面，比如 '404.html'
    return render_template('404.html')


# 使用装饰器来处理异常
@app.errorhandler(Exception)
def handle_exception(error):
    print(error)
    return render_template('error.html')


if __name__ == '__main__':
    CORS(app, resources=r'/*')
    app.run(host='127.0.0.1', port=5000, debug=True)
