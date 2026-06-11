from flask import Flask, render_template, request,redirect,jsonify,g
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
from datetime import datetime,timedelta
from flask import session

app = Flask(__name__)
app.config.from_object(config)

#引用db from exts 初始化
db.init_app(app)
migrate.init_app(app,db)
mail.init_app(app)


@app.before_request
def before_request():
    user_id = session.get('user.id')
    if user_id:
        user = db.session.get(User, user_id)
        #g.user can use for all the web.  thread g
        g.user = user 
    else:
        g.user = None

@app.context_processor
def context_processor():
    return {
        'user':g.user
    }


@app.route('/')
def index():
    return render_template('index.html')    

@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")
        user = db.session.scalar(db.select(User).where(User.email == email))
        if user and user.check_password(password):
            session['user.id'] = user.id
            #rememer me 31 days limite:session.permanent = True
            if remember:
                session.permanent = True
            return redirect('/')
        elif user is None:
            print("You have not have an account yet. Create your new account!")
            return redirect('/register')
        else:
            print("Email or password is incorrect!")
            return redirect('/login')

            


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        code = request.form.get("code")
        #check the code
        code_model = db.session.scalar(db.select(VerificationCode).where((VerificationCode.email == email)&(VerificationCode.code == code)))

        #timedelta 5mins 
        if not code_model or (datetime.now() - code_model.create_time) > timedelta(minutes = 5):
            return jsonify({"result": False,"message":"Verification code expired. Please enter the correct verification code! "})

        user = User(email = email, username = username, password = password)

        db.session.add(user)
        db.session.commit()
        return jsonify({"result": True, "message" : None})


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
    #check if these is old code
    code_model = db.session.scalar(db.select(VerificationCode).where(VerificationCode.email==email))
    if code_model:
        code_model.code = code 
        code_model.create_time = datetime.now()
    else:
        #save the code 
        code_model = VerificationCode(code=code, email=email)
        db.session.add(code_model)
    db.session.commit()
    return jsonify({"result": True, "message":None})


if __name__ == '__main__':  
    app.run(debug=True)