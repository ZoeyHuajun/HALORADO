
SECRET_KEY = 'zhanghuajun'
USER = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = 3306
NAME = 'halorado'
MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'