from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__, 
                template_folder='templates/lab8',
                static_folder='static/lab8')

@lab8.route('/lab8/')
def main():
    return render_template('lab8.html')  

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me') == 'on'  

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect('/lab8/')

    return render_template('/lab8/login.html', 
                          error='Ошибка входа: логин и/или пароль неверны')

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
    
    login_user(new_user, remember=False)
    flash(f'Пользователь {login_form} успешно зарегистрирован и вошел в систему!', 'success')
    
    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    search_query = request.args.get('search', '').strip()
    if search_query:
        user_articles = articles.query.filter(
            db.and_(
                articles.login_id == current_user.id,
                db.or_(
                    articles.title.ilike(f'%{search_query}%'),
                    articles.article_text.ilike(f'%{search_query}%')
                )
            )
        ).all()

        public_articles = articles.query.filter(
            db.and_(
                articles.is_public == True,
                articles.login_id != current_user.id,
                db.or_(
                    articles.title.ilike(f'%{search_query}%'),
                    articles.article_text.ilike(f'%{search_query}%')
                )
            )
        ).all()
    else:
        user_articles = articles.query.filter_by(login_id=current_user.id).all()
        public_articles = articles.query.filter(
            db.and_(
                articles.is_public == True,
                articles.login_id != current_user.id
            )
        ).all()
    
    for article in public_articles:
        article.user_login = users.query.get(article.login_id).login
    
    return render_template('lab8/articles.html', 
                          articles=user_articles,
                          public_articles=public_articles,
                          search_query=search_query)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    content = request.form.get('content')
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        return render_template('lab8/create.html',
                               error='Заголовок не может быть пустым',
                               title=title,
                               content=content)
    
    if not content or not content.strip():
        return render_template('lab8/create.html',
                               error='Содержание статьи не может быть пустым',
                               title=title,
                               content=content)
    
    new_article = articles(
        title=title,
        article_text=content,
        login_id=current_user.id,
        is_public=is_public
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    flash('Статья успешно создана!', 'success')
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        flash('Статья не найдена или у вас нет прав для ее редактирования', 'error')
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    content = request.form.get('content')
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        return render_template('lab8/edit.html',
                               article=article,
                               error='Заголовок не может быть пустым')
    
    if not content or not content.strip():
        return render_template('lab8/edit.html',
                               article=article,
                               error='Содержание статьи не может быть пустым')
    
    article.title = title
    article.article_text = content
    article.is_public = is_public
    
    db.session.commit()
    
    flash('Статья успешно обновлена!', 'success')
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):

    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        flash('Статья не найдена или у вас нет прав для ее удаления', 'error')
        return redirect('/lab8/articles')
    
    db.session.delete(article)
    db.session.commit()
    
    flash('Статья успешно удалена!', 'success')
    return redirect('/lab8/articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect('/lab8/')

@lab8.route('/lab8/public_articles')
def public_articles():
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        public_articles_list = articles.query.filter(
            db.and_(
                articles.is_public == True,
                db.or_(
                    articles.title.ilike(f'%{search_query}%'),
                    articles.article_text.ilike(f'%{search_query}%')
                )
            )
        ).all()
    else:
        public_articles_list = articles.query.filter_by(is_public=True).all()
    
    for article in public_articles_list:
        article.user_login = users.query.get(article.login_id).login
    
    return render_template('lab8/public_articles.html', 
                          public_articles=public_articles_list,
                          search_query=search_query)