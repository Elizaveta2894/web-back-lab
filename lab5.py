from flask import Blueprint, render_template, session, request, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def main():
    return render_template('lab5/lab5.html', login=session.get('login', 'Anonymous'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='liza_stabrovskaya_knowledge_base',
            user='liza_stabrovskaya_knowledge_base',
            password='555'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route("/lab5/logout")
def logout():
    session.pop('login', None)
    return redirect('/lab5/')  

@lab5.route("/lab5/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')  

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните все поля")

    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', 
                                error='Логин и/или пароль неверны')
        
        if not check_password_hash(user['password'], password): 
            db_close(conn, cur)
            return render_template('lab5/login.html', 
                                error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', 
                             error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '').strip()

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните логин и пароль')

    try:
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login = ?;", (login,))
        
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')

        password_hash = generate_password_hash(password)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", 
                       (login, password_hash, real_name if real_name else login))
        else:
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                       (login, password_hash, real_name if real_name else login))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка БД: {str(e)}')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    try:
        login = session.get('login')
        if not login:
            return redirect('/lab5/login')

        if request.method == 'GET':
            return render_template('lab5/create_article.html')

        title = request.form.get('title', '').strip()
        article_text = request.form.get('article_text', '').strip()
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            return render_template('lab5/create_article.html', 
                                 error="Заполните название и текст статьи")

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        user_id = user["id"]
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) 
                VALUES (%s, %s, %s, %s, %s);
            """, (user_id, title, article_text, is_favorite, is_public))
        else:
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) 
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, title, article_text, is_favorite, is_public))

        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return render_template('lab5/create_article.html', 
                             error=f'Ошибка при сохранении статьи: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    try:
        login = session.get('login')
        if not login:
            return redirect('/lab5/login')

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = %s 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id = ? 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
        
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles, login=login)
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return f"Ошибка при загрузке статей: {str(e)}"

@lab5.route('/lab5/public')
def public_articles():
    try:
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.*, u.login, u.real_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = TRUE 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.*, u.login, u.real_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = TRUE 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('/lab5/public_articles.html', articles=articles)
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return render_template('/lab5/error.html', 
                             error=f'Ошибка при загрузке публичных статей: {str(e)}')


@lab5.route('/lab5/users')
def users_list():
    conn = None
    cur = None
    try:

        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
        else:
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
        
        users = cur.fetchall()
        if cur:
            cur.close()
        if conn:
            conn.close()
            
        return render_template('/lab5/users.html', users=users)
        
    except Exception as e:

        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except:
            pass

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ошибка</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .error {{ color: red; background: #fee; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                a {{ color: #3498db; text-decoration: none; }}
            </style>
        </head>
        <body>
            <h1>Ошибка загрузки пользователей</h1>
            <div class="error">{str(e)}</div>
            <p><a href="/lab5/">Вернуться на главную</a></p>
        </body>
        </html>
        """

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    try:
        login = session.get('login')
        if not login:
            return redirect('/lab5/login')

        if request.method == 'GET':
            conn, cur = db_connect()
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT real_name FROM users WHERE login = %s;", (login,))
            else:
                cur.execute("SELECT real_name FROM users WHERE login = ?;", (login,))
            
            user = cur.fetchone()
            db_close(conn, cur)
            
            return render_template('/lab5/profile.html', user=user)

        real_name = request.form.get('real_name', '').strip()
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        errors = []

        if new_password:
            if not current_password:
                errors.append("Введите текущий пароль для смены пароля")
            elif not check_password_hash(user['password'], current_password):
                errors.append("Неверный текущий пароль")
            elif new_password != confirm_password:
                errors.append("Новый пароль и подтверждение не совпадают")
            elif len(new_password) < 3:
                errors.append("Новый пароль должен быть не менее 3 символов")

        if errors:
            db_close(conn, cur)
            return render_template('/lab5/profile.html', user=user, errors=errors)

        if new_password:
            password_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name = %s, password = %s WHERE login = %s;", 
                           (real_name, password_hash, login))
            else:
                cur.execute("UPDATE users SET real_name = ?, password = ? WHERE login = ?;", 
                           (real_name, password_hash, login))
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name = %s WHERE login = %s;", (real_name, login))
            else:
                cur.execute("UPDATE users SET real_name = ? WHERE login = ?;", (real_name, login))

        db_close(conn, cur)
        
        return render_template('/lab5/profile_success.html', 
                             message="Данные профиля успешно обновлены")
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return render_template('/lab5/profile.html', 
                             errors=[f'Ошибка при обновлении профиля: {str(e)}'])

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    try:
        login = session.get('login')
        if not login:
            return redirect('/lab5/login')

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id = %s AND user_id = %s;", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id = ? AND user_id = ?;", (article_id, user_id))
        
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/list')

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article)

        title = request.form.get('title', '').strip()
        article_text = request.form.get('article_text', '').strip()
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            return render_template('lab5/edit_article.html', 
                                 article=article,
                                 error="Заполните название и текст статьи")

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE articles SET title = %s, article_text = %s, is_favorite = %s, is_public = %s 
                WHERE id = %s;
            """, (title, article_text, is_favorite, is_public, article_id))
        else:
            cur.execute("""
                UPDATE articles SET title = ?, article_text = ?, is_favorite = ?, is_public = ? 
                WHERE id = ?;
            """, (title, article_text, is_favorite, is_public, article_id))

        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             error=f'Ошибка при редактировании статьи: {str(e)}')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    try:
        login = session.get('login')
        if not login:
            return redirect('/lab5/login')

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id = %s AND user_id = %s;", (article_id, user_id))
        else:
            cur.execute("DELETE FROM articles WHERE id = ? AND user_id = ?;", (article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    except Exception as e:
        if 'conn' in locals() and 'cur' in locals():
            db_close(conn, cur)
        return f"Ошибка при удалении статьи: {str(e)}"