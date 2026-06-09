#为了避免循环引用。建立exts来建立db 然后app 和 models 分别import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, text, MetaData,Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from flask_migrate import Migrate

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
    #index
    "ix": 'ix_%(column_0_label)s',
    #unique constraint
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    #check constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    #  foreign key
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    # primary key
    "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()