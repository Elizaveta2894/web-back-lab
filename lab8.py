from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__, 
                template_folder='templates/lab8')

@lab8.route('/lab8/')
def main():
    return render_template('lab8.html')  

@lab8.route('/login')
def login():
    return "Страница входа"

@lab8.route('/register')
def register():
    return "Страница регистрации"

@lab8.route('/articles')
def articles():
    return "Список статей"

@lab8.route('/create')
def create():
    return "Создание статьи"