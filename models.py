#存放所有models
from exts import db
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import Integer, String,Text,Float,DateTime,ForeignKey
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from typing import List


class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100),unique=True)
    username: Mapped[str] = mapped_column(String(50))
    _password: Mapped[str] = mapped_column(String(200))

    recipes: Mapped["Recipes"] = relationship("Recipes", back_populates="publisher")

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
    
class RecipeCategory(db.Model):
     __tablename__="recipe_category"
     id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
     name: Mapped[str] = mapped_column(String(100))

     recipes: Mapped[List["Recipes"]] = relationship("Recipes",back_populates="category")

class Recipes(db.Model):
     __tablename__="recipes"
     id : Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
     name: Mapped[str] = mapped_column(String(100))
     ingredient : Mapped[str] = mapped_column(Text)
     step: Mapped[str] = mapped_column(Text)
     picture: Mapped[float] = mapped_column(String(200))
     provider: Mapped[str] = mapped_column(String(100))
     pub_date : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    #食谱属于哪一个类别
     category_id : Mapped[int] = mapped_column(Integer,ForeignKey("recipe_category.id"))
     category: Mapped[RecipeCategory] = relationship("RecipeCategory",back_populates="recipes")

     publish_id : Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
     publisher: Mapped[User] = relationship("User", back_populates="recipes")

class VerificationCode(db.Model):
     __tablename__="verification_code"
     id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
     email: Mapped[str] = mapped_column(String(100))
     code: Mapped[str] = mapped_column(String(10))
     create_time : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)