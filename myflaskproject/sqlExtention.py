HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'bookdata'
PASSWORD = 'MySQL'
USERNAME = 'root'
DBURI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
