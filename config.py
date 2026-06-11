import os

SECRET_KEY = 'zhanghuajun'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR,"media")

USER = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = 3306
NAME = 'halorado'
MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'

# flask_mail init set fixed format
MAIL_SERVER = "smtp.gmail.com"
# ssl -> 465. TLS -> 587
MAIL_USE_TLS = True
MAIL_PORT = 587
MAIL_USERNAME = "haloradostudio@gmail.com"
MAIL_PASSWORD = "rbwtrtysdwdrlivi"
MAIL_DEFAULT_SENDER = "haloradostudio@gmail.com"

