from flask import Blueprint, render_template, session, request
import psycopg2

lab5 = Blueprint('lab5', __name__)


@lab5.route("/")
def main():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route("/lab5/login")
def login():
    return render_template('lab5/login.html')  


@lab5.route("/lab5/list")
def list_articles():
    return "Список статей"

@lab5.route("/lab5/create")
def create_article():
    return "Создать статью"


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='liza_stabrovskaya_knowledge_base',
            user='liza_stabrovskaya_knowledge_base',
            password='555'
        )
        cur = conn.cursor()  

        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))  
        conn.commit()  
        cur.close()
        conn.close()
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка БД: {str(e)}')