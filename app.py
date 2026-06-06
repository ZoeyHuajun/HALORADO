from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import String, text, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_migrate import Migrate

# Create a Flask application instance
app = Flask(__name__)

# Load configuration settings from the config.py file
#app.config['SECRET_KEY'] = '123456'
app.config.from_object(config)
#链接数据库
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Test the database connection
#with app.app_context():
#    with db.engine.connect() as conn:
#      result = conn.execute(text("SELECT 1"))
#      print(result.fetchall())
 

#建立数据表格等
# Import necessary modules from SQLAlchemy Base class for declarative models
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
# Create a Flask application instance 
db = SQLAlchemy(app=app,model_class=Base)
migrete = Migrate(app, db)
# Define a User model for the database
class User(db.Model):
    #name of the table in the database
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username : Mapped[str] = mapped_column(String(50), nullable=False)
    password : Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False) #nullable 表示该字段不能为空

with app.app_context():
    db.create_all()

@app.route('/create')
def create_user():
    user1 = User(username = "zhanghuajun",password = "000000", email = "zhanghuajun@gmail.com")
    db.session.add(user1)
    db.session.commit()
    return"User created successfully"
@app.route('/read')
def read_users():
    users = db.session.scalars(db.select(User).where(User.id == 1)).all()
    print(users)
    return "read successful"

if __name__ == '__main__':
    # Run the Flask application with new host and port settings
    app.run(debug=True, host='0.0.0.0', port=5050)