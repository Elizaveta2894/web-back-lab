from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user

lab8 = Blueprint('lab8', __name__, 
                template_folder='templates/lab8')

@lab8.route('/lab8/')
def main():
    return render_template('lab8.html')  

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = False)
            return redirect('/lab8/')

    return render_template('/lab8/login.html', 
                            error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles')
def article_list():
    return "список статей"

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        users_list = users.query.all()
        return render_template('lab8/register.html', users_list=users_list)    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form or not login_form.strip():
        users_list = users.query.all()
        return render_template('lab8/register.html',
                                error='Имя пользователя не может быть пустым',
                                users_list=users_list)
    if not password_form or not password_form.strip():
        users_list = users.query.all()
        return render_template('lab8/register.html',
                                error='Пароль не может быть пустым',
                                users_list=users_list)
    if len(login_form.strip()) < 3:
        users_list = users.query.all()
        return render_template('lab8/register.html',
                                error='Имя пользователя должно быть не менее 3 символов',
                                users_list=users_list) 
    if len(password_form) < 4:
        users_list = users.query.all()
        return render_template('lab8/register.html',
                                error='Пароль должен быть не менее 4 символов',
                                users_list=users_list)
    login_form = login_form.strip()
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        users_list = users.query.all()
        return render_template('lab8/register.html',
                                error='Такой пользователь уже существует',
                                users_list=users_list)
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    users_list = users.query.all()
    return render_template('lab8/register.html',
                            success=f'Пользователь {login_form} успешно зарегистрирован!',
                            users_list=users_list)

@lab8.route('/articles')
def articles():
    return "Список статей"

@lab8.route('/create')
def create():
    return "Создание статьи"