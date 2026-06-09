from flask import Flask, render_template, request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import config
from sqlalchemy import Column, ForeignKey, Integer, String, text, MetaData,Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from flask_migrate import Migrate
from typing import List
from exts import db, migrate,mail
from models import User,VerificationCode,RecipeCategory,Recipes
from flask_mail import Message
import random
import string

app = Flask(__name__)
app.config.from_object(config)

#引用db from exts 初始化
db.init_app(app)
migrate.init_app(app,db)
mail.init_app(app)

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

@app.get('/email/code')
def get_email_code():
    email = request.args.get("email")
    if not email:
        return jsonify({"result": False, "message": "Please enter an Email."})
    #get verification code
    source = string.digits * 6
    code = "".join(random.sample(source,6))
    message = Message(
        subject = "[ HALORADO ] Verification Code:",
        recipients=[email],
        body=f"Your verification Code : {code}"
    )
    try:
        mail.send(message)
    except Exception as e:
        return jsonify({"result":False, "message":str(e)})
    #save the code 
    email_code = VerificationCode(code=code, email=email)
    db.session.add(email_code)
    db.session.commit()
    return jsonify({"result": True, "message":None})


if __name__ == '__main__':  
    app.run(debug=True)