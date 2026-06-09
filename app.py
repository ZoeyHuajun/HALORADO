from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import Column, ForeignKey, Integer, String, text, MetaData,Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from flask_migrate import Migrate
from typing import List
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)

#引用db from exts 初始化
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

#details
@app.route('/recipes/<int:recipe_id>')
def details(recipe_id):
    return render_template('recipes.html', recipe_id = recipe_id)

@app.route('/pub_r')
def public_recipes():
    return render_template('publish.html')

@app.route('/qb')
def pub():
    return render_template('public_question.html')

@app.route('/halo')
def halo():
    return render_template('halo.html')


if __name__ == '__main__':  
    app.run(debug=True)