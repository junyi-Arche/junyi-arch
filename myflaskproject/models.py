import datetime
import random
import string
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlExtention import DBURI
from flask_migrate import Migrate
from sqlalchemy.sql import text
import mailConfig

app = Flask(__name__)
app.config.from_object(mailConfig)
mail = Mail(app)
app.secret_key = 'agh0h1g1l3k4p19n1g1nf1b'
app.config['SQLALCHEMY_DATABASE_URI'] = DBURI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# 绑定app和数据库，进行数据迁移
migrate = Migrate(app, db)



class Usertobooks(db.Model):
    __tablename__ = 'usersbooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    userid = db.Column(db.String(20), db.ForeignKey('userinfo.usernum'), nullable=False)
    bookid = db.Column(db.String(60), db.ForeignKey('allbooks.bid'), nullable=False)
    usertobook = db.relationship('Userinfo', backref=db.backref('userinfo', cascade='all, delete-orphan'))
    booktouser = db.relationship('Allbooks', backref=db.backref('allbooks', cascade='all, delete-orphan'))


# 创建模型
class Userinfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    usernum = db.Column(db.String(20), unique=True)
    userpwd = db.Column(db.String(100))
    useraddtime = db.Column(db.String(20), unique=True)

    def __init__(self, usernum, userpwd=None):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        self.username = random_str
        self.usernum = usernum
        self.userpwd = userpwd
        self.useraddtime = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")

    def add(self):
        if self.isExisted():
            try:
                db.session.add(self)
                db.session.commit()
                return self.username
            except Exception as e:
                db.session.rollback()
                print(e)
                return 0
        else:
            return 0

    def isExisted(self):
        tempusernum = db.session.query(Userinfo).filter(Userinfo.usernum == self.usernum).first()
        if tempusernum is None:
            return 1
        else:
            return 0

    def getuserbooks(self):
        query = text(f"select * from usersbooks where userid={self.id}")
        result_proxy = db.session.execute(query)
        res = result_proxy.fetchall()
        return res


class Allbooks(db.Model):
    __tablename__ = 'allbooks'
    bid = db.Column(db.String(60), primary_key=True, nullable=False)
    bookname = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    categories = db.Column(db.String(15))
    S_categories = db.Column(db.String(15))
    descipe = db.Column(db.Text)
    imgurl = db.Column(db.String(150))


class Bookcategories(db.Model):
    __tabelname__ = 'bookcategories'
    cateid = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    categoryname = db.Column(db.String(45), nullable=False)


class Bookcomments(db.Model):
    __tabelname__ = 'bookcomments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(35), nullable=False)
    userid = db.Column(db.String(20), db.ForeignKey('userinfo.usernum'), nullable=False)
    bookid = db.Column(db.String(60), db.ForeignKey('allbooks.bid'), nullable=False)
    comment = db.Column(db.String(210))
    addtimestamp = db.Column(db.Integer, nullable=False)
    usertocom = db.relationship('Userinfo', backref=db.backref('userinfo2', cascade='all, delete-orphan'))
    comtouser = db.relationship('Allbooks', backref=db.backref('allbooks2', cascade='all, delete-orphan'))

    def __init__(self, uid, userid, bookid, comment):
        self.uid = uid
        self.userid = userid
        self.bookid = bookid
        self.comment = comment
        self.addtimestamp = int(datetime.datetime.now().timestamp())

    def addcomment(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.userid
        except Exception as e:
            db.session.rollback()
            print(e)
            return 0


class Booksfetch:
    def getbookchaptertitle(self, tablename):
        query = text(f"select chaptertitle from {tablename}")
        result_proxy = db.session.execute(query)
        res = result_proxy.fetchall()
        return res

    def getbookchaptercontent(self, tablename, chapterid):
        query = text(f"select content,chaptertitle from {tablename} where id={chapterid}")
        result_proxy = db.session.execute(query)
        res = result_proxy.fetchall()
        return res
