from flask import Flask, render_template, request,redirect,jsonify,g,send_from_directory
from ai_model import ask_ai
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
import commands
from decorators import login_required
import uuid #random filename
import os
from dlmodel import predict

app = Flask(__name__)
app.config.from_object(config)

#引用db from exts 初始化
db.init_app(app)
migrate.init_app(app,db)
mail.init_app(app)
# bind the command from .py / will update the category as commands /nave ber
app.cli.command("init_category")(commands.init_recipe_category)

#钩子函数
@app.before_request
def before_request():
    user_id = session.get('user.id')
    if user_id:
        user = db.session.get(User, user_id)
        #g.user can use for all the web.  thread g
        g.user = user 
    else:
        g.user = None

#　if every page has the part 钩子函数
@app.context_processor
def context_processor():
    #scalars for multiple items  scalar for one
    categories = db.session.scalars(db.select(RecipeCategory)).all()
    return {
        'user': g.user,
        'categories' : categories
    }


@app.route('/')
def index():
    category_id = request.args.get('category',type=int)
    if category_id:
        stmt = db.select(Recipes).where(Recipes.category_id == category_id)
    else:
        stmt = db.select(Recipes)
    recipes = db.session.scalars(stmt.order_by(Recipes.pub_date.desc())).all()
    return render_template('index.html',recipes = recipes)    

@app.post('/logout')
def logout():
    #log out
    session.clear()
    return redirect('/')

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
    recipe = db.session.get(Recipes, recipe_id)
    return render_template('recipes.html', recipe = recipe)

@app.route('/pub_r',methods = ['GET','POST'])
#这是一个装饰器 自己定义的 必须加载到被限制的api下面
@login_required
def public_recipes():
    if request.method == 'GET':
        category = db.session.scalars(db.select(RecipeCategory)).all()
        return render_template('publish.html', category = category)
    else:
        picture = request.form.get("picture")
        category_id = request.form.get("category")
        name = request.form.get("name")
        ingredient = request.form.get("ingredient")
        step = request.form.get("content")
        provider = request.form.get("provider")
        recipes = Recipes(
            picture = picture,
            category_id = category_id,
            name = name,
            ingredient = ingredient,
            step = step,
            provider = provider,
            publish_id = g.user.id
        )
        db.session.add(recipes)
        db.session.commit()
        return redirect('/')


@app.post('/upload/picture')
def upload_pic():
    #when upload. name is picture
    picture = request.files.get("picture")
    #rename
    ext = picture.filename.split(".")[-1]
    filename = f'{uuid.uuid4()}.{ext}' # random picture name
    picture_path = os.path.join(app.config['MEDIA_DIR'],filename)
    picture.save(picture_path)

    category_name = predict(picture_path)
    category = db.session.scalar(db.select(RecipeCategory).where(RecipeCategory.name == category_name))
    if not category:
        return jsonify({
            "result":False,
            "message":"Category not found"
    })
    return jsonify({
        "result":True, 
        "message":None,
        "filename":filename,
        "category": {"id":category.id, "name":category_name}
    })

@app.route('/qb')
def pub():
    return render_template('public_question.html')

@app.route('/halo',methods=["GET","POST"])
def halo():
    if request.method == "GET":
        return render_template('halo.html')
    else:
        data = request.get_json()
        user_message = data.get("message")
        answer = ask_ai(user_message)

        return jsonify({"result":True, "message":None, "answer":answer})

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

@app.route('/detail/<int:recipe_id>')
def detail(recipe_id):
    recipe = db.session.get(Recipes,recipe_id)
    return render_template("detail.html", recipe = recipe)
@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(config.MEDIA_DIR,filename)

if __name__ == '__main__':  
    app.run(debug=True)