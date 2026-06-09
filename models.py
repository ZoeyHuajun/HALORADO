#存放所有models
from exts import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100),unique=True)
    username: Mapped[str] = mapped_column(String(50))
    _password: Mapped[str] = mapped_column(String(200))

    def __init__(self, *args, **kwargs):
          password = kwargs.get("password")
          if password:
               kwargs.pop("password")
          self.password = password

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self._password, raw_password) # 检验是否密码正确